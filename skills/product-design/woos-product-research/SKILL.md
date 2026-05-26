---
name: woos-product-research
description: Research the market, competitors, feasibility, and existing solutions to produce a product discovery research document.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, discovery, research, competitive-analysis]
    related_skills:
      - woos-product-discovery
---

# Product Research

## Purpose

Produce the research document that discovery uses to justify roadmap and architecture choices.

## Required Load Set (mandatory)

- `references/framework-market-research.md`
- `references/framework-competitive-analysis.md`
- `ideas/<slug>/00-idea-capture.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `docs/research/<topic>.md`

## Required Coverage

1. Market landscape
2. Competitive analysis
3. Technical feasibility
4. Existing solutions or reusable components
5. Risks and unknowns

Research must cite sources and include a recommendation.
