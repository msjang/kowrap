# KOWRAP

KOWRAP is the public project name for the **Korean Wrapping and Rendering Analysis Project**.

한글 풀네임은 **한국어 줄바꿈·렌더링 분석 프로젝트**입니다.

KOWRAP focuses on long Korean compound words, HWPX/PDF/Web rendering differences, and reproducible typography automation.

## License

Public code, documentation, and project-authored synthetic examples are licensed under Apache-2.0. Third-party, restricted, or private data keeps its original license and disclosure boundary.

## Start Here

- [PROJECT.md](PROJECT.md): project definition, scope, claims, outputs, risks.
- [ROADMAP.md](ROADMAP.md): phased plan across paper, patent, standardization, and code.
- [TASKS.md](TASKS.md): current atomic task list.
- [WORKFLOW.md](WORKFLOW.md): how to run the project day to day.
- [docs/break-selection.md](docs/break-selection.md): semantic and renderer-aware candidate selection.
- [docs/glossary.md](docs/glossary.md): shared Korean/English terminology.
- [docs/data-schema.md](docs/data-schema.md): JSONL schema for early examples and benchmarks.
- [docs/data-boundary.md](docs/data-boundary.md): public, restricted, and private data rules.
- [docs/decision-queue.md](docs/decision-queue.md): owner decisions vs autonomous tasks.
- [docs/evidence-pack.md](docs/evidence-pack.md): rendered evidence and evidence template.
- [docs/ip-open-source-strategy.md](docs/ip-open-source-strategy.md): Apache-2.0 and institutional IP strategy note.
- [docs/corpus/legal-text-pipeline.md](docs/corpus/legal-text-pipeline.md): public legal text mining workflow.
- [reports/data-probe-2026-05-21.md](reports/data-probe-2026-05-21.md): first MSIT/evaluation/law data probe.
- [docs/adr/0001-project-operating-system.md](docs/adr/0001-project-operating-system.md): first architecture/process decision.
- [docs/adr/0002-data-boundary.md](docs/adr/0002-data-boundary.md): data disclosure boundary decision.
- [docs/adr/0003-evidence-first-before-ml.md](docs/adr/0003-evidence-first-before-ml.md): evidence-first research strategy.
- [docs/adr/0004-public-name-and-license.md](docs/adr/0004-public-name-and-license.md): public name and Apache-2.0 license decision.

## Local Evidence

Rendered images from `2026_0518_krigf_partial.pdf`:

- [renders/krigf_p3-3.png](renders/krigf_p3-3.png)
- [renders/krigf_p5-5.png](renders/krigf_p5-5.png)

## Seed Dataset

- [examples/wrapping_failures.jsonl](examples/wrapping_failures.jsonl): synthetic public examples for early schema and benchmark work.

## Data Workspace

Bulk crawled and extracted data lives outside this repository at `~/kowrap`.
