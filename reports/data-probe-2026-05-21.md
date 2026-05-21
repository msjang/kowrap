# Data Probe: 2026-05-21

## Workspace

Bulk data is stored outside the synced project directory:

- `~/kowrap`

Repository scripts live in:

- `scripts/kowrap_fetch_law.py`
- `scripts/kowrap_extract_text.py`
- `scripts/kowrap_extract_candidates.py`
- `scripts/kowrap_fetch_evaluation_pdfs.py`
- `scripts/kowrap_build_review_set.py`
- `scripts/kowrap_export_review_labels.py`

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
- expanded to pages 2-3; 19 additional HWP/HWPX/ODT sets were saved
- extracted text from 49 HWPX and ODT files
- generated `~/kowrap/data/processed/candidates/msit_candidates.jsonl`

Candidate count:

- 325

## Evaluation.go.kr

Source:

- `https://www.evaluation.go.kr/web/page.do?menu_id=139`

Observed:

- 918 `ebookView.do?atchId=...&fileSn=1` links were found in the page HTML.
- Each sampled ebook page embeds a direct PDF path such as `/upload2/atch/eval/20250508092501161.pdf`.

Sample:

- raw PDF: `~/kowrap/data/raw/evaluation/sample_4567.pdf`
- text: `~/kowrap/data/processed/text/evaluation_4567.txt`
- candidates: `~/kowrap/data/processed/candidates/evaluation_candidates.jsonl`

Batch expansion:

- downloaded 20/20 PDFs from the menu page into `~/kowrap/data/raw/evaluation/pdfs`
- extracted 20/20 PDFs into `~/kowrap/data/processed/text/evaluation_batch`
- extracted text line count: 123,721 total lines

Candidate count after batch expansion:

- 1,160

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

- `~/kowrap/data/processed/candidates/review_context_top_500.tsv`
- `~/kowrap/data/processed/candidates/review_context_top_500.jsonl`

Columns:

- `review_id`
- `candidate`
- `stem_guess`
- `suffix_guess`
- `type_guess`
- `domain`
- `hangul_len`
- `count`
- `context`
- `context_path`
- `source_paths`
- `protected_spans`
- `preferred_breaks`
- `acceptable_breaks`
- `bad_breaks`
- `label_status`
- `review_note`

Review-set distribution:

- law: 293 rows
- evaluation: 137 rows
- msit: 70 rows

Type-hint distribution:

- compound: 472 rows
- law-title: 14 rows
- agency-list: 11 rows
- enumeration: 3 rows

This is the current best human-in-the-loop entry point. Labeling instructions are
in `docs/annotation-guide.md`.

Export:

- `scripts/kowrap_export_review_labels.py` converts reviewed TSV rows to JSONL.
- Current export has 0 rows because all generated labels remain `todo`.
- `examples/review_labels_synthetic.tsv` and `.jsonl` provide a small checked-in
  fixture for the label format.

## Next Improvements

- Improve type hints for source-extraction enumerations and collapsed bullet lists.
- Add scoring fields for preferred, acceptable, and protected break candidates.
- Crawl more MSIT pages after confirming rate limits.
- Crawl more evaluation.go.kr PDFs by metadata, not blindly.
