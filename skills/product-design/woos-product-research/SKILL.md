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
