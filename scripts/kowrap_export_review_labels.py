#!/usr/bin/env python3
"""Export reviewed KOWRAP TSV labels to compact JSONL."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


EDITABLE_FIELDS = {
    "protected_spans",
    "preferred_breaks",
    "acceptable_breaks",
    "bad_breaks",
    "label_status",
    "review_note",
}


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def strip_breaks(value: str) -> str:
    return value.replace("/", "")


def validate_breaks(candidate: str, values: list[str], field: str) -> list[str]:
    errors = []
    for value in values:
        if strip_breaks(value) != candidate:
            errors.append(f"{field} value does not match candidate after removing '/': {value}")
    return errors


def build_record(row: dict[str, str]) -> tuple[dict[str, object], list[str]]:
    candidate = row["candidate"]
    preferred = split_values(row.get("preferred_breaks", ""))
    acceptable = split_values(row.get("acceptable_breaks", ""))
    bad = split_values(row.get("bad_breaks", ""))
    errors = []
    errors.extend(validate_breaks(candidate, preferred, "preferred_breaks"))
    errors.extend(validate_breaks(candidate, acceptable, "acceptable_breaks"))
    errors.extend(validate_breaks(candidate, bad, "bad_breaks"))

    record = {
        "id": row["review_id"],
        "candidate": candidate,
        "domain": row.get("domain", ""),
        "hangul_len": int(row.get("hangul_len") or 0),
        "type_hint": row.get("type_guess", ""),
        "stem_guess": row.get("stem_guess", ""),
        "suffix_guess": row.get("suffix_guess", ""),
        "protected_spans": split_values(row.get("protected_spans", "")),
        "preferred_breaks": preferred,
        "acceptable_breaks": acceptable,
        "bad_breaks": bad,
        "context": row.get("context", ""),
        "context_path": row.get("context_path", ""),
        "source_paths": split_values(row.get("source_paths", "")),
        "label_status": row.get("label_status", ""),
        "review_note": row.get("review_note", ""),
    }
    return record, errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_tsv", help="Reviewed KOWRAP TSV")
    parser.add_argument("--out", required=True, help="Output JSONL path")
    parser.add_argument(
        "--include-status",
        action="append",
        default=["reviewed"],
        help="Status to export; repeatable. Default: reviewed",
    )
    parser.add_argument("--allow-errors", action="store_true")
    args = parser.parse_args()

    input_tsv = Path(args.input_tsv).expanduser()
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)

    exported = 0
    all_errors = []
    with input_tsv.open(encoding="utf-8", newline="") as f, out.open("w", encoding="utf-8") as g:
        reader = csv.DictReader(f, delimiter="\t")
        missing = EDITABLE_FIELDS - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"missing columns: {', '.join(sorted(missing))}")
        for row in reader:
            if row.get("label_status") not in args.include_status:
                continue
            record, errors = build_record(row)
            if errors:
                all_errors.extend(f"{row.get('review_id')}: {error}" for error in errors)
                if not args.allow_errors:
                    continue
            g.write(json.dumps(record, ensure_ascii=False) + "\n")
            exported += 1

    if all_errors and not args.allow_errors:
        for error in all_errors[:20]:
            print(error)
        raise SystemExit(f"found {len(all_errors)} validation errors; re-run with --allow-errors to export anyway")

    print(f"exported {exported} labels to {out}")


if __name__ == "__main__":
    main()

