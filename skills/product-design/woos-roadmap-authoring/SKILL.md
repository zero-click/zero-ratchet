---
name: woos-roadmap-authoring
description: Turn capture and research inputs into a versioned product roadmap document.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, roadmap, planning, authoring]
    related_skills:
      - woos-product-discovery
---

# Roadmap Authoring

## Purpose

Synthesize discovery inputs into a roadmap that defines vision, scope, versioning, and success metrics.

## Required Load Set (mandatory)

- `references/framework-create-prd.md`
- `ideas/<slug>/00-idea-capture.md`
- `docs/research/<topic>.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/product/<project>-roadmap.md`

## Required Sections

1. Vision
2. User Personas
3. Core Experience
4. Versioned Roadmap
5. Constraints
6. Decision Log
