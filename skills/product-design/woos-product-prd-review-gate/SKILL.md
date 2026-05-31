---
name: woos-product-prd-review-gate
description: Independent product-side PRD review gate. Runs the full PRD checklist in fresh context and returns PASS or REQUEST_CHANGES.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, prd, review, gate, validator]
    related_skills:
      - woos-product-design-flow
---

# Product PRD Review Gate

## Purpose

Run Step 4 of `woos-product-design-flow` as an isolated review skill so the reviewer cannot coast on the parent orchestrator's momentum.

This skill exists to enforce:

- fresh-context review
- full checklist coverage
- explicit structural + content verdicts
- fail-closed behavior when evidence is missing

## Required Invocation (hard gate)

- MUST be invoked as a separate skill from `woos-product-design-flow`
- MUST use fresh context; same-session self-review is invalid
- MUST read all declared inputs before issuing a verdict
- MUST cover Phase A and Phase B in one run
- If any required section or checklist row is skipped, return `BLOCKED`

## Required Load Set (mandatory)

Before reviewing, load and report:

- `references/persona-prd-validator.md`
- `references/template-prd-validation-checklist.md`
- `docs/prd/<version>/<feature>.md`
- `docs/prd/<version>/<feature>-requirements.md`
- `docs/product/<project>-architecture.md`

If any required file is not loaded, return `BLOCKED`.

## Conditional Load Set (upstream dependencies)

When the orchestrator provides upstream interface summaries, also load:

- `docs/prd/<version>/<upstream-feature>-interface.md` for each declared upstream dependency

When upstream interface summaries are present, add **P8** to the content quality checklist:

| P8 | Upstream interface alignment | Verify all shared concepts (enums, models, events, endpoints, terms) match upstream interface definitions exactly. Flag any divergence. |

P8 failures count toward `REQUEST_CHANGES`.

## Output

- `docs/reviews/<version>/<feature>-prd-review-rN.md`

## Review Protocol

### Phase A — Structural Completeness

Check all required PRD sections:

1. `## Background`
2. `## User Personas`
3. `## Functional Requirements`
4. `## Non-Functional Requirements`
5. `## User Flows`
6. `## Edge Cases`
7. `## Non-Goals`
8. `## Success Metrics`

If any section is missing, the result is immediately `REQUEST_CHANGES`.

### Phase B — Content Quality Checklist

| # | Criterion | Fix Hint |
|---|-----------|----------|
| P1 | Value-traced | Add `User value:` lines linking each requirement to user outcome |
| P2 | AC testable | Rewrite as Given/When/Then or add measurable threshold |
| P3 | Non-goals effective | Make non-goals concrete enough to reject a real request |
| P4 | Edge cases covered | Add empty/error/timeout/concurrent-access scenarios |
| P5 | Real user behavior | Replace developer-centric wording with user-observable behavior |
| P6 | No internal contradictions | Resolve conflicting statements or move scope to non-goals |
| P7 | Architecture reference check | Compare routes/constants/state names against architecture and annotate divergence |

## Special Rule — P7 Does Not Auto-Fail

Architecture is a reference, not a hard constraint.

- `✅` = aligned
- `📐` = intentional or explainable divergence
- `❌` = true contradiction with no rationale

Only unsupported contradictions count toward `REQUEST_CHANGES`.

## Output Contract (required)

The output MUST include:

1. Structural checklist results
2. Full P1-P7 review table
3. `## Architecture Divergences` section when needed
4. `## Summary` with explicit verdict

## Verdicts

- `PASS` — all required structural checks pass and P1-P6 have no failures
- `REQUEST_CHANGES` — one or more structural/content failures remain
- `BLOCKED` — review incomplete, missing inputs, or checklist rows were skipped

## Fail-Closed Rules

- No blanket pass language
- No "looks good overall"
- Every checklist row MUST have a status and a concrete finding
- If any row has no finding or no judgment, verdict is `BLOCKED`
- If the reviewer cannot confirm a point, mark it explicitly and fail the gate
