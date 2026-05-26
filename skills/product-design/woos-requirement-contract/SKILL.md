---
name: woos-requirement-contract
description: Produce the per-feature requirements contract used as the input to priority ranking and PRD authoring.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, requirements, authoring, design-flow]
    related_skills:
      - woos-product-design-flow
      - woos-prd-authoring
---

# Requirement Contract

## Purpose

Turn one selected roadmap feature into a structured requirements file before any ranking or PRD work begins.

## Required Load Set (mandatory)

- `references/framework-prd.md`
- `templates/requirements-template.md`
- `docs/product/<project>-roadmap.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/prd/<version>/<feature>-requirements.md`

## Required Sections

1. `## Problem Statement`
2. `## Goals`
3. `## User Stories`
4. `## Non-Goals`
5. `## Constraints`
6. `## Risks & Unknowns`
7. `## Priority Ranking`

## Authoring Rules

- Follow the template structure exactly
- Keep the file scoped to one feature only
- Mark unresolved items as `[NEEDS CLARIFICATION: ...]`
- Do not fold this output into the PRD
- Include an explicit `P0 / P1 / P2` ranking and ship cut-line in `## Priority Ranking`
