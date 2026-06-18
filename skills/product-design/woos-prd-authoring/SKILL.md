---
name: woos-prd-authoring
description: Write the per-feature PRD directly from the approved roadmap scope or Lite idea capture using the mandatory PRD template.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, prd, authoring, design-flow]
    related_skills:
      - woos-product-design-flow
      - woos-product-prd-review-gate
---

# PRD Authoring

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

Write a full PRD for one feature directly from the approved roadmap scope (Standard / Strict) or Lite idea capture.

## Required Load Set (mandatory)

- `references/framework-prd.md` — authoring framework / reference reading
- `templates/prd-template.md` — **the authoring template; the output PRD MUST match this template's section structure** (Background / Goals / User Personas / Functional Requirements / Non-Functional Requirements / MVP Scope / User Flows / Edge Cases / Non-Goals / Success Metrics). This template is the source of truth for Step 3's section checks.
- **Standard / Strict:** `docs/product/<project>-roadmap.md` + `docs/product/<project>-architecture.md`
- **Lite:** the idea capture file (`ideas/<slug>.md` or `ideas/<slug>/00-idea-capture.md`) in place of the roadmap/architecture pair

## Supplemental Reference (optional, do not author against)

- `references/template-prd-template.md` — a richer per-feature PRD reference (Vision / JTBD / UJ-N etc.) kept for context; **do not** use it as the section structure for the output PRD. When it conflicts with `templates/prd-template.md`, the template wins.

If any mandatory file is not loaded, return `BLOCKED`.

## Conditional Load Set (upstream dependencies)

When the orchestrator provides upstream interface summaries, also load:

- `docs/prd/<version>/<upstream-feature-id>-interface.md` for each declared upstream dependency

When referencing shared concepts (status enums, data models, event types, API endpoints), use the exact definitions from upstream interface summaries. Do NOT invent alternate names for concepts already defined upstream.

## Output

- `docs/prd/<version>/<feature-id>.md`

## Required Sections

1. `## Background`
2. `## Goals`
3. `## Functional Requirements`
4. `## Non-Functional Requirements`
5. `## MVP Scope`
6. `## Edge Cases`
7. `## Non-Goals`
8. `## Success Metrics`

## Conditionally Required Sections

- `## User Personas` — **required** when the feature has user-facing UI OR serves multiple distinct user types. **Optional** for internal-tool / single-operator / CLI features (in which case omit the section entirely rather than write a one-row table just to satisfy a check).
- `## User Flows` — same condition as `## User Personas`.
- `## Assumptions Index` — **required** whenever any `[ASSUMPTION: ...]` tag appears inline anywhere in the PRD. Every inline tag must be surfaced in the index for explicit confirmation. Omit only if the PRD contains no inline assumption tags.

The PRD MUST state its feature shape in a one-liner at the top of `## Background`, e.g. `Shape: internal-tool / single-operator` or `Shape: consumer-product / multi-stakeholder`. The review gate uses this to decide whether to enforce the conditional sections.

## Optional Sections

Include only when they add real decision value:

- `## Dependencies`
- `## Open Questions`

## Authoring Rules

- Follow the template exactly
- Use the roadmap entry (Standard / Strict) or idea capture file (Lite) as the product source of truth; do not invent an intermediate `requirements.md`
- Mark unresolved items as `[NEEDS CLARIFICATION: ...]`
- Do not embed review verdicts or gate outcomes in the PRD itself
- Start from the actual problem, not from the template furniture
- In `## Background`, separate **observable problem**, **root cause / mismatch** (if known), **current workaround**, and **user impact**
- If a concrete system/channel/environment exposed the issue, explicitly say whether it is **the product problem itself** or **the current example that surfaced the general problem**
- Do NOT let sample paths, deployment conventions, or current operator habits harden into product requirements unless the feature truly depends on them
- Each FR should describe one capability or one relationship. Split FRs that combine multiple concerns such as precedence, routing, observability, fallback behavior, and scope boundaries
- Each FR MUST include at least one `**Consequences (testable):**` bullet — an atomic, observable condition with a concrete threshold or outcome. Phrases like "system handles X gracefully", "reasonable performance", or "user-friendly" are not consequences and MUST be rewritten as concrete bounds
- Use per-FR `**Out of Scope:**` to draw boundaries between adjacent FRs whenever confusion between them is plausible
- `## Goals` states the product outcomes this feature is meant to move; `## MVP Scope` states what is in for this version, what is out, and the cut-line. This is where the old requirements-contract ranking now lives
- Any inference made without explicit user confirmation MUST be tagged inline with `[ASSUMPTION: <one-line statement>]` and surfaced in `## Assumptions Index`. Do not bury inferences in prose.
- If a decision in the PRD cannot be traced to a direct quote in the original idea capture, the roadmap entry, or an explicit user confirmation in the conversation, it MUST be tagged `[ASSUMPTION]`.
- `## Success Metrics` MUST contain at least one quantitative primary metric with a target value, AND at least one counter-metric or explicit `[NEEDS CLARIFICATION: counter-metric]` tag. Bare bullets like "users complete without confusion" are not metrics.
- For internal tools or single-operator features, omit `User Personas` and `User Flows` rather than write trivial placeholders to satisfy a structural check
- Only include `Dependencies` when downstream planning or implementation genuinely depends on them
- Only include `Open Questions` when there are real unresolved decisions; do not use that section for rhetorical filler
