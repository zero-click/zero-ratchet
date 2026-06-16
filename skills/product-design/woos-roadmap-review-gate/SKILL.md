---
name: woos-roadmap-review-gate
description: Independent roadmap review gate for discovery. Checks roadmap quality and returns PASS or REQUEST_CHANGES.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, roadmap, review, gate]
    related_skills:
      - woos-product-discovery
      - woos-roadmap-authoring
---

# Roadmap Review Gate

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

Review the roadmap in fresh context before architecture work continues.

## Required Load Set (mandatory)

- `references/persona-prd-validator.md`
- `docs/product/<project>-roadmap.md`
- `ideas/<slug>/00-idea-capture.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/reviews/<project>-roadmap-review-rN.md`

## Checklist

| # | Criterion | Fix Hint |
|---|-----------|----------|
| R1 | Vision differentiated | Add a distinct angle compared with alternatives |
| R2 | Versioning logical | Keep V1 independently shippable |
| R3 | Metrics measurable | Replace vague claims with observable thresholds |
| R4 | Non-goals effective | State concrete exclusions |
| R5 | Decision Log sound | Record real alternatives and rationale |
| R6 | Personas grounded | Tie personas to evidence or observed behavior |

Every row must have a finding and status.
