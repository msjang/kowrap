# Data Boundary Policy

Last updated: 2026-05-21

KOWRAP needs real document evidence, but the project must not accidentally publish private reports, personal data, internal policy material, or font assets with unclear licenses.

## Data Classes

## Public

Data that can be committed to a public repository, cited in papers, and shown in talks.

Examples:

- synthetic Korean compound-word examples
- public laws and regulations, if license terms permit
- derived candidate words from public legal text, with source and API/license notes
- public standards text excerpts within citation limits
- user-created minimal examples
- rendered screenshots from synthetic examples

Rules:

- Keep source URL or authorship note.
- Record license or usage basis.
- Use `Apache-2.0 project-authored` for examples authored inside KOWRAP.
- Prefer short minimal examples over long copied passages.

## Restricted

Data that can be used for internal experiments but should not be redistributed as raw text.

Examples:

- public PDFs with unclear extraction or redistribution rights
- bulk public legal text snapshots until redistribution rights and API terms are documented
- papers and reports where screenshots are acceptable for analysis but raw text release is not
- derived aggregate statistics from larger corpora

Rules:

- Do not commit raw source files unless redistribution is confirmed.
- Store derived features separately from source text when possible.
- Publish only aggregate metrics or synthetic equivalents.

## Private

Data that must not leave the institution, machine, or approved secure environment without permission.

Examples:

- internal HWP/HWPX reports
- grant proposals
- unpublished research plans
- documents with names, emails, budgets, project IDs, security-sensitive details
- licensed fonts not cleared for redistribution

Rules:

- Do not commit private text to public benchmark files.
- Do not paste private examples into public issues or standards discussions.
- Convert the pattern into a synthetic public equivalent.
- Keep private model versions clearly labeled, e.g. `kowrap-domain-KISTI-YYYYMM`.

## Synthetic Equivalent Pattern

When a private example reveals a useful failure pattern:

1. Remove all names, identifiers, project titles, numbers, and confidential nouns.
2. Replace domain-specific content with fictional but structurally similar Korean terms.
3. Preserve the key layout property:
   - long compound noun
   - numeric unit
   - punctuation
   - mixed Hangul/Latin
   - table width
   - font or renderer condition
4. Record that the public example is synthetic.

## Dataset Record Fields

Every dataset item should include:

- `id`
- `text`
- `source_class`: `public`, `restricted`, or `private`
- `source_note`
- `license_note`
- `domain`
- `renderer_context`
- `bad_breaks`
- `safe_breaks`
- `notes`

## Public Disclosure Rule

Before public release or W3C issue filing, check whether the material contains:

- exact private text
- personal data
- institution-only project names
- confidential budgets or schedules
- licensed font files
- patent-sensitive scoring formulas

If any item is present, rewrite into a synthetic example or hold it for internal use.

## Public Legal Text Workflow

For 법령-based candidate mining:

1. Use official public law data sources where possible.
2. Crawl or call APIs law-by-law rather than building an uncontrolled bulk mirror.
3. Extract only derived candidates at first:
   - long eojeols
   - candidate compounds
   - source law id/title
   - article/paragraph reference
   - extraction date
4. Put human labels and KOWRAP annotations under Apache-2.0 only when they are project-authored.
5. Keep raw full-text redistribution out of the public repo until the source terms are confirmed.
