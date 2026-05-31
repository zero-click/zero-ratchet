---
name: woos-prd-authoring
description: Write the per-feature PRD from the ranked requirements contract using the mandatory PRD template.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, prd, authoring, design-flow]
    related_skills:
      - woos-product-design-flow
      - woos-requirement-contract
      - woos-product-prd-review-gate
---

# PRD Authoring

## Purpose

Convert the ranked requirements contract into a full PRD for one feature.

## Required Load Set (mandatory)

- `references/framework-prd.md`
- `references/template-prd-template.md`
- `templates/prd-template.md`
- `docs/prd/<version>/<feature>-requirements.md`

If any required file is not loaded, return `BLOCKED`.

## Conditional Load Set (upstream dependencies)

When the orchestrator provides upstream interface summaries, also load:

- `docs/prd/<version>/<upstream-feature>-interface.md` for each declared upstream dependency

When referencing shared concepts (status enums, data models, event types, API endpoints), use the exact definitions from upstream interface summaries. Do NOT invent alternate names for concepts already defined upstream.

## Output

- `docs/prd/<version>/<feature>.md`

## Required Sections

1. `## Background`
2. `## User Personas`
3. `## Functional Requirements`
4. `## Non-Functional Requirements`
5. `## User Flows`
6. `## Edge Cases`
7. `## Non-Goals`
8. `## Success Metrics`

## Authoring Rules

- Follow the template exactly
- Give full detail to `P0` scope; keep `P2` brief
- Mark unresolved items as `[NEEDS CLARIFICATION: ...]`
- Do not embed review verdicts or gate outcomes in the PRD itself
