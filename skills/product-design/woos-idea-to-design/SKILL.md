---
name: woos-idea-to-design
description: Entry-point product workflow from raw idea to validated product design artifacts. Stops at PRD/UI/handoff readiness and does not include engineering implementation.
version: 3.1.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [idea, prd, design, handoff, review, workflow, product]
    related_skills:
      - woos-idea-capture
      - woos-product-discovery
      - woos-problem-validation
      - woos-product-research
      - woos-roadmap-authoring
      - woos-roadmap-review-gate
      - woos-architecture-overview
      - woos-architecture-review-gate
      - woos-product-design-flow
      - woos-requirement-contract
      - woos-prd-authoring
      - woos-product-prd-review-gate
      - woos-ui-design-brief
      - woos-ui-brief-review
      - woos-prd-consistency-audit
      - woos-build-handoff
      - woos-handoff-readiness-check
      - woos-version-integration-audit
---

# Idea-to-Design

## Purpose

Transform a raw idea into validated product design artifacts.

This is the **product-side entry skill**. It stops at reviewed product outputs and does **not** include engineering implementation.

## Key Boundary

| Concern | Owned By | Examples |
|---------|----------|----------|
| WHAT to build | Research agent | User stories, acceptance criteria, UI flows, success metrics |
| WHY to build it | Research agent | Problem statement, user pain, business value |
| High-level solution shape | Research agent | Version-level architecture, major components, boundaries, key integration points |
| Detailed implementation design | Downstream engineering workflow | Data model, API design, code structure, tech stack choices |

The product side produces requirements, user experience direction, and a high-level architecture recommendation during Discovery. Detailed technical design happens later, outside this skill.

## Execution Tiers

```text
Lite:     Capture → Brief PRD / Lite Handoff
Standard: Capture → Discovery → Product Design Flow
Strict:   Capture → Discovery → Product Design Flow
```

## Tier Selection — Two Decision Points

```text
Capture
 ↓
Trivially simple? → Lite
Otherwise → Discovery
Discovery approved?
 → Single feature → Standard
 → Multi-feature / UX-heavy / high-risk → Strict
```

## Phase Definitions

### Phase 1 — Capture

**Skill:** `woos-idea-capture`
**Output:** `ideas/<slug>/00-idea-capture.md`
**Next:** Lite if trivially simple and approved; otherwise continue to Discovery.

### Phase 2 — Product Discovery

**Skill:** `woos-product-discovery`
**Output:** `docs/product/<project>-roadmap.md` + `docs/product/<project>-architecture.md`
**Next:** Wait for explicit human approval before PRD work begins.

### Phase 3 — Product Design Flow

**Skill:** `woos-product-design-flow`
**Output:** `docs/prd/<version>/<feature>.md`
**Optional Output:** `docs/design/<version>/<feature>-ui-brief.md`
**Final Output:** `docs/handoff/<version>/<feature>.md`

## Completion

This skill is complete when the selected scope has finished the product-design flow for its mode:

- Lite → lite product artifact ready
- Standard → handoff readiness passed
- Strict → all features pass readiness and required integration audit passes

## Skill Dependency Map

```text
idea-to-design entry skill
├── Phase 1: woos-idea-capture
├── Phase 2: woos-product-discovery
│   ├── woos-problem-validation
│   ├── woos-product-research
│   ├── woos-roadmap-authoring
│   ├── woos-roadmap-review-gate
│   ├── woos-architecture-overview
│   └── woos-architecture-review-gate
└── Phase 3: woos-product-design-flow
    ├── woos-requirement-contract
    ├── woos-prd-authoring
    ├── woos-product-prd-review-gate
    ├── woos-ui-design-brief
    ├── woos-ui-brief-review
    ├── woos-prd-consistency-audit
    ├── woos-build-handoff
    ├── woos-handoff-readiness-check
    └── woos-version-integration-audit
```
