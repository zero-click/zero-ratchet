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
      - woos-prd-consistency-audit
---

# Version Integration Audit

## Output Language

- Author all user-facing prose (narratives, findings, summaries) in the **user's most recent input language** (e.g. if the user is writing in Chinese, write the PRD body, review findings, and summaries in Chinese).
- Keep these tokens **verbatim in English** regardless of the user's language, because they are contract identifiers consumed by other skills and gates:
  - Verdict tokens: `PASS`, `REQUEST_CHANGES`, `BLOCKED`, `NOT_RUN`
  - Severity tokens: `critical`, `high`, `medium`, `low`, `warning`
  - Tag tokens: `[ASSUMPTION: ...]`, `[NEEDS CLARIFICATION: ...]`, `[NEEDS INPUT: ...]`
  - Phase / dimension IDs: `P0` … `P11`, `P2a`, `Phase A`, `Phase B`
  - Shape values: `internal-tool`, `single-operator`, `consumer-product`, `multi-stakeholder`, `CLI`
  - P0 rating values: `strong`, `adequate`, `thin`, `broken`
  - Section headings declared in templates (e.g. `## Background`, `## Functional Requirements`, `## Assumptions Index`) — translations break downstream structural checks
  - Field labels inside templates (e.g. `**Consequences (testable):**`, `**Out of Scope:**`, `**User value:**`, `Given … When … Then …`)
- Code, file paths, IDs, and quoted PRD excerpts stay in their original form.


## Purpose

Run Step 6 of `woos-product-design-flow` as a standalone audit skill with its own completion contract.

This skill exists because cross-feature review is where agents most often pretend they checked everything and then write a shallow PASS.

## Incremental Execution Model

This skill runs **incrementally** — not just once at the end:

- After the 2nd feature completes Step 5.5 → first run (F1 + F2)
- After each subsequent feature → incremental run (all completed features so far)
- Final run after last feature → full integration report

**Context management:** To avoid context explosion, each incremental run loads:

- Full docs: ONLY the newest completed feature (PRD + UI brief when present)
- Interface summaries: ALL completed features (`*-interface.md`), including the newest when produced
- Script pre-filter: `integration_gate.py` extracts conflict candidates BEFORE semantic review
- Roadmap + architecture: always loaded (shared context)

This keeps context bounded at O(1 full feature + n interface summaries) rather than O(n full features).

## Required Invocation (hard gate)

- MUST be invoked as a separate skill in fresh context
- MUST run `scripts/integration_gate.py` before semantic review
- MUST account for the full version scope (roadmap + architecture + all completed feature interfaces), not only the newest feature's full docs
- MUST produce a finding for every A1-A5, B1-B5, C1-C5 row
- MUST include row-level evidence in the final report
- If any row is missing evidence or judgment, return `BLOCKED`

## Required Load Set (mandatory)

Before auditing, load and report:

- `references/framework-implementation-readiness.md`
- `scripts/integration_gate.py`
- `docs/product/<project>-roadmap.md`
- `docs/product/<project>-architecture.md`
- `docs/prd/<version>/<newest-feature>.md` (full doc for newest feature)
- `docs/design/<version>/<newest-feature>-ui-brief.md` (if present, for newest feature)
- `docs/prd/<version>/<feature-id>-interface.md` for ALL completed features when produced

For the **final run** (after last feature), load full docs for all features instead of just the newest, plus all interface summaries when produced.

If any required file is not loaded, return `BLOCKED`.

## Input Scope

**Shared scope for every run:**

- `docs/product/<project>-roadmap.md`
- `docs/product/<project>-architecture.md`
- `docs/prd/<version>/<feature-id>-interface.md` for all completed features when produced
- `scripts/integration_gate.py`

**Incremental run additional full-doc scope:**

- `docs/prd/<version>/<newest-feature>.md`
- `docs/design/<version>/<newest-feature>-ui-brief.md` (if present)

Previously completed features may be represented by **interface summaries only** during incremental runs. They are still part of scope; they are not missing full-doc coverage unless this is the final run.

The orchestrator MUST invoke the script without `--final-run` for incremental checks, and WITH `--final-run` after the last feature completes.
For every run it MUST pass `--feature <feature-id>` for each audited feature in the selected-version scope completed so far. For incremental checks it MUST also pass `--newest-feature <feature-id>`. For final checks it MUST add `--final-run`.

**Final run additional full-doc scope:**

- `docs/prd/<version>/<feature-id>.md` for all features
- `docs/design/<version>/<feature-id>-ui-brief.md` for all features that have one

## Output

- `docs/reviews/<version>/integration-report.md` (or `integration-report-after-<feature-id>.md` for incremental runs)

## Two-Phase Protocol

### Phase 1 — Script Extraction

Run `scripts/integration_gate.py` to extract candidate evidence, including:

- feature coverage matrix
- constants
- endpoints (including duplicate-endpoint signals — same `METHOD /path` defined by multiple sources)
- state signatures
- UI-to-PRD mappings
- deterministic coverage gaps
- A1-C5 script evidence rows (a row may explicitly say no deterministic signal was found)

The script emits `SIGNALS_CLEAR` or `HOTSPOTS_FOUND` as a **script signal only** (in a `## Script Verdict` section). It does NOT emit `PASS` / `CONFLICTS_FOUND`. The gate verdict is set by Phase 2.

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

- B1 Roadmap → PRD coverage
- B2 PRD → Interface Summary coverage
- B3 Architecture → PRD alignment
- B4 UI → PRD traceability
- B5 Version-scope file coverage

### Part C — Cross-Feature Integration

- C1 No AC conflicts
- C2 User flows connectable
- C3 No duplicate effort
- C4 Dependency order clear
- C5 Error handling consistent

For **incremental runs**, C1/C2 are provisional checks based on the newest feature's full PRD plus previously completed features' interface summaries. Full PRD-to-PRD verification of C1/C2 is mandatory on the **final run**.

## Output Contract (required)

The final report MUST include a row for every A1-C5 check with these columns:

| Check | Script Evidence | Semantic Judgment | Result |
|------|------------------|-------------------|--------|

The semantic-review report MUST carry forward the script's A1-C5 evidence rows. When the script has no deterministic signal for a row, preserve that fact explicitly rather than inventing evidence.

It MUST also include:

1. `## Summary`
2. `## Part A — Shared Concepts`
3. `## Part B — Traceability`
4. `## Part C — Cross-Feature`
5. `## Verdict` — the gate verdict (`PASS` or `CONFLICTS_FOUND`). This is set by the audit skill in Phase 2 and is separate from the script's `## Script Verdict` (which only emits `SIGNALS_CLEAR` / `HOTSPOTS_FOUND`).
6. `## Recommended Fix Order`

A report that contains only the raw script output (no `## Verdict` section, no per-row semantic judgments) is not a completed gate output and MUST be treated as `BLOCKED`.

## Verdicts

- `PASS` — all 15 checks reviewed and no real conflicts remain
- `CONFLICTS_FOUND` — all 15 checks reviewed and one or more real conflicts remain
- `BLOCKED` — script not run, full input scope not read, row coverage incomplete, or evidence missing

## Fail-Closed Rules

- PASS is forbidden if the report skips any A1-C5 row
- PASS is forbidden if a row has neither script-produced evidence nor an explicit "no deterministic signal" note
- PASS is forbidden if a row has no semantic judgment
- "Reviewed all docs, no major conflicts found" is not a valid completion state
