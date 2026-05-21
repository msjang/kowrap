#!/usr/bin/env python3
"""Build a human review TSV/JSONL with context for break labeling."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


PARTICLE_SUFFIXES = [
    "으로부터",
    "로부터",
    "에서는",
    "에서",
    "에게",
    "으로",
    "로서",
    "로써",
    "까지",
    "부터",
    "처럼",
    "보다",
    "이나",
    "거나",
    "와",
    "과",
    "은",
    "는",
    "이",
    "가",
    "을",
    "를",
    "의",
    "에",
    "중",
    "도",
]


NOISY_EXTRACTION_RE = re.compile(
    r"([0-9]+여년간|월까지의|"
    r"하면서|하였으며|하였고|하였다|하였음|기여함|있으며|되었으며|"
    r"개선하였|노력하였|추진하였)"
)


def guess_stem_suffix(candidate: str) -> tuple[str, str]:
    for suffix in PARTICLE_SUFFIXES:
        if candidate.endswith(suffix) and len(candidate) > len(suffix) + 2:
            return candidate[: -len(suffix)], suffix
    return candidate, ""


def type_guess(candidate: str) -> str:
    stem, _ = guess_stem_suffix(candidate)
    if NOISY_EXTRACTION_RE.search(candidate):
        return "noisy-extraction"
    if re.fullmatch(r"제[0-9가-힣의]+[조항호][0-9가-힣의조항호]*", candidate):
        return "article-reference"
    if stem.endswith(("법률", "특별법", "기본법", "진흥법", "전파법", "전자정부법")):
        return "law-title"
    if (
        candidate.count("장관") >= 2
        or candidate.count("위원회") >= 2
        or candidate.count("진흥원") >= 2
        or candidate.count("규칙") >= 2
    ):
        return "agency-list"
    if "특별시장광역시장" in candidate or "국회법원헌법재판소" in candidate:
        return "agency-list"
    if candidate.count("맞춤형") >= 3 or candidate.count("분야") >= 3:
        return "enumeration"
    if re.search(r"(허가|승인|인증|검증|인가|등록|신고|지정|동의|협의){3,}", candidate):
        return "enumeration"
    if re.search(r"(생산중지|수입중지|판매중지|사용중지){2,}", candidate):
        return "enumeration"
    return "compound"


def sort_key(row: dict) -> tuple[int, int, int, str]:
    candidate = row.get("candidate", "")
    guessed_type = type_guess(candidate)
    noisy_rank = 1 if guessed_type == "noisy-extraction" else 0
    return (
        noisy_rank,
        -int(row.get("hangul_len", 0)),
        -int(row.get("count", 0)),
        candidate,
    )


def candidate_pattern(candidate: str) -> re.Pattern[str]:
    escaped_chars = [re.escape(ch) for ch in candidate]
    return re.compile(r"[\sㆍ·_-]*".join(escaped_chars))


def find_context(candidate: str, source_paths: list[str], radius: int) -> tuple[str, str]:
    for raw in source_paths:
        path = Path(raw)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        idx = text.find(candidate)
        end = idx + len(candidate) if idx >= 0 else -1
        if idx < 0:
            match = candidate_pattern(candidate).search(text)
            if match:
                idx, end = match.span()
        if idx >= 0:
            left = max(0, idx - radius)
            right = min(len(text), end + radius)
            context = text[left:right].replace("\n", " ")
            context = re.sub(r"\s+", " ", context).strip()
            return context, str(path)
    return "", source_paths[0] if source_paths else ""


def read_candidates(paths: list[str]) -> list[dict]:
    rows = []
    for raw in paths:
        path = Path(raw).expanduser()
        with path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    row["_candidate_file"] = str(path)
                    rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Candidate JSONL files")
    parser.add_argument("--out-tsv", required=True)
    parser.add_argument("--out-jsonl")
    parser.add_argument("--top", type=int, default=500)
    parser.add_argument("--context-radius", type=int, default=90)
    parser.add_argument("--min-hangul", type=int, default=8)
    args = parser.parse_args()

    candidates = [
        row
        for row in read_candidates(args.inputs)
        if int(row.get("hangul_len", 0)) >= args.min_hangul
    ]
    candidates.sort(key=sort_key)
    candidates = candidates[: args.top]

    review_rows = []
    for i, row in enumerate(candidates, 1):
        candidate = row["candidate"]
        stem, suffix = guess_stem_suffix(candidate)
        source_paths = row.get("source_paths", [])
        context, context_path = find_context(candidate, source_paths, args.context_radius)
        review_rows.append(
            {
                "review_id": f"review-{i:06d}",
                "candidate": candidate,
                "stem_guess": stem,
                "suffix_guess": suffix,
                "type_guess": type_guess(candidate),
                "domain": row.get("domain", ""),
                "hangul_len": row.get("hangul_len", ""),
                "count": row.get("count", ""),
                "context": context,
                "context_path": context_path,
                "source_paths": ";".join(source_paths[:3]),
                "protected_spans": "",
                "preferred_breaks": "",
                "acceptable_breaks": "",
                "bad_breaks": "",
                "label_status": "todo",
                "review_note": "",
            }
        )

    out_tsv = Path(args.out_tsv).expanduser()
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    if not review_rows:
        raise SystemExit("no review rows matched the input filters")
    with out_tsv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(review_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(review_rows)

    if args.out_jsonl:
        out_jsonl = Path(args.out_jsonl).expanduser()
        out_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with out_jsonl.open("w", encoding="utf-8") as f:
            for row in review_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"wrote {len(review_rows)} review rows to {out_tsv}")


if __name__ == "__main__":
    main()
