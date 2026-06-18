---
name: woos-idea-to-design
description: Entry-point product workflow from raw idea to validated product design artifacts. Stops at reviewed PRD readiness and does not include engineering implementation.
version: 4.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [idea, prd, design, review, workflow, product]
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
      - woos-prd-authoring
      - woos-product-prd-review-gate
      - woos-ui-design-brief
      - woos-ui-brief-review
      - woos-prd-consistency-audit
      - woos-version-integration-audit
---

# Idea-to-Design

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
Lite:     Capture → Lightweight PRD Package
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
**Output:** `docs/prd/<version>/<feature-id>.md`
**Optional Output:** `docs/design/<version>/<feature-id>-ui-brief.md`
**Interface Summary:** `docs/prd/<version>/<feature-id>-interface.md` (Strict only)

## Completion

This skill is complete when the selected scope has finished the product-design flow for its mode:

- Lite → PRD ready
- Standard → PRD review passed
- Strict → all features pass analyze gate and required integration audit passes

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
    ├── woos-prd-authoring
    ├── woos-product-prd-review-gate
    ├── woos-ui-design-brief
    ├── woos-ui-brief-review
    ├── woos-prd-consistency-audit
    └── woos-version-integration-audit
```
