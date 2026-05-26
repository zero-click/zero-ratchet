---
name: woos-architecture-overview
description: Produce the high-level architecture overview used by downstream product design and engineering.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, discovery, architecture, overview]
    related_skills:
      - woos-product-discovery
---

# Architecture Overview

## Purpose

Produce the high-level solution architecture for the roadmap scope.

## Required Load Set (mandatory)

- `references/framework-create-architecture.md`
- `docs/product/<project>-roadmap.md`
- `ideas/<slug>/00-idea-capture.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/product/<project>-architecture.md`

## Required Coverage

1. Major components and boundaries
2. Communication patterns
3. Data architecture
4. Cross-feature infrastructure
5. Technology recommendations with rationale
6. System-level technical risks
