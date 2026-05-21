# KOWRAP Workflow

Last updated: 2026-05-21

This project uses a modified Ryan Carson-style 3-file system plus ADRs.

## The Core Files

`PROJECT.md` is the project contract. It explains why the work exists, what is in scope, what is not in scope, and what evidence would prove success.

`TASKS.md` is the active work queue. Tasks should be small enough to finish in one focused session. If a task cannot be completed in one session, split it.

`WORKFLOW.md` is the operating manual. It explains how to make decisions, update documents, and avoid mixing paper, patent, standardization, and code work into one ambiguous pile.

`ROADMAP.md` is the calendar view. It is not the task tracker. Update it only when milestone timing or strategy changes.

`docs/adr/*.md` records decisions that should not be silently reversed.

## Session Start Protocol

At the beginning of a work session:

1. Read `PROJECT.md`.
2. Check the current phase in `ROADMAP.md`.
3. Pick one to three tasks from `TASKS.md`.
4. If the task changes architecture, data policy, model family, license, or public disclosure timing, write or update an ADR.
5. Define what artifact will prove the session succeeded.

## Session End Protocol

Before ending a work session:

1. Mark completed tasks in `TASKS.md`.
2. Add new follow-up tasks immediately.
3. Save generated evidence under a stable path.
4. Update `PROJECT.md` only if the definition changed.
5. Update `ROADMAP.md` only if schedule or milestones changed.
6. Add an ADR only for durable decisions.

## ADR Rules

Create an ADR when deciding:

- public vs private data boundary
- code license, data license, or font distribution policy
- model family or model export format
- HWPX/PDF/Web adapter boundary
- benchmark metric definition
- patent-sensitive public disclosure timing
- standardization strategy

Do not create ADRs for:

- typo fixes
- temporary implementation details
- one-off scripts
- task ordering

ADR states:

- `Proposed`
- `Accepted`
- `Superseded`
- `Rejected`

## Evidence Rules

Every visual evidence item should have:

- original source
- generated image path
- date generated
- rendering command or tool
- font and renderer if known
- observed problem
- expected better behavior

Evidence should be reproducible. A screenshot without input text and rendering context is useful for a talk, but weak for a paper or standard.

## Data Boundary Rules

Use three data classes:

- Public: can be published with repository and paper.
- Restricted: can be described statistically but not redistributed.
- Private: cannot leave the institution or machine without approval.

Never mix private examples into public benchmark files. If a private example teaches a pattern, create a synthetic public equivalent.

## Model Registry Rules

Every model version needs:

- model name
- training data class
- date
- algorithm family
- feature set
- evaluation results
- intended domain
- known failures
- distribution permission

Model APIs should stay stable even when implementation changes from rules to statistics to ML.

## Paper, Patent, Standard, Code Coupling

Code creates reproducible evidence.

Evidence supports paper claims.

Paper claims help decide what is novel.

Patent review happens before detailed novelty is disclosed.

Standardization receives implementation-neutral examples and tests, not hype.

## Weekly Rhythm

Weekly review:

- What evidence became stronger?
- What assumption failed?
- What task is blocking code?
- What task is blocking paper?
- What public disclosure needs IP review first?

Monthly review:

- Update `ROADMAP.md`.
- Archive or close stale tasks.
- Decide whether to write a new ADR.
- Produce one short progress note that can be shared with collaborators.

