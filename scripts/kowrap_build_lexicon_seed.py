#!/usr/bin/env python3
"""Build a high-frequency protected-term seed TSV from KOWRAP candidates."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from kowrap_build_review_set import merge_candidate_rows, read_candidates, sort_key, type_guess


FIELDS = [
    "term",
    "hangul_len",
    "count",
    "domain",
    "type_guess",
    "source_paths",
    "status",
    "note",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Candidate JSONL files")
    parser.add_argument("--out", required=True)
    parser.add_argument("--min-hangul", type=int, default=5)
    parser.add_argument("--max-hangul", type=int, default=8)
    parser.add_argument("--top", type=int, default=500)
    parser.add_argument(
        "--exclude-type",
        action="append",
        default=["noisy-extraction", "article-reference"],
    )
    args = parser.parse_args()

    excluded = set(args.exclude_type)
    rows = []
    for row in merge_candidate_rows(read_candidates(args.inputs)):
        hangul_len = int(row.get("hangul_len", 0))
        guessed_type = type_guess(row.get("candidate", ""))
        if hangul_len < args.min_hangul or hangul_len > args.max_hangul:
            continue
        if guessed_type in excluded:
            continue
        rows.append(row)

    rows.sort(key=lambda row: sort_key(row, "frequency-short"))
    rows = rows[: args.top]

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "term": row["candidate"],
                    "hangul_len": row.get("hangul_len", ""),
                    "count": row.get("count", ""),
                    "domain": row.get("domain", ""),
                    "type_guess": type_guess(row["candidate"]),
                    "source_paths": ";".join(row.get("source_paths", [])[:3]),
                    "status": "todo",
                    "note": "",
                }
            )

    print(f"wrote {len(rows)} lexicon seed rows to {out}")


if __name__ == "__main__":
    main()

