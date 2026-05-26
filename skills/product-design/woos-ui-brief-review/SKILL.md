---
name: woos-ui-brief-review
description: Independent UI brief review gate. Verifies coverage, states, flows, accessibility, and component mapping before handoff.
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
- `docs/design/<version>/<feature>-ui-brief.md`
- `docs/prd/<version>/<feature>.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/reviews/<version>/<feature>-ui-review-rN.md`

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
