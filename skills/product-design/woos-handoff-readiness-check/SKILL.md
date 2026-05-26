---
name: woos-handoff-readiness-check
description: Dedicated handoff readiness gate. Runs deterministic extraction first, then semantic readiness review before engineering starts.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [handoff, readiness, gate, audit, product-design]
    related_skills:
      - woos-product-design-flow
      - woos-build-handoff
---

# Handoff Readiness Check

## Purpose

Run Step 8 of `woos-product-design-flow` as a dedicated gate skill instead of an in-flow mental checklist.

## Required Invocation (hard gate)

- MUST be invoked as a separate skill
- MUST run `scripts/readiness_check.py` before semantic review
- MUST inspect every checklist row explicitly
- MUST produce the declared output file
- If any row is skipped or evidence is missing, return `BLOCKED`

## Required Load Set (mandatory)

Before auditing, load and report:

- `references/framework-implementation-readiness.md`
- `scripts/readiness_check.py`
- `templates/readiness-template.md`
- `docs/handoff/<version>/<feature>.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/reviews/<version>/<feature>-readiness.md`

## Two-Phase Protocol

### Phase 1 — Script Extraction

Run `scripts/readiness_check.py` to extract:

- acceptance criteria
- task mappings
- unresolved items
- flows
- UI-direction presence
- DCR protocol signals

### Phase 2 — Semantic Readiness Review

Review script findings row by row and decide whether any literal warning is a true readiness blocker.

## Checklist

1. All AC are testable
2. Build Tasks map to user stories
3. No unresolved product decisions
4. User flows have no dead ends
5. UI brief covers all interactive features (if applicable)
6. Non-goals clear enough to prevent scope creep
7. DCR protocol specified

## Output Contract (required)

The report MUST match the readiness template structure:

1. `## Checklist`
2. `## Unresolved Items`
3. `## Verdict`

Each checklist row must include status and notes.

## Verdicts

- `PASS` — all applicable rows pass
- `FAIL` — one or more real readiness blockers remain
- `BLOCKED` — script not run, checklist incomplete, or final report missing required sections

## Fail-Closed Rules

- PASS is forbidden if unresolved placeholders remain unaddressed
- PASS is forbidden if the report has no row-level evidence
- `N/A` is allowed only when the row is genuinely not applicable and the reason is stated
