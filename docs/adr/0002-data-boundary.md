# ADR 0002: Separate Public, Restricted, and Private Data

Date: 2026-05-21

Status: Accepted

## Context

KOWRAP needs realistic Korean document examples. The most valuable examples may come from internal reports, grant proposals, HWPX files, PDFs, and institution-specific terminology. These sources can contain personal data, confidential content, unpublished research plans, license-restricted fonts, or text that cannot be redistributed.

The project also needs public artifacts for open-source collaboration, papers, talks, and W3C issues.

## Decision

Classify all data as one of:

- Public
- Restricted
- Private

Public examples can be committed and redistributed. Restricted examples can be used internally or summarized, but raw text should not be released unless licensing is clear. Private examples must stay inside approved environments and must not be copied into public benchmark files, GitHub issues, papers, or slides without approval.

When a private example reveals an important layout failure, create a synthetic public equivalent that preserves the structural problem without exposing original content.

The operational policy lives in `docs/data-boundary.md`.

## Consequences

Benefits:

- The project can use realistic internal pain points without contaminating public assets.
- Paper and standardization work will have safer examples.
- Model versions can be labeled by distribution scope.

Costs:

- Some data preparation work will be slower.
- Public benchmarks may initially look smaller or more synthetic than internal benchmarks.
- Every imported example needs source and license notes.

## Review Trigger

Revisit this ADR before:

- publishing a dataset
- submitting a paper
- opening W3C issues with examples
- training an institution-specific model on private data
- mounting internal corpora on the future GPU VM

