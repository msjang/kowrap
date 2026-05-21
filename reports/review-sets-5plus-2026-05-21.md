# 5+ Review Sets: 2026-05-21

## Purpose

This pass lowers candidate extraction from 8+ Hangul characters to 5+ Hangul
characters. The goal is to label short high-frequency terms first, then use
those labels as protected units for longer compound break scoring.

Separators such as `·`, `ㆍ`, `_`, and `-` remain token boundaries.

## Candidate Files

Generated outside the repository:

- `~/kowrap/data/processed/candidates/msit_candidates_5plus.jsonl`
- `~/kowrap/data/processed/candidates/evaluation_candidates_5plus.jsonl`
- `~/kowrap/data/processed/candidates/law_seed_candidates_5plus.jsonl`

Counts:

- MSIT: 5,131
- evaluation.go.kr: 23,174
- law seed: 5,264
- raw total: 33,569
- merged unique candidates: 31,671

Merged unique length distribution:

- 5-8 Hangul chars: 28,822
- 9-11 Hangul chars: 2,259
- 12-15 Hangul chars: 474
- 16-19 Hangul chars: 95
- 20+ Hangul chars: 21

## Review Sets

`review_core_5plus_top_500.tsv`

- Purpose: label short high-frequency terms first.
- Selection: 5+ Hangul chars, deduplicated, short-first then count.
- Result: 500 rows, all length 5.
- Use for: protected span seed terms and simple break/no-break examples.

`review_long_12plus_top_500.tsv`

- Purpose: keep the long compound benchmark visible.
- Selection: 12+ Hangul chars, deduplicated, long-first then count.
- Result: 500 rows, length 12-29.
- Use for: paper examples, renderer stress tests, and long-compound scoring.

`review_train_seed_500.tsv`

- Purpose: balanced first training/evaluation seed.
- Selection:
  - 5-8 chars: 200 rows
  - 9-15 chars: 200 rows
  - 16+ chars: 100 rows
- Use for: the first scoring baseline after human labels exist.

`lexicon_seed_5to8_top_500.tsv`

- Purpose: draft protected-term lexicon.
- Selection: 5-8 chars, deduplicated, count-first then short.
- Use for: human review of terms that should usually be kept intact.

## Validation

For the three review TSV files, the top 100 rows were checked as direct matches
against their `context_path` text files.

Results:

- `review_core_5plus_top_500.tsv`: 0 direct-match misses
- `review_long_12plus_top_500.tsv`: 0 direct-match misses
- `review_train_seed_500.tsv`: 0 direct-match misses

## Recommended Next Step

Start labeling `review_train_seed_500.tsv`, not the pure core or pure long set.
The train seed has enough short candidates to learn protected units and enough
long candidates to keep the real KOWRAP problem in scope.

After 100-200 rows are reviewed:

1. Export reviewed rows with `scripts/kowrap_export_review_labels.py`.
2. Generate a protected-span dictionary from reviewed short terms.
3. Implement baseline scoring against `preferred_breaks`, `acceptable_breaks`,
   `protected_spans`, and `bad_breaks`.

