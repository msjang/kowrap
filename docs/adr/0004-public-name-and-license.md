# ADR 0004: Public Name and License

Date: 2026-05-21

Status: Accepted

## Context

The project needs a stable public name before opening a repository, talking with maintainers, filing issues, preparing KrIGF material, or writing paper/patent notes. It also needs a clear license so collaborators can evaluate whether they can use or contribute to the code.

## Decision

Use `KOWRAP` as the public project name.

- English expansion: Korean Wrapping and Rendering Analysis Project
- Korean expansion: 한국어 줄바꿈·렌더링 분석 프로젝트
- CLI/package name: `kowrap`
- Repository name candidate: `kowrap`

Use Apache-2.0 for public code, documentation, and project-authored synthetic examples.

Third-party, restricted, and private data are not automatically covered by this project license. They keep their original source license and disclosure boundary as described in `docs/data-boundary.md`.

## Consequences

Benefits:

- The name is short and directly tied to Korean wrapping.
- The Korean and English names are clear enough for papers, slides, GitHub, and standards discussions.
- Apache-2.0 is friendly to open-source adoption and includes an explicit patent grant.

Costs:

- `KOWRAP` is descriptive but not fully self-explanatory without the expansion.
- Future public datasets may still need separate dataset-specific license decisions.

## Review Trigger

Revisit this ADR only if:

- the repository name is unavailable
- institutional policy requires another license
- a public dataset release needs a data-specific license

