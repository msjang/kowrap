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


REVIEW_FIELDS = [
    "review_id",
    "candidate",
    "stem_guess",
    "suffix_guess",
    "type_guess",
    "domain",
    "hangul_len",
    "count",
    "context",
    "context_path",
    "source_paths",
    "protected_spans",
    "preferred_breaks",
    "acceptable_breaks",
    "bad_breaks",
    "label_status",
    "review_note",
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


def sort_key(row: dict, mode: str = "long") -> tuple[int, int, int, str]:
    candidate = row.get("candidate", "")
    guessed_type = type_guess(candidate)
    noisy_rank = 1 if guessed_type == "noisy-extraction" else 0
    hangul_len = int(row.get("hangul_len", 0))
    count = int(row.get("count", 0))
    if mode == "short-frequency":
        return (noisy_rank, hangul_len, -count, candidate)
    if mode == "frequency-short":
        return (noisy_rank, -count, hangul_len, candidate)
    if mode == "count-long":
        return (noisy_rank, -count, -hangul_len, candidate)
    return (
        noisy_rank,
        -hangul_len,
        -count,
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


def merge_candidate_rows(rows: list[dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    for row in rows:
        candidate = row["candidate"]
        if candidate not in merged:
            merged[candidate] = dict(row)
            merged[candidate]["count"] = int(row.get("count", 0))
            merged[candidate]["source_paths"] = list(row.get("source_paths", []))
            merged[candidate]["_domains"] = {row.get("domain", "")}
            continue
        target = merged[candidate]
        target["count"] = int(target.get("count", 0)) + int(row.get("count", 0))
        target["_domains"].add(row.get("domain", ""))
        seen = set(target.get("source_paths", []))
        for source_path in row.get("source_paths", []):
            if source_path not in seen and len(target["source_paths"]) < 40:
                target["source_paths"].append(source_path)
                seen.add(source_path)
    for row in merged.values():
        domains = sorted(domain for domain in row.pop("_domains", set()) if domain)
        row["domain"] = ",".join(domains)
    return list(merged.values())


def build_review_row(row: dict, review_id: str, context_radius: int) -> dict:
    candidate = row["candidate"]
    stem, suffix = guess_stem_suffix(candidate)
    source_paths = row.get("source_paths", [])
    context, context_path = find_context(candidate, source_paths, context_radius)
    return {
        "review_id": review_id,
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Candidate JSONL files")
    parser.add_argument("--out-tsv", required=True)
    parser.add_argument("--out-jsonl")
    parser.add_argument("--top", type=int, default=500)
    parser.add_argument("--context-radius", type=int, default=90)
    parser.add_argument("--min-hangul", type=int, default=8)
    parser.add_argument("--max-hangul", type=int)
    parser.add_argument(
        "--sort-mode",
        choices=["long", "short-frequency", "frequency-short", "count-long"],
        default="long",
    )
    parser.add_argument("--exclude-type", action="append", default=[])
    parser.add_argument("--dedupe-candidate", action="store_true")
    parser.add_argument("--id-prefix", default="review")
    args = parser.parse_args()

    candidates = [
        row
        for row in read_candidates(args.inputs)
        if int(row.get("hangul_len", 0)) >= args.min_hangul
        and (args.max_hangul is None or int(row.get("hangul_len", 0)) <= args.max_hangul)
        and type_guess(row.get("candidate", "")) not in set(args.exclude_type)
    ]
    if args.dedupe_candidate:
        candidates = merge_candidate_rows(candidates)
    candidates.sort(key=lambda row: sort_key(row, args.sort_mode))
    candidates = candidates[: args.top]

    review_rows = []
    for i, row in enumerate(candidates, 1):
        review_rows.append(build_review_row(row, f"{args.id_prefix}-{i:06d}", args.context_radius))

    out_tsv = Path(args.out_tsv).expanduser()
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    if not review_rows:
        raise SystemExit("no review rows matched the input filters")
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

    print(f"wrote {len(review_rows)} review rows to {out_tsv}")


if __name__ == "__main__":
    main()
