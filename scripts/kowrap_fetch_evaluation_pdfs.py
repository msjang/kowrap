#!/usr/bin/env python3
"""Download PDF files referenced by evaluation.go.kr ebookView pages."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen


BASE = "https://www.evaluation.go.kr"
UA = "Mozilla/5.0 KOWRAP/0.1"


def fetch_bytes(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=60) as resp:
        return resp.read()


def fetch_text(url: str) -> str:
    return fetch_bytes(url).decode("utf-8", errors="replace")


def parse_ebook_links(menu_html: str) -> list[dict]:
    pattern = re.compile(
        r'href="([^"]*ebookView\.do\?atchId=(\d+)&fileSn=(\d+))"[^>]*>([^<]+)</a>'
    )
    seen = set()
    rows = []
    for href, atch_id, file_sn, label in pattern.findall(menu_html):
        key = (atch_id, file_sn)
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "atch_id": atch_id,
                "file_sn": file_sn,
                "label": re.sub(r"\s+", " ", label).strip(),
                "ebook_url": urljoin(BASE, href),
            }
        )
    return rows


def parse_pdf_url(ebook_html: str) -> str | None:
    match = re.search(r'PDFObject\.embed\("([^"]+\.pdf)"', ebook_html)
    if match:
        return urljoin(BASE, match.group(1))
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--menu-url", default=f"{BASE}/web/page.do?menu_id=139")
    parser.add_argument("--menu-html")
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()

    if args.menu_html:
        menu_html = Path(args.menu_html).expanduser().read_text(encoding="utf-8", errors="replace")
    else:
        menu_html = fetch_text(args.menu_url)

    links = parse_ebook_links(menu_html)
    selected = links[args.offset : args.offset + args.limit]

    outdir = Path(args.outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)
    meta_path = Path(args.metadata).expanduser()
    meta_path.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for row in selected:
        record = dict(row)
        record["status"] = "error"
        try:
            ebook_html = fetch_text(row["ebook_url"])
            pdf_url = parse_pdf_url(ebook_html)
            if not pdf_url:
                raise RuntimeError("PDFObject.embed URL not found")
            out = outdir / f"evaluation-{row['atch_id']}-{row['file_sn']}.pdf"
            if not out.exists() or out.stat().st_size == 0:
                out.write_bytes(fetch_bytes(pdf_url))
            if out.stat().st_size < 1000:
                raise RuntimeError(f"download too small: {out.stat().st_size}")
            record.update(
                {
                    "status": "ok",
                    "pdf_url": pdf_url,
                    "pdf_path": str(out),
                    "bytes": out.stat().st_size,
                }
            )
        except Exception as exc:
            record["error"] = str(exc)
        records.append(record)
        time.sleep(args.delay)

    with meta_path.open("a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    ok = sum(1 for r in records if r["status"] == "ok")
    print(f"downloaded {ok}/{len(records)} PDFs to {outdir}")


if __name__ == "__main__":
    main()

