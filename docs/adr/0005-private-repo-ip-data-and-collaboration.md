# ADR 0005: Private Repository, Open-Source-First IP, Public Legal Data, and KONI First

Date: 2026-05-21

Status: Accepted

## Context

The project now needs a concrete repository and near-term collaboration path. The owner wants to start privately, keep Apache-2.0 as the default public license, and explore whether institutional patent handling can coexist with open-source availability.

The project also needs data before internal document access is ready. Public legal text is a plausible first corpus because it contains long formal Korean compounds and is available through official public law data services.

## Decision

Use `msjang/kowrap` as the initial private GitHub repository.

Keep Apache-2.0 as the default license for public code, documentation, and project-authored synthetic examples.

Explore institutional patent filing only if it can support an open-source-friendly posture. The desired direction is:

- open-source implementations can use the public Apache-2.0 implementation freely
- commercial proprietary users can be handled through explicit licensing if needed
- exact claim-sensitive mechanisms are not published until the disclosure boundary is clear

Use public legal text and synthetic examples as the first data sources. Internal HWP/HWPX/PDF documents remain optional private evaluation material, not a requirement for Phase 0 or Phase 1.

Prioritize KONI / KISTI internal AI collaboration first. HWPX maintainers, W3C `klreq`, and browser/document-layout implementers follow after the benchmark and disclosure boundary are more stable.

## Consequences

Benefits:

- The project can move without waiting for internal document access.
- A private repo allows early iteration before public disclosure.
- Apache-2.0 keeps the project aligned with practical adoption by browser and document-tool implementers.
- KONI collaboration can give the project an institutionally legible AI path without making ML the first dependency.

Costs:

- Private-first development delays outside maintainer feedback.
- Public legal text still needs careful source and redistribution handling.
- Institutional patent handling may slow public release if not scoped early.
- Apache-2.0 patent grants and any separate institutional licensing strategy must be reconciled carefully.

## Review Trigger

Revisit this ADR before:

- making the repository public
- publishing a W3C issue
- presenting detailed scoring formulas
- submitting an invention disclosure
- using KONI outputs in benchmark or model training

