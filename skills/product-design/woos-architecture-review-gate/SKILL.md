---
name: woos-architecture-review-gate
description: Independent high-level architecture review gate for discovery.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, discovery, architecture, review, gate]
    related_skills:
      - woos-product-discovery
      - woos-architecture-overview
---

# Architecture Review Gate

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

Review the architecture overview in fresh context before discovery completes.

## Required Load Set (mandatory)

- `references/framework-architecture-validation.md`
- `docs/product/<project>-architecture.md`
- `docs/product/<project>-roadmap.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/reviews/<project>-architecture-review-rN.md`

## Checklist

| # | Criterion | Fix Hint |
|---|-----------|----------|
| A1 | Component boundaries | Split unclear or overloaded components |
| A2 | Communication consistency | Pick one dominant pattern and justify exceptions |
| A3 | Data decoupling | Add boundaries where raw sharing is too tight |
| A4 | Infrastructure proportional | Avoid premature infra for later versions |
| A5 | Dependencies manageable | Mark independent vs sequential buildability |
| A6 | Risks realistic | Add concrete mitigations |
| A7 | Version-aligned | Keep V2+ only elements out of V1 baseline |

Every row must have a finding and status.
