# KOWRAP Decision Queue

Last updated: 2026-05-21

## Fixed Decisions

- Public project name: `KOWRAP`
- English name: Korean Wrapping and Rendering Analysis Project
- Korean name: 한국어 줄바꿈·렌더링 분석 프로젝트
- Public code/docs/project-authored synthetic examples license: Apache-2.0
- Initial repository: `msjang/kowrap`, private first
- First collaboration target: KONI / KISTI internal AI collaboration
- Initial data strategy: public legal text and synthetic examples before internal documents
- Project operating model: 3-file system plus ADRs
- Data boundary: public, restricted, private
- Research strategy: evidence and baselines before large ML

## Decisions the Project Owner Should Make Soon

These need owner judgment, institutional context, or public-facing responsibility.

1. Patent/public disclosure boundary

Decide what can be shown publicly before an invention disclosure is filed. Problem evidence and high-level benchmark plans are safe enough; exact scoring formulas, model compression, domain adaptation, and render-aware optimization loops should probably wait for IP review.

Recommended timing: before public demo, GitHub issue, or slide upload.

2. Internal data permission

Decide which internal HWP/HWPX/PDF documents can be used privately for evaluation, and whether any can be converted into synthetic public examples.

Recommended timing: before building the private benchmark or mounting data on the future GPU VM.

3. KISTI/KONI involvement detail

KONI is the first collaboration target. Decide whether it should be part of the first paper/patent plan, or held as a later domain-adaptation track.

Recommended timing: after baseline evidence, before ML phase.

4. Paper/patent priority

Decide whether the first serious external artifact should be a paper/workshop submission, an invention disclosure, or a standardization test-case proposal.

Recommended timing: after Phase 1 baseline report.

## Decisions Codex Can Make Autonomously

These can move forward without blocking on owner approval, as long as private data and public disclosure rules are respected.

1. Expand synthetic examples

Grow `examples/wrapping_failures.jsonl` from 10 to 20, then 50, then 100 public synthetic examples.

2. Write annotation guide

Create a human labeling guide for safe breaks, bad breaks, uncertain breaks, and renderer-specific notes.

3. Build schema validator

Add a small validator that checks JSONL validity, reconstructability of `/` break markers, source class, license note, and required fields.

4. Implement simple baselines

Start with whitespace-only, syllable-level, protected-domain-term, and rule-based candidate generation.

5. Draft renderer harness

Use open fonts and browser/PDF rendering to compare fixed-width paragraphs. HWPX-specific rendering can stay scoped until the boundary is clearer.

6. Draft W3C issue privately

Prepare a `klreq` issue draft with synthetic examples and evidence links, but do not publish it until disclosure and outreach decisions are made.

7. Prepare KrIGF core paragraph

Write the 1-paragraph problem statement and 1-slide evidence chain from the existing deck images.

8. Create repo hygiene files

Add `CONTRIBUTING.md`, issue templates, citation metadata, and model-card templates once a Git repository is initialized.

9. Build public legal-text corpus pipeline

Use the national law open API or public legal text sources to extract long Korean eojeol/compound candidates. Keep raw-source licensing notes separate from project-authored annotations.

## Default Autonomous Technical Choices

Unless overruled:

- Use TypeScript for browser-facing package and demo.
- Use Python for data preparation, benchmarking, and later ML experiments.
- Use JSONL as the first dataset format.
- Use open fonts for CI and public reproduction.
- Keep HWPX adapter read-only in v0.
- Keep public examples synthetic until explicit source licensing is known.
