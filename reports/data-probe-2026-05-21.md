# Data Probe: 2026-05-21

## Workspace

Bulk data is stored outside the synced project directory:

- `~/kowrap`

Repository scripts live in:

- `scripts/kowrap_fetch_law.py`
- `scripts/kowrap_extract_text.py`
- `scripts/kowrap_extract_candidates.py`

## Sources Probed

## MSIT

Tool:

- `~/kowrap/tools/msit-dl`

Command:

```sh
python3 ~/kowrap/tools/msit-dl/msit_dl.py --pages 1 --outdir ~/kowrap/data/raw/msit --delay 0.5
```

Result:

- downloaded recent MSIT page-1 HWP/HWPX/ODT attachments
- extracted text from HWPX and ODT files
- generated `~/kowrap/data/processed/candidates/msit_candidates.jsonl`

Candidate count:

- 146

## Evaluation.go.kr

Source:

- `https://www.evaluation.go.kr/web/page.do?menu_id=139`

Observed:

- 918 `ebookView.do?atchId=...&fileSn=1` links were found in the page HTML.
- Each sampled ebook page embeds a direct PDF path such as `/upload2/atch/eval/20250508092501161.pdf`.

Sample:

- raw PDF: `~/kowrap/data/raw/evaluation/sample_4567.pdf`
- text: `~/kowrap/data/processed/text/evaluation/sample_4567.pdf.txt`
- candidates: `~/kowrap/data/processed/candidates/evaluation_candidates.jsonl`

Candidate count:

- 260

Usefulness:

- Good for policy/report-style long compounds.
- PDF text extraction works with `pdftotext -layout`.
- Full crawl is likely useful but should be rate-limited and metadata-driven.

## Law.go.kr

API finding:

- The official API guide is reachable, but `OC=test` failed with IP/domain validation in this environment.

Fallback:

- Open `https://www.law.go.kr/법령/{법령명}`.
- Follow the `lawService` iframe.
- Convert `lsInfoP.do` to `lsInfoR.do` to fetch body HTML.

Seed list:

- `data/legal_seed_laws.txt`

Result:

- fetched 15/15 seed laws
- extracted text from law body HTML
- generated `~/kowrap/data/processed/candidates/law_seed_candidates.jsonl`

Candidate count:

- 1,000, capped by `--top 1000`

Usefulness:

- Strong source for long formal legal and policy compounds.
- Needs filtering for enumerations, agency lists, and suffix particles.

## Combined Review Sheet

Created:

- `~/kowrap/data/processed/candidates/review_top_200.tsv`

Columns:

- `candidate`
- `domain`
- `hangul_len`
- `count`
- `source_paths`
- `safe_breaks`
- `bad_breaks`
- `review_note`

This is the current best human-in-the-loop entry point.

## Next Improvements

- Add context sentence around each candidate.
- Normalize trailing particles such as `이`, `은`, `을`, `중` into a separate field.
- Add candidate type tags:
  - compound
  - agency-list
  - law-title
  - article-reference
  - enumeration
  - noisy-extraction
- Add direct TSV-to-JSONL labeling conversion.
- Crawl more MSIT pages after confirming rate limits.
- Crawl more evaluation.go.kr PDFs by metadata, not blindly.

