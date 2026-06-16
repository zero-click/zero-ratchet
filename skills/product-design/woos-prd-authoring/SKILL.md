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

- `references/framework-prd.md` — authoring framework / reference reading
- `templates/prd-template.md` — **the authoring template; the output PRD MUST match this template's section structure** (Background / User Personas / Functional Requirements / Non-Functional Requirements / User Flows / Edge Cases / Non-Goals / Success Metrics). This template is the source of truth for Step 4's section checks.
- `docs/prd/<version>/<feature-id>-requirements.md`

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
2. `## Functional Requirements`
3. `## Non-Functional Requirements`
4. `## Edge Cases`
5. `## Non-Goals`
6. `## Success Metrics`

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
- Give full detail to `P0` scope; keep `P2` brief
- Mark unresolved items as `[NEEDS CLARIFICATION: ...]`
- Do not embed review verdicts or gate outcomes in the PRD itself
- Start from the actual problem, not from the template furniture
- In `## Background`, separate **observable problem**, **root cause / mismatch** (if known), **current workaround**, and **user impact**
- If a concrete system/channel/environment exposed the issue, explicitly say whether it is **the product problem itself** or **the current example that surfaced the general problem**
- Do NOT let sample paths, deployment conventions, or current operator habits harden into product requirements unless the feature truly depends on them
- Each FR should describe one capability or one relationship. Split FRs that combine multiple concerns such as precedence, routing, observability, fallback behavior, and scope boundaries
- Each FR MUST include at least one `**Consequences (testable):**` bullet — an atomic, observable condition with a concrete threshold or outcome. Phrases like "system handles X gracefully", "reasonable performance", or "user-friendly" are not consequences and MUST be rewritten as concrete bounds
- Use per-FR `**Out of Scope:**` to draw boundaries between adjacent FRs whenever confusion between them is plausible
- Any inference made without explicit user confirmation MUST be tagged inline with `[ASSUMPTION: <one-line statement>]` and surfaced in `## Assumptions Index`. Do not bury inferences in prose.
- **Inferences inherited from `requirements.md` are still inferences.** If a decision in the PRD cannot be traced to a direct quote in the original idea capture, the roadmap entry, or an explicit user confirmation in the conversation, it MUST be tagged `[ASSUMPTION]` — even when it appears verbatim in `requirements.md`. The requirements doc is AI-authored and does not count as ground truth.
- `## Success Metrics` MUST contain at least one quantitative primary metric with a target value, AND at least one counter-metric or explicit `[NEEDS CLARIFICATION: counter-metric]` tag. Bare bullets like "users complete without confusion" are not metrics.
- For internal tools or single-operator features, omit `User Personas` and `User Flows` rather than write trivial placeholders to satisfy a structural check
- Only include `Dependencies` when downstream planning or implementation genuinely depends on them
- Only include `Open Questions` when there are real unresolved decisions; do not use that section for rhetorical filler
