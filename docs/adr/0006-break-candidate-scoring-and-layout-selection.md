# ADR 0006: Separate Break Candidate Scoring from Layout Selection

Date: 2026-05-21

Status: Accepted

## Context

Korean compound words often contain multiple possible internal break points. For example, `과학기술유공자` can be split as `과학|기술유공자` or `과학기술|유공자`. The second is usually semantically better, but the renderer may not have enough remaining line width to fit `과학기술`.

If KOWRAP only labels break points as safe or unsafe, it cannot make good choices under real layout constraints.

## Decision

KOWRAP will separate the problem into two layers.

Layer 1 scores word-internal break candidates using semantic, lexical, domain, and corpus signals.

Layer 2 selects actual line breaks using renderer-aware layout cost, including remaining line width, font metrics, typography adjustment cost, next-line effects, and semantic break penalties. It may choose small semantic-preserving microcompression, such as slightly negative letter spacing or modest glyph width scaling, when that avoids a much worse semantic break.

The final decision minimizes:

```text
total_cost =
  layout_badness
+ semantic_break_penalty
+ typography_adjustment_penalty
+ lookahead_penalty
+ renderer_instability_penalty
```

## Consequences

Benefits:

- The same semantic break model can be reused across renderers.
- The layout engine can choose a lower-ranked semantic break only when line conditions justify it.
- Future ML models can replace heuristic candidate scores without changing the selection interface.
- Annotation can capture preferred, acceptable, and bad breaks rather than a flat binary label.
- The system can model what Korean document workers manually do with HWP 자간/장평 shortcuts, but with explicit bounds and penalties.

Costs:

- The benchmark needs width/font/renderer context for layout-level evaluation.
- The data schema needs richer labels than `safe_breaks` and `bad_breaks`.
- The implementation needs at least a simple dynamic-programming line breaker for serious evaluation.
- Microcompression thresholds must be validated visually across fonts and renderers.

## Review Trigger

Revisit this ADR when:

- the first renderer harness exists
- the annotation schema is revised for preferred/acceptable/protected spans
- the first trainable scoring model is introduced
