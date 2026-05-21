# KOWRAP Tasks

Last updated: 2026-05-21

Status keys:

- `[ ]` not started
- `[~]` in progress
- `[x]` done
- `[!]` blocked or needs decision

## Done This Session

- [x] Render `2026_0518_krigf_partial.pdf` page 3 to `renders/krigf_p3-3.png`.
- [x] Render `2026_0518_krigf_partial.pdf` page 5 to `renders/krigf_p5-5.png`.
- [x] Create project definition and planning documents.
- [x] Add first ADR for the project operating system.
- [x] Create `docs/glossary.md` with Korean and English terms.
- [x] Create `docs/data-schema.md` for early JSONL examples.
- [x] Create `docs/data-boundary.md` for public/private/internal data handling.
- [x] Create `docs/evidence-pack.md` for rendered proof and future evidence items.
- [x] Create `examples/wrapping_failures.jsonl` with 10 synthetic seed examples.
- [x] Fix public project name: `KOWRAP`.
- [x] Fix English name: Korean Wrapping and Rendering Analysis Project.
- [x] Fix Korean name: 한국어 줄바꿈·렌더링 분석 프로젝트.
- [x] Fix public project license: Apache-2.0.
- [x] Create `docs/decision-queue.md` for owner decisions vs autonomous work.
- [x] Initialize local Git repository.
- [x] Set `origin` to private GitHub repo `https://github.com/msjang/kowrap.git`.
- [x] Set collaboration target priority: KONI first.
- [x] Set initial data strategy: public legal text and synthetic examples first.

## Next 72 Hours

- [ ] Expand `examples/wrapping_failures.jsonl` from 10 to 20 minimal examples.
- [ ] Extract text snippets from the KrIGF PDF examples into reusable test cases.
- [ ] Write one paragraph of the core problem statement for KrIGF slides.
- [ ] Draft but do not publish W3C `klreq` issue.
- [x] Create `docs/ip-open-source-strategy.md`.
- [x] Create `docs/corpus/legal-text-pipeline.md`.

## Evidence Pack

- [ ] Collect 10 HWP/HWPX examples where manual line breaks were inserted.
- [ ] Collect 10 Web/CSS examples where `keep-all` or syllable break produces bad layout.
- [ ] Collect 10 PDF examples where font or renderer changes shift Korean line breaks.
- [ ] For each example, record:
  - text
  - font
  - width
  - renderer
  - bad break location
  - expected better break location
  - screenshot path
- [ ] Define image naming convention for evidence artifacts.

## Data Schema

- [x] Draft JSONL schema for paragraph-level examples.
- [x] Add initial fields for `text`, `bad_breaks`, `safe_breaks`, `source_class`, `license_note`, and `domain`.
- [x] Define how to mark private/internal examples without exposing original text.
- [ ] Add character-offset fields after annotation tooling exists.
- [ ] Add renderer context fields to visual benchmark examples.
- [ ] Create annotation guide for human labelers.
- [x] Create synthetic examples for legal, science, policy, and report style.
- [ ] Define legal-text candidate extraction fields.

## Algorithms

- [ ] Implement baseline 1: keep existing whitespace only.
- [ ] Implement baseline 2: syllable-level break opportunities.
- [ ] Implement baseline 3: dictionary/domain-term protected spans.
- [ ] Implement baseline 4: morphology-based break opportunities.
- [ ] Implement baseline 5: PMI/branching-entropy score.
- [ ] Define combined score interface.
- [ ] Define model export format for future lightweight model versions.

## Renderer Harness

- [ ] Define fixed viewport widths for tests.
- [ ] Select open fonts that can be redistributed or installed in CI.
- [ ] Build browser rendering harness.
- [ ] Build PDF rendering harness.
- [ ] Decide how much HWPX rendering is in scope for v0.
- [ ] Define visual diff metrics.

## Open Source

- [x] Initialize Git repository.
- [x] Add private GitHub remote.
- [ ] Add package layout after language choice is decided.
- [x] Add `LICENSE` and `NOTICE`.
- [ ] Add contribution guide focused on examples and test cases.
- [ ] Add maintainer note for HWPX ecosystem collaborators.

## Paper

- [ ] Create literature review note for Korean layout, line breaking, hyphenation, and document rendering.
- [ ] Define paper contribution in one sentence.
- [ ] Select first target venue.
- [ ] Draft related-work table.
- [ ] Draft experiment table.
- [ ] Prepare paper skeleton after Phase 1 baseline results.

## Patent

- [ ] Create invention disclosure memo before publishing detailed scoring formulas.
- [ ] Separate public demo material from claim-sensitive material.
- [ ] List prior art:
  - TeX/Knuth-Liang hyphenation
  - Unicode line breaking
  - W3C `klreq`
  - browser `word-break` behavior
  - phrase break tools
  - HWP/HWPX rendering behavior
- [ ] Draft claim sketches with counsel or institutional IP office.

## Standardization

- [ ] Open or draft a W3C `klreq` GitHub issue with minimal examples.
- [ ] Convert evidence into implementation-neutral requirements.
- [ ] Propose terminology for Korean compound-word break opportunity.
- [ ] Propose test cases before proposing normative text.
- [ ] Track external feedback in ADRs or decision notes.

## GPU VM Preparation

- [ ] Record expected Ubuntu 24.04 environment.
- [ ] Define Python/Node/Rust requirements after implementation stack is chosen.
- [ ] Prepare reproducible setup script.
- [ ] Prepare small CPU-only smoke test before GPU training.
- [ ] Decide whether any private corpus may be mounted on the VM.
