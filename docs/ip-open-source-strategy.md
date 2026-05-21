# IP and Open-Source Strategy

Last updated: 2026-05-21

This is an engineering strategy note, not legal advice.

## Current Position

KOWRAP starts as an Apache-2.0 open-source project in a private repository.

The owner is willing to ask KISTI whether institutional patent filing makes sense, but the default fallback is open-source release if the institutional route does not fit.

Desired shape:

- Keep the reference implementation open under Apache-2.0.
- Let open-source implementers such as browser engines or document tooling use it freely under that license.
- If an institution wants a patent/commercial licensing path, keep that path compatible with the open-source reference implementation.
- Avoid delaying the core project indefinitely for IP handling.

## Why This Is Plausible

Apache-2.0 includes an explicit patent license from contributors for patent claims necessarily infringed by their contributions. It is therefore a better fit than MIT/BSD if the project may touch patents while still trying to be open-source-friendly.

This does not automatically solve institutional ownership. It only means the chosen open-source license has a patent-aware mechanism.

## Main Legal/Policy Questions

### 1. Is this a work-related invention?

Under Korean invention law, the key test is not only whether the work was done during office hours. The risk point is whether the invention:

- relates to the employee's duties
- falls within the employer's business scope
- was made through current or past job duties

The owner believes the core research field is computer networking, and KOWRAP began from personal frustration with report typography and open-source HWPX work outside regular duties. That is a credible argument for non-duty invention, but it is not enough by itself.

KISTI's employment rules, research assignment, use of institutional resources, and whether KONI/internal data/GPU resources are used can change the analysis.

### 2. Can KISTI patent and still allow open-source use?

Maybe, but it must be designed deliberately. Possible patterns:

- Institution files a patent but grants Apache-2.0 or equivalent royalty-free license for the reference implementation.
- Institution files a patent and uses a separate commercial license for proprietary implementations.
- Institution declines patent handling; owner releases under Apache-2.0 as a personal/open-source project.

The risky middle state is filing or disclosing without a clear license grant, because that can chill adoption by open-source maintainers.

### 3. What should not be disclosed yet?

Safe to disclose early:

- problem statement
- rendered evidence
- benchmark need
- synthetic examples
- high-level architecture
- comparison with existing layout behavior

Hold until IP review or deliberate open release:

- exact scoring formula
- model compression method
- domain adaptation mechanism
- render-aware optimization loop
- claim language

## Recommended Operating Rule

Proceed with Apache-2.0 development now, but separate public communication into two tiers.

Tier 1 public-safe material:

- evidence pack
- data schema
- benchmark design
- rule/statistical baselines
- synthetic examples

Tier 2 hold-back material:

- specific invention claims
- scoring internals
- trainable model details
- commercial licensing proposal

This keeps momentum while preserving the option to talk to institutional IP staff.

## Recommended Message to Institution

KOWRAP is an Apache-2.0 open-source reference implementation for Korean line breaking and renderer-aware typography evaluation. I would like KISTI to review whether any patentable implementation method should be disclosed and filed institutionally. My preferred route is open-source-friendly: public implementations remain freely usable under Apache-2.0, while any proprietary commercial licensing can be handled separately if the institution wants that path. If institutional filing is not appropriate, I plan to proceed as an open-source personal research project with careful separation from internal data and confidential resources.

## Source Notes

- Apache License 2.0 official text includes a patent grant in Section 3 and redistribution conditions in Section 4: https://www.apache.org/licenses/LICENSE-2.0
- Apache guidance says ALv2 is a set of copyright and patent licensing terms and recommends top-level `LICENSE` and `NOTICE` files: https://www.apache.org/legal/apply-license
- Korean employee-invention analysis should be checked against current `발명진흥법`, institutional employment rules, and KISTI IP policy before public disclosure.

