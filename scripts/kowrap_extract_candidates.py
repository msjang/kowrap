#!/usr/bin/env python3
"""Extract long Korean word candidates from plain text files."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


HANGUL_RE = re.compile(r"[가-힣]")
TOKEN_RE = re.compile(r"[가-힣A-Za-z0-9]+")
TRIM_RE = re.compile(r"^[^가-힣A-Za-z0-9]+|[^가-힣A-Za-z0-9]+$")


def clean_token(token: str) -> str:
    return TRIM_RE.sub("", token)


def hangul_count(token: str) -> int:
    return len(HANGUL_RE.findall(token))


def is_article_reference_noise(token: str) -> bool:
    digit_count = sum(ch.isdigit() for ch in token)
    if token.startswith("제") and digit_count >= 2 and any(ch in token for ch in "조항호"):
        return True
    if digit_count >= 6 and re.search(r"[제조항호의]", token):
        return True
    return False


def iter_tokens(text: str, min_hangul: int, keep_article_refs: bool) -> list[str]:
    result = []
    for match in TOKEN_RE.finditer(text):
        token = clean_token(match.group(0))
        if hangul_count(token) >= min_hangul:
            if not keep_article_refs and is_article_reference_noise(token):
                continue
            result.append(token)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Plain text files")
    parser.add_argument("--out", required=True, help="Output JSONL path")
    parser.add_argument("--min-hangul", type=int, default=8)
    parser.add_argument("--source-class", default="restricted")
    parser.add_argument("--domain", default="unknown")
    parser.add_argument("--top", type=int, default=1000)
    parser.add_argument("--keep-article-refs", action="store_true")
    args = parser.parse_args()

    counts: Counter[str] = Counter()
    sources: dict[str, set[str]] = defaultdict(set)

    for raw in args.inputs:
        path = Path(raw).expanduser()
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in iter_tokens(text, args.min_hangul, args.keep_article_refs):
            counts[token] += 1
            if len(sources[token]) < 20:
                sources[token].add(str(path))

    ranked = sorted(
        counts.items(), key=lambda item: (-hangul_count(item[0]), -item[1], item[0])
    )
    if args.top:
        ranked = ranked[: args.top]

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for i, (token, count) in enumerate(ranked, 1):
            record = {
                "id": f"{args.domain}-candidate-{i:06d}",
                "candidate": token,
                "hangul_len": hangul_count(token),
                "count": count,
                "source_class": args.source_class,
                "license_note": "source terms pending; KOWRAP labels Apache-2.0 project-authored",
                "tokenizer_version": "separator-boundary-v1",
                "domain": args.domain,
                "source_paths": sorted(sources[token]),
                "safe_breaks": [],
                "bad_breaks": [],
                "notes": "",
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"wrote {len(ranked)} candidates to {out}")


if __name__ == "__main__":
    main()
