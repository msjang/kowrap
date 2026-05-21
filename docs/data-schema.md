# KOWRAP Dataset Schema

Last updated: 2026-05-21

This schema is for early Korean line-break examples. It is intentionally simple so the benchmark can start before the final model design is known.

## File Format

Use JSON Lines:

- one UTF-8 JSON object per line
- no trailing commas
- file extension: `.jsonl`

Current seed file:

- `examples/wrapping_failures.jsonl`

## Required Fields

`id`

Stable unique identifier. Use prefixes such as `synthetic-`, `public-`, `restricted-`, or `private-`.

`source_class`

One of:

- `public`
- `restricted`
- `private`

See `docs/data-boundary.md`.

`source_note`

Short human-readable source description.

`license_note`

License or usage note. For synthetic examples created in this project, use `Apache-2.0 project-authored`.

`domain`

Document or language domain. Examples:

- `research_admin`
- `policy`
- `document_automation`
- `science`
- `legal_admin`
- `standardization`
- `rendering`
- `mlops`
- `benchmark`
- `typography`

`text`

Original paragraph or sentence to evaluate.

`bad_breaks`

Array of strings marking bad break positions with `/`.

Example:

```json
["국가연구개발사업성과평가체/계"]
```

`safe_breaks`

Array of strings marking acceptable or preferred break positions with `/`.

Example:

```json
["국가연구개발사업/성과평가체계"]
```

`notes`

Short explanation of why the example matters.

## Optional Fields

`renderer_context`

Object describing visual test conditions.

```json
{
  "renderer": "chromium",
  "font": "Noto Sans CJK KR",
  "width_px": 320,
  "line_height": 1.6,
  "justification": "none"
}
```

`safe_break_indices`

Character offsets for preferred break positions. Add this once annotation tooling exists.

`bad_break_indices`

Character offsets for bad break positions. Add this once annotation tooling exists.

`screenshot_path`

Path to visual evidence.

`model_expectations`

Object for future tests where a model should protect or prefer certain spans.

## Validation Rules

- `text` must not contain private or restricted content if `source_class` is `public`.
- Every item must have at least one `bad_breaks` or `safe_breaks` entry.
- Slashed break examples must be reconstructable into a substring of `text` after removing `/`.
- Synthetic examples should be structurally realistic but not copied from private documents.
