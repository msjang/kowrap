# Korean Compound Break Selection

Last updated: 2026-05-21

## Purpose

KOWRAP should not only answer "where can this word be broken?" It should answer "which break should be chosen under the current line width, renderer, font, and typography constraints?"

For example:

```text
과학기술유공자
```

Possible internal breaks include:

```text
과학|기술유공자
과학기술|유공자
과학|기술|유공자
```

The usual semantic preference is:

```text
과학기술|유공자 > 과학|기술유공자
```

because `과학기술` is a strong compound and `유공자` is a natural suffix-like noun unit. But the final choice also depends on the remaining line width. If only `과학` fits in the current line, KOWRAP must compare:

```text
과학\n기술유공자
```

against:

```text
previous-word break\n과학기술유공자
```

or:

```text
slight spacing/width adjustment + 과학기술\n유공자
```

This is the same kind of decision Korean document workers often make manually in HWP by reducing 자간 or 장평 slightly. KOWRAP should make that tradeoff explicit and measurable rather than leaving it as manual formatting labor.

## Two-Layer Model

KOWRAP uses two layers.

1. Word-internal candidate scoring
2. Renderer-aware line choice

The first layer scores break candidates inside a word or eojeol. The second layer selects the best candidate for the current paragraph layout.

## Layer 1: Word-Internal Candidate Scoring

Each candidate break gets a semantic score and penalty.

Example:

```json
{
  "word": "과학기술유공자",
  "candidates": [
    {
      "offset": 2,
      "left": "과학",
      "right": "기술유공자",
      "break": "과학|기술유공자",
      "semantic_score": 0.42,
      "semantic_penalty": 58,
      "reason": "과학/기술 is possible, but 기술유공자 is a weaker right segment"
    },
    {
      "offset": 4,
      "left": "과학기술",
      "right": "유공자",
      "break": "과학기술|유공자",
      "semantic_score": 0.91,
      "semantic_penalty": 9,
      "reason": "과학기술 is a strong compound and 유공자 is a natural unit"
    }
  ]
}
```

Initial scoring signals:

- Strong known compounds get protection, e.g. `과학기술`, `정보통신`, `국가연구개발`.
- Left and right segments that are independent nouns get positive scores.
- Very short segments get penalties, especially one-syllable fragments.
- Domain terms from legal, science, policy, and institutional dictionaries get protection.
- Frequent corpus compounds get protection.
- Breaks before common head nouns such as `사업`, `계획`, `체계`, `유공자`, `지원`, `평가`, `관리` can receive positive scores when the left segment is also meaningful.

## Layer 2: Renderer-Aware Line Choice

Final line breaking is a layout decision. KOWRAP considers the current line width, font metrics, renderer behavior, optional typography adjustment, and the next few lines.

The line-level decision compares candidate actions:

```text
Action A: break inside the current word at candidate offset k
Action B: move the whole word to the next line
Action C: break at the previous eojeol
Action D: apply small inter-character spacing or width adjustment, then use a better semantic break
```

The selection minimizes a total cost:

```text
total_cost =
  layout_badness
+ semantic_break_penalty
+ typography_adjustment_penalty
+ lookahead_penalty
+ renderer_instability_penalty
```

Definitions:

- `layout_badness`: cost from overfull lines, underfull lines, rivers of space, and awkward raggedness.
- `semantic_break_penalty`: cost from the word-internal break score.
- `typography_adjustment_penalty`: cost from using 자간/장평 changes.
- `lookahead_penalty`: cost if the current choice makes the next one or two lines worse.
- `renderer_instability_penalty`: cost if the choice is likely to change across font or renderer conditions.

## Semantic-Preserving Microcompression

Sometimes the layout engine has an ugly choice:

```text
... 과학기|술유공자
```

The default overflow behavior may split at a poor semantic point. But a small negative spacing or width adjustment may allow:

```text
... 과학기술|유공자
```

KOWRAP should compare:

```text
bad semantic break cost
vs
microcompression cost
```

Example scoring:

```text
과학|기술유공자
semantic_penalty = 58
microtypography_penalty = 0

과학기술|유공자
semantic_penalty = 9
microtypography_penalty = 12  # e.g. letter-spacing -2%, glyph width 98.5%
```

The second option wins if preserving the semantic unit is worth the small typography adjustment.

Terminology:

- `letter-spacing` can be negative, e.g. `-0.02em`.
- 장평 should be described as width scaling or glyph width scale, e.g. `98.5%`, not as "negative 장평".

Initial safety bands:

```text
letter spacing:
  0% to -1%    nearly invisible, generally allowed
 -1% to -3%    allowed when it preserves a strong semantic unit
 -3% to -5%    restricted; table/narrow-cell cases only
 < -5%         normally forbidden

glyph width scale:
 100% to 98%   generally allowed
  98% to 96%   restricted
 <96%          normally forbidden
```

These numbers are starting hypotheses. They must be validated visually by font, renderer, and document type.

## Selection Rule

For `과학기술유공자`, the default semantic ranking is:

```text
과학기술|유공자 > 과학|기술유공자
```

If `과학기술` fits in the remaining line width, choose:

```text
과학기술\n유공자
```

If only `과학` fits, do not automatically choose:

```text
과학\n기술유공자
```

Instead compare:

```text
1. move the whole eojeol to the next line
2. use an earlier break opportunity
3. apply small typography adjustment so 과학기술 fits
4. accept 과학|기술유공자 only if the alternatives are worse
```

This means an inferior semantic break can be used, but only after the layout model decides that the alternatives cost more.

## Dynamic Programming Shape

The paragraph can be modeled as a lattice.

Nodes:

- eojeol boundaries
- word-internal break candidates
- optional typography adjustment states
- microcompression states, such as `letter_spacing=-0.02em` or `glyph_width=98.5%`

Edges:

- candidate line segments
- edge cost = layout + semantic + typography + lookahead approximation

The best line breaking is the lowest-cost path through the lattice.

Minimal v0:

```text
for each paragraph:
  generate break candidates
  assign semantic penalties
  estimate rendered width for candidate line segments
  compute lowest-cost line breaks with dynamic programming
```

Future versions can replace heuristic semantic penalties with model scores while keeping the same line-selection interface.

## Data Annotation Implication

The dataset should label more than a binary safe/bad break.

Useful labels:

- `preferred_breaks`: best semantic breaks when width is not constrained.
- `acceptable_breaks`: usable but not ideal breaks.
- `bad_breaks`: breaks that should be avoided unless no reasonable alternative exists.
- `protected_spans`: segments that should not be split in normal conditions.
- `contextual_notes`: explanation of width-dependent tradeoffs.
- `microcompression_allowed`: whether small spacing/width adjustment may be used to preserve the preferred break.

Example:

```json
{
  "text": "과학기술유공자",
  "protected_spans": ["과학기술"],
  "preferred_breaks": ["과학기술/유공자"],
  "acceptable_breaks": ["과학/기술유공자"],
  "bad_breaks": [],
  "microcompression_allowed": true,
  "contextual_notes": "Prefer 과학기술/유공자. 과학/기술유공자 is acceptable only when layout alternatives are worse."
}
```
