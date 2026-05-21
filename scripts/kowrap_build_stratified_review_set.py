#!/usr/bin/env python3
"""Build a stratified KOWRAP review TSV/JSONL from candidate JSONL files."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from kowrap_build_review_set import (
    REVIEW_FIELDS,
    build_review_row,
    merge_candidate_rows,
    read_candidates,
    sort_key,
    type_guess,
)


DEFAULT_BUCKETS = [
    "short:5:8:200:frequency-short",
    "mid:9:15:200:frequency-short",
    "long:16::100:long",
]


def parse_bucket(raw: str) -> dict[str, object]:
    label, min_len, max_len, size, sort_mode = raw.split(":", 4)
    return {
        "label": label,
        "min_len": int(min_len),
        "max_len": int(max_len) if max_len else None,
        "size": int(size),
        "sort_mode": sort_mode,
    }


def in_bucket(row: dict, bucket: dict[str, object]) -> bool:
    hangul_len = int(row.get("hangul_len", 0))
    max_len = bucket["max_len"]
    return hangul_len >= bucket["min_len"] and (max_len is None or hangul_len <= max_len)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Candidate JSONL files")
    parser.add_argument("--out-tsv", required=True)
    parser.add_argument("--out-jsonl")
    parser.add_argument("--bucket", action="append", default=DEFAULT_BUCKETS)
    parser.add_argument("--context-radius", type=int, default=90)
    parser.add_argument("--id-prefix", default="seed")
    parser.add_argument(
        "--exclude-type",
        action="append",
        default=["noisy-extraction", "article-reference"],
    )
    args = parser.parse_args()

    excluded = set(args.exclude_type)
    rows = [
        row
        for row in merge_candidate_rows(read_candidates(args.inputs))
        if type_guess(row.get("candidate", "")) not in excluded
    ]
    buckets = [parse_bucket(raw) for raw in args.bucket]
    selected = []
    used_candidates = set()
    bucket_counts = {}
    for bucket in buckets:
        pool = [
            row
            for row in rows
            if row["candidate"] not in used_candidates and in_bucket(row, bucket)
        ]
        pool.sort(key=lambda row, mode=bucket["sort_mode"]: sort_key(row, mode))
        chosen = pool[: bucket["size"]]
        bucket_counts[bucket["label"]] = len(chosen)
        for row in chosen:
            used_candidates.add(row["candidate"])
            selected.append((bucket["label"], row))

    review_rows = []
    for i, (bucket_label, row) in enumerate(selected, 1):
        review_row = build_review_row(
            row, f"{args.id_prefix}-{i:06d}", args.context_radius
        )
        review_row["review_note"] = f"bucket={bucket_label}"
        review_rows.append(review_row)

    if not review_rows:
        raise SystemExit("no review rows matched the input filters")

    out_tsv = Path(args.out_tsv).expanduser()
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    with out_tsv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REVIEW_FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(review_rows)

    if args.out_jsonl:
        out_jsonl = Path(args.out_jsonl).expanduser()
        out_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with out_jsonl.open("w", encoding="utf-8") as f:
            for row in review_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    count_text = ", ".join(f"{label}={count}" for label, count in bucket_counts.items())
    print(f"wrote {len(review_rows)} rows to {out_tsv} ({count_text})")


if __name__ == "__main__":
    main()

