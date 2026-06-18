---
name: woos-requirement-contract
description: 'DEPRECATED — BMAD-style single-PRD flow now embeds requirements directly in the PRD; retained only as a legacy compatibility marker.'
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

# DEPRECATED — Requirement Contract

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


This skill is deprecated.

Hermes now follows the BMAD-style artifact boundary:

```text
idea capture / roadmap
→ PRD (requirements live here)
→ architecture
→ epics / stories
```

New product-design flows MUST NOT create a parallel per-feature `*-requirements.md` file.

## Purpose

Retained only so older conversations or references can explain the historical workflow. New work should go directly to `woos-prd-authoring`.

## Behavior

If invoked:

1. Explain that the per-feature requirements contract has been merged into the PRD
2. Point the caller to `woos-prd-authoring`
3. Return `BLOCKED` unless the caller is explicitly migrating legacy docs

## Migration Rule

- Move problem statement, goals, scope, and ranking into the PRD itself (`## Background`, `## Goals`, `## MVP Scope`, `## Non-Goals`, `## Success Metrics`)
- Keep architecture in `docs/product/<project>-architecture.md`
- Keep engineering decomposition downstream in the engineering workflow
