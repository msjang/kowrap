#!/usr/bin/env python3
"""Fetch current law body HTML from law.go.kr by Korean law name."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen


BASE = "https://www.law.go.kr"
UA = "Mozilla/5.0 KOWRAP/0.1"


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def find_iframe_src(html: str) -> str:
    match = re.search(r'<iframe[^>]+id="lawService"[^>]+src="([^"]+)"', html)
    if not match:
        raise RuntimeError("could not find lawService iframe")
    return match.group(1).replace("&amp;", "&")


def to_body_url(iframe_src: str) -> str:
    url = urljoin(BASE, iframe_src)
    return url.replace("lsInfoP.do", "lsInfoR.do")


def safe_name(name: str) -> str:
    return re.sub(r"[^0-9A-Za-z가-힣_.-]+", "_", name).strip("_")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="*", help="Law names")
    parser.add_argument("--names-file", help="UTF-8 text file with one law name per line")
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--metadata", help="Optional JSONL metadata output")
    args = parser.parse_args()

    names = list(args.names)
    if args.names_file:
        names.extend(
            line.strip()
            for line in Path(args.names_file).expanduser().read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        )

    outdir = Path(args.outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)
    meta_path = Path(args.metadata).expanduser() if args.metadata else None

    records = []
    for name in names:
        record = {"law_name": name, "status": "error"}
        try:
            landing_url = f"{BASE}/%EB%B2%95%EB%A0%B9/{quote(name)}"
            landing = fetch(landing_url)
            iframe = find_iframe_src(landing)
            body_url = to_body_url(iframe)
            body = fetch(body_url)
            out = outdir / f"{safe_name(name)}.html"
            out.write_text(body, encoding="utf-8")
            record.update(
                {
                    "status": "ok",
                    "landing_url": landing_url,
                    "body_url": body_url,
                    "html_path": str(out),
                    "chars": len(body),
                }
            )
        except Exception as exc:
            record["error"] = str(exc)
        records.append(record)
        time.sleep(args.delay)

    if meta_path:
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        with meta_path.open("a", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    ok = sum(1 for r in records if r["status"] == "ok")
    print(f"fetched {ok}/{len(records)} laws to {outdir}")


if __name__ == "__main__":
    main()
