# KOWRAP Roadmap

Last updated: 2026-05-21

This roadmap assumes the KrIGF presentation date visible in the local deck is 2026-07-02.

## Strategy

The project should not start as a large ML project. It should start as a reproducible evidence and benchmark project, then grow into algorithms, model distillation, patent claims, and standards text.

Priority order:

1. Make the problem undeniable with screenshots, metrics, and failing examples.
2. Define the data schema and evaluation before optimizing algorithms.
3. Ship a small open-source baseline that other maintainers can run.
4. Add model versions only after rule/statistical baselines are measurable.
5. Use the code and benchmark as the spine for paper, patent, and standardization.

## Phase 0: Project Skeleton and Evidence Pack

Target: 2026-05-21 to 2026-06-02

Deliverables:

- Project documents: `PROJECT.md`, `ROADMAP.md`, `TASKS.md`, `WORKFLOW.md`, first ADR.
- Rendered evidence from `2026_0518_krigf_partial.pdf` pages 3 and 5.
- 20 to 50 minimal failing Korean wrapping examples.
- Initial glossary: break opportunity, bad break, compound noun, renderer stability, model card.
- Public/private data boundary memo.

Exit criteria:

- A maintainer or researcher can understand the project in 10 minutes.
- Each evidence item has input text, expected issue, renderer/font context, and image output.

## Phase 1: Baselines and Data Schema

Target: 2026-06-03 to 2026-06-23

Deliverables:

- JSONL annotation schema for Korean break opportunities.
- Gold annotation guide for human labeling.
- Baseline implementations:
  - keep-all
  - syllable break
  - morpheme analyzer heuristic
  - PMI/branching entropy statistical score
- Renderer harness plan for Web/PDF/HWPX comparison.
- First benchmark report using at least 100 examples.

Exit criteria:

- Every algorithm can be evaluated on the same input/output schema.
- Benchmark failure cases can be rendered as images.

## Phase 2: KrIGF Demo and Public Narrative

Target: 2026-06-24 to 2026-07-02

Deliverables:

- KrIGF demo page or notebook showing the same paragraph under multiple wrapping strategies.
- One-slide evidence chain:
  - manual HWP work
  - renderer inconsistency
  - missing Korean compound-word break model
  - proposed open benchmark and reference implementation
- Maintainer-facing README for HWPX/open-source collaborators.
- Draft W3C `klreq` GitHub issue with concrete examples.

Exit criteria:

- The talk can end with a concrete call to action: examples, issues, datasets, and collaborators.

## Phase 3: Prototype Library

Target: 2026-07-03 to 2026-08-31

Deliverables:

- `kowrap` CLI prototype.
- JavaScript package for browser demo.
- Python package or script for dataset and benchmark generation.
- Model registry layout:
  - rule model
  - statistical model
  - domain override dictionary
- Visual regression tests with fixed fonts and viewport widths.

Exit criteria:

- The library can process a paragraph and output ranked break candidates.
- The browser demo can compare baseline vs KOWRAP visually.
- Results are reproducible on a clean Ubuntu 24.04 VM.

## Phase 4: Paper and Patent Drafting

Target: 2026-09-01 to 2026-11-30

Deliverables:

- Paper outline:
  - motivation
  - Korean layout gap
  - dataset
  - algorithms
  - renderer-aware evaluation
  - open-source implementation
- Invention disclosure:
  - problem
  - prior art
  - novelty
  - embodiments
  - claim sketches
- Expanded benchmark with public and private partitions.
- Ablation study:
  - morphology only
  - statistics only
  - combined score
  - domain dictionary
  - render-aware penalty

Exit criteria:

- The project has one conservative, defensible paper target and one ambitious backup.
- Patent claims are reviewed before public disclosure of the exact inventive mechanism.

## Phase 5: Model Distillation and Domain Adaptation

Target: 2026-12-01 to 2027-03-31

Deliverables:

- Lightweight trainable model.
- Model card template and version registry.
- Institution-specific fine-tuning workflow that does not leak private text.
- GPU VM training runbook for Ubuntu 24.04.
- Evaluation report comparing model families.

Exit criteria:

- A domain model can be trained, evaluated, exported, and replaced without changing the application API.

## Phase 6: Standardization and Maintainer Adoption

Target: 2027-04-01 to 2027-06-30

Deliverables:

- W3C `klreq` issue/PR set:
  - terminology update
  - compound-word line-break examples
  - renderer test cases
  - reference implementation link
- Open-source maintainer guide.
- Public benchmark release if licensing permits.
- Final paper submission or workshop submission.

Exit criteria:

- The project is no longer only a personal research idea; it has a test suite, external feedback, and a path into standards discussion.

## Recommended Publication Targets

Conservative first targets:

- ACM DocEng
- W3C/i18n or Web typography related workshops
- ACL/EMNLP workshop tracks on NLP for document processing or language resources
- CHI/UIST late-breaking or workshop track if the manual editing burden is measured with users

Ambitious later targets:

- The Web Conference
- CHI/UIST full paper, if user study and interaction design become strong
- Top-tier ML venues only if the model/distillation method becomes the primary contribution rather than the application layer

## Patent Timing

Patent review should happen before publishing the exact algorithmic combination if the intended claim is more than a dataset or benchmark. Safe public material before patent review:

- Problem statement
- Renderer inconsistency examples
- General need for Korean compound-word break opportunities
- High-level benchmark plan

Material to hold until review:

- Exact scoring formula
- Model compression mechanism
- Domain adaptation method
- Render-aware optimization loop

