---
name: woos-prd-consistency-audit
description: Dedicated analyze gate for PRD and UI brief consistency. Runs script extraction first, then semantic review with evidence-backed findings.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, prd, audit, consistency, gate]
    related_skills:
      - woos-product-design-flow
      - woos-ui-design-brief
---

# PRD Consistency Audit

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

Run Step 6 of `woos-product-design-flow` as an isolated audit skill.

This skill exists to stop the parent orchestrator from skipping straight to a soft summary like "looks consistent enough."

## Required Invocation (hard gate)

- MUST be invoked as a separate skill
- MUST run `scripts/analyze_gate.py` before semantic review
- MUST use the script output as evidence, not as the final verdict
- MUST review every A1-A5 check explicitly
- If script execution is skipped or any check is omitted, return `BLOCKED`

## Required Load Set (mandatory)

Before auditing, load and report:

- `references/framework-implementation-readiness.md`
- `scripts/analyze_gate.py`
- `docs/prd/<version>/<feature-id>.md`
- `docs/design/<version>/<feature-id>-ui-brief.md` (if present)

If any required file is not loaded, return `BLOCKED`.

## Conditional Load Set (upstream dependencies)

When the orchestrator provides upstream interface summaries, also load:

- `docs/prd/<version>/<upstream-feature-id>-interface.md` for each declared upstream dependency

When upstream interface summaries are present, add **A6** to the required checks:

| A6 | Upstream Interface Consistency | All shared concepts used in this feature's PRD/UI match upstream interface definitions (enums, field names, event types, terminology) |

A6 failures count toward `GAPS_FOUND`.

## Output

- `docs/reviews/<version>/<feature-id>-analyze-report.md`

## Two-Phase Protocol

### Phase 1 — Script Extraction

Run `scripts/analyze_gate.py` to extract:

- user stories
- acceptance criteria
- flows
- non-goals
- UI screens
- placeholders
- deterministic hotspot candidates

### Phase 2 — Semantic Audit

Review the extracted evidence and decide whether script-flagged mismatches are:

- real gaps
- wording differences
- acceptable scope choices

## Required Checks

| # | Check | Pass Condition |
|---|-------|----------------|
| A1 | Requirement Coverage | Every user story has acceptance criteria |
| A2 | AC Testability | Every AC is verifiable without implementation knowledge |
| A3 | Flow Completeness | Flows have clear start/end transitions |
| A4 | Non-goal Alignment | Requirements do not contradict non-goals |
| A5 | UI Coverage | Every UI screen maps to one or more user stories |

## Output Contract (required)

The final report MUST contain a table with these columns:

| Check | Script Evidence | Semantic Judgment | Result |
|------|------------------|-------------------|--------|

Every A1-A5 row must be present. When upstream interface summaries are loaded, A6 must also be present.

The final report MUST also contain a dedicated `## Semantic Audit Verdict` section. A raw `SIGNALS_CLEAR` / `HOTSPOTS_FOUND` script dump is not a valid gate completion artifact.

## Verdicts

- `PASS` — all A1-A5 rows pass after semantic review, A6 passes when it applies, and `## Semantic Audit Verdict` is present
- `GAPS_FOUND` — one or more real gaps remain
- `BLOCKED` — script not run, evidence missing, or row coverage incomplete

## Fail-Closed Rules

- PASS is forbidden if the report only gives a summary without row-level evidence
- If script output and final judgment disagree, explain why
- If UI brief is absent, A5 must still appear as `N/A` with reason
