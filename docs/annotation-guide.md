# KOWRAP Annotation Guide

This guide defines the first human-in-the-loop format for Korean break candidates.

## Review File

Current review set:

- `~/kowrap/data/processed/candidates/review_context_top_500.tsv`

Checked-in format fixture:

- `examples/review_labels_synthetic.tsv`
- `examples/review_labels_synthetic.jsonl`

The file is generated from public or externally downloaded source text, but it is
kept outside this repository until source terms are reviewed. The KOWRAP labels
created by project contributors are intended to be project-authored Apache-2.0
data.

## Tokenization Policy

`candidate` is a surface token observed in extracted text. Separators such as
`·`, `ㆍ`, `_`, and `-` are token boundaries. They must not be deleted to create a
longer candidate.

If a row exists only because document extraction collapsed spaces across a table
cell or sentence, mark `label_status` as `skip` or `needs-discussion`.

## Columns To Edit

Annotators should only edit these columns:

- `protected_spans`
- `preferred_breaks`
- `acceptable_breaks`
- `bad_breaks`
- `label_status`
- `review_note`

All other columns are generated evidence and should be treated as read-only.

## Break Marking

Use `/` inside the candidate string to mark a break opportunity.

Example:

```text
국가인적자원개발/컨소시엄/지원
```

Use `;` to record multiple alternatives if needed.

Example:

```text
국가인적자원개발/컨소시엄지원;국가인적자원개발컨소시엄/지원
```

## Label Semantics

`protected_spans` marks text that should normally stay unbroken.

```text
국가인적자원개발;컨소시엄
```

`preferred_breaks` marks the best break positions for narrow layout.

```text
국가인적자원개발/컨소시엄/지원
```

`acceptable_breaks` marks tolerable but less ideal break positions.

```text
국가인적자원개발컨소시엄/지원
```

`bad_breaks` marks visually or semantically bad break positions.

```text
국가인적/자원개발컨소시엄지원
```

`label_status` should be one of:

- `todo`
- `reviewed`
- `skip`
- `needs-discussion`

## Candidate Types

The generated `type_guess` is only a hint.

- `compound`: likely policy, law, science, or organization compound.
- `law-title`: legal title or legal title with trailing particle.
- `agency-list`: ministry, committee, government body, or institution list.
- `enumeration`: list-like token collapsed by source extraction.
- `article-reference`: legal article or clause reference noise.
- `noisy-extraction`: likely spacing loss from PDF/HWPX extraction.

For `agency-list` and `enumeration`, good labels often preserve each named unit
and place breaks at list boundaries. For `law-title`, the title itself is usually
a protected span, while a trailing particle can be split out in downstream
normalization.

## First Pass Goal

For the first 500-row file, aim for:

- 100 high-confidence `compound` labels.
- 30 `law-title` labels.
- 30 `agency-list` or `enumeration` labels.
- A short note on any extraction noise pattern that appears repeatedly.

## Export

After rows are marked `reviewed`, export labels with:

```sh
python3 scripts/kowrap_export_review_labels.py \
  ~/kowrap/data/processed/candidates/review_context_top_500.tsv \
  --out ~/kowrap/data/processed/labels/reviewed_labels.jsonl
```

The exporter validates that each slash-marked break string becomes the original
candidate after `/` is removed.
