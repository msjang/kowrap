# Evidence Pack

Last updated: 2026-05-21

## Local Rendered Evidence

Source file:

- `2026_0518_krigf_partial.pdf`

Rendered images:

- `renders/krigf_p3-3.png`
- `renders/krigf_p5-5.png`

Rendering commands:

```sh
pdftoppm -f 3 -l 3 -png -r 200 2026_0518_krigf_partial.pdf renders/krigf_p3
pdftoppm -f 5 -l 5 -png -r 200 2026_0518_krigf_partial.pdf renders/krigf_p5
```

PDF metadata observed locally:

- Producer: macOS 15.0 Quartz PDFContext
- Creation date: 2026-05-21 12:01:16 KST
- Pages: 7
- Page size: 960 x 540 pt

## Evidence 001: Missing Korean Compound-Word Break Model

Image:

- `renders/krigf_p3-3.png`

Observed problem:

- English has a mature hyphenation tradition, shown in the slide with `Knuth-Liang Hyphenation Algorithm (1983)`.
- Korean long compounds are still often handled through syllable-level breaks, manual `<br>`, font substitution, or inter-character spacing.
- The slide demonstrates that these workarounds create awkward points, forced line breaks, and table layout failures.

Project use:

- Motivation for Korean-specific break opportunity modeling.
- Opening evidence for KrIGF and paper introduction.
- Candidate example for a W3C `klreq` issue, after converting it into a compact implementation-neutral test case.

## Evidence 002: HWPX Rendering Inconsistency

Image:

- `renders/krigf_p5-5.png`

Observed problem:

- The same paragraph renders differently across Hancom 2010, Hancom 2020, and Hancom Docs Web.
- Differences include line spacing, width scaling, inter-character spacing, and line break positions.
- The visual result makes HWPX automation fragile because the same source can produce different perceived layout quality.

Project use:

- Motivation for renderer-aware benchmark.
- Justification for recording font, renderer, width, and layout settings in every evidence item.
- Evidence that KOWRAP should not be only a tokenizer; it needs a layout evaluation harness.

## Evidence Template

Use this template for every new evidence item.

````md
## Evidence NNN: Title

Source:

- path or URL

Rendered artifact:

- path

Text:

```text
...
```

Renderer context:

- renderer:
- font:
- width:
- line-height:
- justification:
- date generated:

Observed bad behavior:

- ...

Expected better behavior:

- ...

Use in project:

- paper
- patent
- standardization
- code test
````
