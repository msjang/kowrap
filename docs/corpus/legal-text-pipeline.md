# Public Legal Text Corpus Pipeline

Last updated: 2026-05-21

## Goal

Use public Korean legal text to discover long eojeols and compound candidates for KOWRAP annotation and benchmark construction.

The first target is not to redistribute a full legal corpus. The first target is to extract candidate strings, source references, and human labels.

## Why Legal Text

Legal and administrative writing contains many long formal compounds, fixed expressions, mixed numeric references, and narrow-layout citation patterns. It is a strong first public-domain-style stress source for Korean line breaking.

Examples of useful patterns:

- long compounds
- agency and committee names
- law/article/paragraph references
- mixed Hangul, Latin, numbers, and punctuation
- repeated formal endings

## Source Preference

Prefer official sources:

- 국가법령정보 공동활용 LAW OPEN DATA
- 국가법령정보센터

The open API guide documents law search APIs and result fields such as law id, title, ministry, promulgation date, enforcement date, and detail links.

Current note: the sample `OC=test` API key can fail with IP/domain validation. KOWRAP therefore also supports a no-key fallback for named laws: `https://www.law.go.kr/법령/{법령명}` is opened, the `lawService` iframe is followed, and the body HTML is fetched via `lsInfoR.do`.

## Phase 1: Candidate Mining

For each law:

1. Fetch metadata.
2. Fetch body text if allowed by API terms.
3. Normalize whitespace and punctuation conservatively.
4. Split into eojeols.
5. Extract candidates:
   - Hangul eojeols longer than a threshold, e.g. 8 syllables
   - mixed Hangul/Latin/number eojeols
   - repeated compounds across laws
   - terms with high internal branching uncertainty
6. Store source reference:
   - source URL or API endpoint
   - law id
   - law title
   - article/paragraph if available
   - extraction date
7. Do not publish raw full text until redistribution terms are confirmed.

## Phase 2: Human-in-the-Loop Labeling

For each candidate:

1. Show the source sentence or short local context.
2. Ask the human labeler to mark:
   - safe break positions
   - bad break positions
   - protected spans
   - uncertain positions
3. Save only the minimal context needed for the benchmark.
4. Convert useful private or restricted patterns into synthetic public examples.

## Phase 3: Benchmark Split

Use three splits:

- `public-synthetic`: project-authored examples under Apache-2.0
- `public-derived`: labels and derived candidates from public legal text, with source references
- `restricted-raw`: local raw legal text cache if API/source terms do not permit redistribution

## Initial JSONL Candidate Fields

```json
{
  "id": "law-candidate-000001",
  "source_class": "restricted",
  "source_note": "National law text candidate; raw redistribution not yet cleared",
  "license_note": "source terms pending; KOWRAP labels Apache-2.0 project-authored",
  "domain": "legal",
  "law_id": "",
  "law_title": "",
  "article": "",
  "extraction_date": "2026-05-21",
  "candidate": "",
  "context": "",
  "bad_breaks": [],
  "safe_breaks": [],
  "notes": ""
}
```

## API Notes

The national law open-data guide lists request parameters for law search, including `target=law`, output types such as HTML/XML/JSON, search range, query, result count, sorting, ministry, and law kind.

The API sign-up page notes that an API key is used as the `OC` request parameter. It also warns that excessive short-interval calls can be treated as abnormal access and restricted.

## Crawler Discipline

- Use API first, browser scraping last.
- Cache politely.
- Rate limit.
- Store raw cache outside public repository until terms are clear.
- Keep derived labels separate from raw source text.
- Record extraction date and source link.

## Current Seed Run

Seed list:

- `data/legal_seed_laws.txt`

External outputs:

- raw HTML: `~/kowrap/data/raw/law/seed_laws`
- extracted text: `~/kowrap/data/processed/text/law_seed`
- candidates: `~/kowrap/data/processed/candidates/law_seed_candidates.jsonl`
- review sheet: `~/kowrap/data/processed/candidates/review_top_200.tsv`

As of 2026-05-21, the seed run fetched 15/15 laws and produced 1,000 ranked legal candidates after filtering obvious 조문번호-style noise.
