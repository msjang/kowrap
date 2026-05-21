# ADR 0001: Use a 3-File Project System Plus ADRs

Date: 2026-05-21

Status: Accepted

## Context

KOWRAP is not only a code project. It has four coupled outputs: paper, patent, standardization, and open-source implementation. A normal issue tracker alone would lose the research narrative. A long research memo alone would hide the next executable tasks.

The maintainer is already comfortable with a Ryan Carson-style 3-file system and ADRs, so the project should use that familiarity instead of introducing a heavy project management framework.

## Decision

Use the following structure:

- `PROJECT.md`: stable project definition and research contract.
- `TASKS.md`: current atomic task list.
- `WORKFLOW.md`: process rules for sessions, evidence, data boundaries, model versions, and ADRs.
- `ROADMAP.md`: milestone and calendar view.
- `docs/adr/*.md`: durable architecture, process, data, model, licensing, and disclosure decisions.

ADRs are required when a decision affects public/private data boundaries, patent-sensitive disclosure, model export format, benchmark metrics, or standardization strategy.

## Consequences

Benefits:

- The project can move without waiting for a heavyweight management tool.
- Research claims, engineering tasks, and standardization work stay connected.
- Future collaborators can onboard by reading a small number of files.
- Decisions that matter will be recoverable later.

Costs:

- The files must be maintained manually.
- `TASKS.md` can become stale if it is not updated at the end of each session.
- More formal tooling may be needed later if multiple contributors join.

## Review Trigger

Revisit this ADR when:

- the repository has more than three active contributors
- external issues/PRs become the main workflow
- private training data requires stricter governance
- a paper submission deadline creates a separate writing workflow

