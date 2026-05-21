#!/usr/bin/env python3
"""Extract plain text from KOWRAP source documents."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import tempfile
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET


class TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in {"script", "style"}:
            self.skip_depth += 1
        if tag.lower() in {"p", "br", "div", "li", "tr", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
        if tag.lower() in {"p", "div", "li", "tr", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def xml_text(data: bytes) -> str:
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return ""
    parts: list[str] = []
    for elem in root.iter():
        if elem.text:
            parts.append(elem.text)
        if elem.tail:
            parts.append(elem.tail)
    return " ".join(parts)


def extract_zip_xml(path: Path, member_patterns: tuple[str, ...]) -> str:
    parts: list[str] = []
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".xml"):
                continue
            if member_patterns and not any(re.search(pattern, name) for pattern in member_patterns):
                continue
            parts.append(xml_text(zf.read(name)))
    return "\n".join(parts)


def extract_pdf(path: Path) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out.txt"
        subprocess.run(
            ["pdftotext", "-layout", str(path), str(out)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return out.read_text(encoding="utf-8", errors="replace")


def extract_html(path: Path) -> str:
    parser = TextHTMLParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser.text()


def extract_one(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".hwpx":
        return extract_zip_xml(path, (r"^Contents/.*\.xml$", r"^Preview/.*\.xml$"))
    if suffix == ".odt":
        return extract_zip_xml(path, (r"^content\.xml$",))
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in {".html", ".htm"}:
        return extract_html(path)
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="replace")
    raise ValueError(f"unsupported file type: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Input files")
    parser.add_argument("--outdir", required=True, help="Directory for extracted .txt files")
    parser.add_argument("--metadata", help="Optional JSONL metadata output")
    args = parser.parse_args()

    outdir = Path(args.outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)
    meta_path = Path(args.metadata).expanduser() if args.metadata else None

    records = []
    for raw in args.inputs:
        path = Path(raw).expanduser()
        if not path.exists() or path.is_dir():
            continue
        try:
            text = clean_text(extract_one(path))
        except Exception as exc:
            records.append({"source_path": str(path), "status": "error", "error": str(exc)})
            continue

        out = outdir / f"{path.name}.txt"
        out.write_text(text, encoding="utf-8")
        records.append(
            {
                "source_path": str(path),
                "text_path": str(out),
                "status": "ok",
                "chars": len(text),
            }
        )

    if meta_path:
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        with meta_path.open("a", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    ok = sum(1 for r in records if r["status"] == "ok")
    print(f"extracted {ok}/{len(records)} files to {outdir}")


if __name__ == "__main__":
    main()
