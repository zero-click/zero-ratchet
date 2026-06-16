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
