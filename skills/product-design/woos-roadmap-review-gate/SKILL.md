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
