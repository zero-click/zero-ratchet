---
name: woos-ui-brief-review
description: Independent UI brief review gate. Verifies coverage, states, flows, accessibility, and component mapping before engineering delivery.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [ui, ux, review, gate, product-design]
    related_skills:
      - woos-product-design-flow
      - woos-ui-design-brief
---

# UI Brief Review

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

Run Step 5R of `woos-product-design-flow` as a dedicated fresh-context review skill.

This skill prevents the authoring context from self-certifying the UI brief.

## Required Invocation (hard gate)

- MUST be invoked separately from `woos-ui-design-brief`
- MUST use fresh context
- MUST read both the UI brief and the PRD
- MUST check every checklist row in one pass
- If any row is skipped, return `BLOCKED`

## Required Load Set (mandatory)

Before reviewing, load and report:

- `references/persona-ux-designer.md`
- `references/framework-ux-validate.md`
- `docs/design/<version>/<feature-id>-ui-brief.md`
- `docs/prd/<version>/<feature-id>.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/reviews/<version>/<feature-id>-ui-review-rN.md`

## Checklist

| # | Criterion | Fix Hint |
|---|-----------|----------|
| U1 | Screen coverage | List unmapped user stories; add a screen or flow for each |
| U2 | States complete | Add missing empty/loading/error/success/first-run states |
| U3 | Flows connected | Trace each flow end-to-end; add missing transitions or exits |
| U4 | Visual consistency | Remove contradicting principles; choose one direction |
| U5 | Accessibility realistic | Downgrade unrealistic targets; document actual target and trade-off |
| U6 | Components sufficient | Add missing component mappings or mark reuse explicitly |
| U7 | Principles actionable | Replace generic taste words with decision-guiding rules |

## Output Contract (required)

The output MUST include:

1. One row for every U1-U7 criterion
2. Concrete findings, not generic praise
3. A `## Summary` section with explicit verdict

## Verdicts

- `PASS` — all rows pass
- `REQUEST_CHANGES` — one or more rows fail
- `BLOCKED` — inputs missing, same-context review detected, or any row skipped

## Fail-Closed Rules

- No self-review
- No condensed "covered by above" rows
- PASS is forbidden if any criterion lacks evidence
- If the UI brief is intentionally minimal, the reviewer must still write explicit row-by-row confirmations
