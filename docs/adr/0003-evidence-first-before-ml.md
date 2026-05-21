# ADR 0003: Build Evidence and Baselines Before Large ML

Date: 2026-05-21

Status: Accepted

## Context

The long-term project may include lightweight ML, model distillation, domain fine-tuning, and GPU training. However, starting there would make the project hard to evaluate and hard to explain. The immediate gap is that Korean compound-word line breaking lacks shared examples, benchmark schema, renderer-aware tests, and reference baselines.

## Decision

KOWRAP will proceed in this order:

1. Evidence pack
2. Data schema
3. Simple baselines
4. Renderer harness
5. Lightweight model
6. Domain adaptation and distillation

Large ML work should not begin until baseline failures are measurable and reproducible.

## Consequences

Benefits:

- The project can produce useful open-source and standardization artifacts early.
- Paper claims will be grounded in measurable baselines.
- Patent-sensitive details can be separated from public problem evidence.
- GPU work later has a clear target and evaluation loop.

Costs:

- The project may feel less flashy in the first phase.
- Some ambitious model ideas will remain parked until the benchmark is ready.

## Review Trigger

Revisit this ADR when:

- the seed benchmark reaches at least 100 labeled examples
- a renderer harness can render and compare outputs reproducibly
- the rule/statistical baselines have clear failure modes
- the GPU VM is available and data boundaries are approved

