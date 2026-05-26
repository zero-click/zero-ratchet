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
