---
name: woos-version-integration-audit
description: Dedicated cross-feature integration audit. Extracts candidate conflicts by script, then performs evidence-backed semantic review across the full version scope.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [integration, audit, cross-feature, traceability, gate, product-design]
    related_skills:
      - woos-product-design-flow
      - woos-handoff-readiness-check
---

# Version Integration Audit

## Purpose

Run Step 9 of `woos-product-design-flow` as a standalone audit skill with its own completion contract.

This skill exists because cross-feature review is where agents most often pretend they checked everything and then write a shallow PASS.

## Incremental Execution Model

This skill runs **incrementally** — not just once at the end:

- After the 2nd feature completes Step 8.5 → first run (F1 + F2)
- After each subsequent feature → incremental run (all completed features so far)
- Final run after last feature → full integration report

**Context management:** To avoid context explosion, each incremental run loads:

- Full docs: ONLY the newest completed feature (PRD + requirements + handoff + UI brief)
- Interface summaries: ALL previously completed features (`*-interface.md`)
- Script pre-filter: `integration_gate.py` extracts conflict candidates BEFORE semantic review
- Roadmap + architecture: always loaded (shared context)

This keeps context bounded at O(1 full feature + n interface summaries) rather than O(n full features).

## Required Invocation (hard gate)

- MUST be invoked as a separate skill in fresh context
- MUST run `scripts/integration_gate.py` before semantic review
- MUST read the full version input scope, not only handoff files
- MUST produce a finding for every A1-A5, B1-B5, C1-C5 row
- MUST include row-level evidence in the final report
- If any row is missing evidence or judgment, return `BLOCKED`

## Required Load Set (mandatory)

Before auditing, load and report:

- `references/framework-implementation-readiness.md`
- `scripts/integration_gate.py`
- `docs/product/<project>-roadmap.md`
- `docs/product/<project>-architecture.md`
- `docs/prd/<version>/<newest-feature>-requirements.md` (full doc for newest feature)
- `docs/prd/<version>/<newest-feature>.md` (full doc for newest feature)
- `docs/handoff/<version>/<newest-feature>.md` (full doc for newest feature)
- `docs/design/<version>/<newest-feature>-ui-brief.md` (if present, for newest feature)
- `docs/prd/<version>/<feature>-interface.md` for ALL previously completed features

For the **final run** (after last feature), load full docs for all features instead of just the newest.

If any required file is not loaded, return `BLOCKED`.

## Input Scope (all required)

- `docs/product/<project>-roadmap.md`
- `docs/product/<project>-architecture.md`
- `docs/prd/<version>/<feature>-requirements.md` for all features
- `docs/prd/<version>/<feature>.md` for all features
- `docs/handoff/<version>/<feature>.md` for all features
- `docs/design/<version>/<feature>-ui-brief.md` for all features that have one
- `scripts/integration_gate.py`

## Output

- `docs/reviews/<version>/integration-report.md`

## Two-Phase Protocol

### Phase 1 — Script Extraction

Run `scripts/integration_gate.py` to extract candidate evidence, including:

- feature coverage matrix
- constants
- endpoints
- state signatures
- UI-to-PRD mappings
- deterministic coverage gaps

### Phase 2 — Semantic Audit

Review the extracted evidence and decide whether candidate mismatches are:

- true conflicts
- semantic equivalents
- harmless naming differences
- intentional divergences that should be documented but not block

## Required Checklist

### Part A — Shared Concept Consistency

- A1 State machine unified
- A2 Constants consistent
- A3 Data model aligned
- A4 API contract consistent
- A5 Terminology unified

### Part B — Completeness & Traceability

- B1 Roadmap → Requirements coverage
- B2 Requirements → PRD coverage
- B3 PRD → Handoff coverage
- B4 Architecture → PRD alignment
- B5 UI → PRD traceability

### Part C — Cross-Feature Integration

- C1 No AC conflicts
- C2 User flows connectable
- C3 No duplicate effort
- C4 Dependency order clear
- C5 Error handling consistent

## Output Contract (required)

The final report MUST include a row for every A1-C5 check with these columns:

| Check | Script Evidence | Semantic Judgment | Result |
|------|------------------|-------------------|--------|

It MUST also include:

1. `## Summary`
2. `## Part A — Shared Concepts`
3. `## Part B — Traceability`
4. `## Part C — Cross-Feature`
5. `## Verdict`
6. `## Recommended Fix Order`

## Verdicts

- `PASS` — all 15 checks reviewed and no real conflicts remain
- `CONFLICTS_FOUND` — all 15 checks reviewed and one or more real conflicts remain
- `BLOCKED` — script not run, full input scope not read, row coverage incomplete, or evidence missing

## Fail-Closed Rules

- PASS is forbidden if the report skips any A1-C5 row
- PASS is forbidden if a row has no script evidence
- PASS is forbidden if a row has no semantic judgment
- "Reviewed all docs, no major conflicts found" is not a valid completion state
