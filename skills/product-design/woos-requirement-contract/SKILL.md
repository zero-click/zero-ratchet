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

- `references/framework-requirements.md`
- `templates/requirements-template.md`
- **Standard / Strict:** `docs/product/<project>-roadmap.md`
- **Lite:** the idea capture file (`ideas/<slug>.md` for Quick Note, or `ideas/<slug>/00-idea-capture.md` for Guided Interview) in place of the roadmap

If the required input file for the active mode is not loaded, return `BLOCKED`. In Lite mode the absence of `docs/product/<project>-roadmap.md` is expected and is not a BLOCK condition; the orchestrator MUST tell this skill which mode it is running in.

## Conditional Load Set (upstream dependencies)

When the orchestrator identifies upstream dependencies (via Step 1.5), also load:

- `docs/prd/<version>/<upstream-feature-id>-interface.md` for each declared upstream dependency

These interface summaries define shared terminology, enums, data models, and API surfaces that this feature MUST align with. When writing requirements that reference shared concepts, use the exact names and definitions from the upstream interface summary.

## Output

- `docs/prd/<version>/<feature-id>-requirements.md`

## Required Sections

1. `## Problem Statement`
2. `## Goals`
3. `## User Stories`
4. `## Non-Goals`
5. `## Constraints`
6. `## Risks & Unknowns`
7. `## Priority Ranking`

## Conditionally Required Sections

- `## Assumptions Index` — **required** whenever any `[ASSUMPTION: ...]` tag appears inline anywhere in the document. Every inline tag must be surfaced for explicit confirmation. Omit only if no inline assumption tags are used.

## Optional Sections

Include only when they add real decision value:

- `## Open Questions`

## Authoring Rules

- Follow the template structure exactly
- Keep the file scoped to one feature only
- Mark unresolved items as `[NEEDS CLARIFICATION: ...]`
- Do not fold this output into the PRD
- Include an explicit `P0 / P1 / P2` ranking and ship cut-line in `## Priority Ranking`
- Write the actual problem in plain language before writing formal user stories
- Separate **observable problem**, **root cause / mismatch** (if known), **current workaround**, and **user impact**
- If a concrete channel / integration / environment exposed the issue, state whether it is **the problem itself** or merely **the current example that revealed the problem**
- Do NOT turn deployment conventions, sample paths, or current operator habits into product requirements unless the feature explicitly depends on them
- Each user story should express **one capability or relationship**; split stories that mix multiple decisions, precedence rules, observability requirements, and edge-case policy into separate stories
- Each user story MUST include at least one `**Consequences (testable):**` bullet — an atomic, observable condition with a concrete threshold or outcome. Reject "system handles X gracefully" style phrasing; rewrite as concrete bounds
- Use per-story `**Out of Scope:**` to draw boundaries when adjacent stories could be confused
- Any inference made without explicit user confirmation MUST be tagged inline with `[ASSUMPTION: <one-line statement>]` and surfaced in `## Assumptions Index` at the end. Do not let inferences hide in prose
- **The roadmap/idea-capture is the source of truth for "explicit user input".** Any decision in this requirements doc that cannot be traced to a direct quote in the roadmap entry (Standard/Strict) or the idea capture file (Lite) MUST be tagged `[ASSUMPTION]`. An inference is no less an inference just because it sounds reasonable.
- For internal tools or single-operator features, prefer concrete capability wording over inflated persona theater
- Only include `Open Questions` when there are real unresolved decisions that affect scope, sequencing, or acceptance
