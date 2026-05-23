---
name: idea-to-delivery
description: End-to-end delivery flow from idea capture through PR. Bridges research agent (idea → product design → handoff) and coding agent (technical design → implement → verify → PR). Product side focuses on WHAT/WHY; engineering side focuses on HOW. Includes DCR feedback loop.
version: 3.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [delivery, idea, prd, design, handoff, review, workflow, end-to-end, dcr]
    related_skills:
      - idea-capture
      - product-discovery
      - product-design-flow
      - ui-design-brief
      - build-handoff
      - woos-development-workflow
---

# Idea-to-Delivery

## Purpose

End-to-end flow from raw idea to merged PR, with a **bidirectional feedback loop** between research and coding agents.

Two agents collaborate through a file-based handoff:

- **Research agent** (product side): idea → product discovery → PRD → UI direction → handoff
- **Coding agent** (engineering side): technical design → implement → verify → PR
- **Feedback loop**: coding agent can issue Design Change Requests (DCR) back to research agent

This skill is the umbrella — it selects the execution tier, routes phases, and delegates to sub-skills.

## Key Boundary

| Concern | Owned By | Examples |
|---------|----------|----------|
| WHAT to build | Research agent | User stories, acceptance criteria, UI flows, success metrics |
| WHY to build it | Research agent | Problem statement, user pain, business value |
| HOW to build it | Coding agent | Architecture, data model, API design, tech stack choices |
| Technical conventions | Coding agent | Constitution (`.hep/constitution.md`), ADRs |

The product handoff defines requirements and user experience. Technical architecture is the engineering stage's responsibility.

## When to Use

Use when:

- User presents a new feature idea, product initiative, or behavior-changing request
- Work spans both product thinking and engineering implementation
- You need a structured flow from ideation to delivery

Skip when:

- Pure bugfix with clear scope → use `woos-development-workflow` Lite directly
- Typos, docs-only changes → no workflow needed
- Already have a PRD → jump to `woos-development-workflow` Standard/Strict

## Execution Tiers

Default: **Standard**.

### Lite — Quick Validation

For: small tools, bugfix with design questions, scope-clear small changes, low risk.

```text
Capture → PRD (brief) → Lite Handoff → Implement → Verify → PR
```

- Skips: product discovery, independent review gates, UI brief
- PRD is abbreviated (user stories + AC only)
- Handoff only 4 fields: Mission + Build Tasks + AC + Verification
- No DCR (handle small deviations inline)

### Standard — Default

For: normal features, cross-file changes, needs design clarity.

```text
[Product Side]
Capture → Product Discovery → Product Design Flow (PRD → UI Brief → Handoff)
    ↓
[Engineering Side]
Technical Design → Implement → Verify → Code Review → PR
    ↓ (if design issue found)
DCR → back to Product Side
```

- PRD Review: self-review with checklist
- UI Brief: optional (only for UI-heavy features)
- Code Review: dispatch independent reviewer
- DCR: available for product issues found during implementation

### Strict — Full Hard-Gate Flow

For: security-sensitive, compliance, high-risk changes.

```text
[Product Side]
Capture → Product Discovery → Product Design Flow (PRD → [PRD Review] → UI Brief → Handoff)
    ↓
[Engineering Side]
Technical Design → [Design Review] → TDD → Implement → Verify
→ [Security Review] → [Code Review] → PR
    ↓ (if design issue found)
DCR → back to Product Side
```

- All gates active, including security reviewer
- PRD Review: independent dispatch
- Design Review (engineering side): independent dispatch
- DCR: mandatory for any product assumption violation

## Tier Selection Guide

```text
Is it security/compliance sensitive?              → Strict
Is it a major initiative (multi-feature)?         → Standard (start with product-discovery)
Is it a normal feature?                           → Standard
Is scope clear, single-purpose, low risk?         → Lite
Is it a typo/docs fix?                            → No workflow needed
```

If unsure, start with Standard. User can override with `GREENLIGHT NEXT STAGE` to skip questions (NOT gates).

## Phase Definitions

### Product Side (Research Agent)

#### Phase 1 — Capture & Interview

**Skill:** `idea-capture`

- Captures raw idea through guided interview
- Determines scope and urgency
- Output: `ideas/<slug>/00-idea-capture.md`
- **User override:** `GREENLIGHT NEXT STAGE` skips remaining questions

#### Phase 2 — Product Discovery

**Skill:** `product-discovery`

- Research existing landscape
- Competitive analysis
- Product roadmap with versioned delivery
- System architecture overview (high-level, product-perspective)
- Output: `docs/product/<project>-roadmap.md`

**Lite: skip.**

#### Phase 3 — Product Design Flow

**Skill:** `product-design-flow`

- Select version scope from roadmap
- Write requirements + PRD
- PRD review (self-check or independent)
- UI Design Brief (optional, via `ui-design-brief`)
- Analyze gate (product consistency)
- Package into handoff

**Output:** `docs/handoff/<feature>-vN.md`

**Lite: abbreviated** — only Mission + Tasks + AC + Verification.

---

### Engineering Side (Coding Agent)

#### Phase 4 — Technical Design

**Skills:** `woos-feature-design`, `woos-design-review-gate`

- Read product handoff
- Design architecture, data model, API contracts
- Create/update Constitution (`.hep/constitution.md`) if needed
- Document technical decisions as ADRs
- Output: `docs/design/<feature>.md`

**Lite: skip** (implement directly from handoff).

#### Phase 5 — Implementation

**Skills:** `coding-standards`, `tdd-workflow` (Strict)

- Standard: implement from handoff + technical design
- Strict: TDD (write tests first)
- **If product issue discovered**: initiate DCR (Phase 7)

#### Phase 6 — Verify & PR

**Skills:** `verification-loop`, `woos-code-review-gate`, `woos-pr-readiness`

- Run tests, verify acceptance criteria
- Code review (independent dispatch)
- PR readiness check
- Output: PR ready to merge

---

### Feedback Loop

#### Phase 7 — Design Change Request (DCR)

**Trigger:** Coding agent discovers a product issue during implementation.

**Applicable modes:** Standard + Strict (Lite handles deviations inline).

**Flow:**
1. Coding agent writes `docs/feedback/<feature>-dcr.md`
2. DCR contains: issue description, impact scope, proposed resolution, priority
3. Research agent reads DCR and assesses
4. **Small change**: research agent updates handoff directly
5. **Large change**: research agent returns to Phase 3 (PRD or UI brief)

**DCR File Template:**

```markdown
# Design Change Request: <Feature Name>

## Issue
Description of the product assumption that doesn't hold.

## Impact
- Affected scope (which user stories/requirements)
- Risk level (Low / Medium / High)

## Proposed Resolution
Suggested change to product requirements or UI.

## Priority
- [ ] Blocking — cannot continue implementation
- [ ] Important — affects quality but not blocking
- [ ] Nice to have — improvement suggestion

## Research Agent Decision
(filled by research agent)
- [ ] Approved — update handoff
- [ ] Needs PRD revision — back to Phase 3
- [ ] Deferred — record but don't address this round
```

## Core Design Principles

| Dimension | Decision |
|-----------|----------|
| Agent boundary | research = idea→handoff (WHAT/WHY); coding = design→PR (HOW) |
| Handoff mechanism | File-based (Markdown artifacts), version-controlled |
| Execution modes | Lite / Standard / Strict, default Standard |
| Gate model | PASS / REQUEST_CHANGES (binary) |
| Override phrase | `GREENLIGHT NEXT STAGE` — skip questions, not gates |
| Feedback loop | DCR: coding → research (bidirectional) |
| Technical conventions | Engineering side only (Constitution, ADRs) |

## File Layout

```text
<project-root>/
├── docs/
│   ├── product/<project>-roadmap.md        ← Phase 2 output
│   ├── prd/<feature>.md                     ← Phase 3 output
│   ├── design/
│   │   ├── <feature>-ui-brief.md           ← Phase 3 output (optional)
│   │   └── <feature>.md                    ← Phase 4 output (engineering)
│   ├── handoff/<feature>-vN.md             ← Phase 3 output (main)
│   ├── feedback/<feature>-dcr.md           ← Phase 7 (DCR)
│   └── adr/ADR-001-*.md                    ← Phase 4 output (engineering)
├── .hep/
│   └── constitution.md                     ← Engineering conventions
└── ideas/
    └── <idea-slug>/00-idea-capture.md      ← Phase 1 output
```

## Skill Dependency Map

```text
idea-to-delivery (this skill)
├── [Product Side — Research Agent]
│   ├── Phase 1: idea-capture
│   ├── Phase 2: product-discovery
│   └── Phase 3: product-design-flow
│       ├── ui-design-brief (optional)
│       └── build-handoff
├── [Engineering Side — Coding Agent]
│   ├── Phase 4: woos-feature-design + woos-design-review-gate
│   ├── Phase 5: coding-standards / tdd-workflow
│   └── Phase 6: verification-loop + woos-code-review-gate + woos-pr-readiness
└── [Feedback Loop]
    └── Phase 7: DCR (built-in)
```

## Key Design Decisions

### D1: Product side defines WHAT, not HOW

Technical architecture, data models, API design are engineering decisions. The product handoff gives requirements and user experience direction — the coding agent decides implementation approach. This prevents premature technical commitment during product thinking.

### D2: Constitution is engineering-side only

Project conventions (`.hep/constitution.md`) are created and maintained by the engineering stage. Product side doesn't need to know or reference tech stack choices. This keeps product thinking pure and technology-agnostic.

### D3: File-based handoff

Files are human-readable, version-controllable, diffable. The handoff file is the single source of truth that bridges product and engineering.

### D4: Binary gate (PASS / REQUEST_CHANGES)

No PASS_WITH_NOTES. Notes go in findings but don't affect gate state. Reduces agent decision complexity.

### D5: Research agent does not code

Separation of concerns. Research agent value = product thinking + requirement quality. Mixing coding and product thinking leads to skipping requirement clarification.

### D6: Why DCR exists

Original flow was one-way (research → coding). But coding often discovers product assumptions that don't hold. DCR enables bidirectional communication without chaos.

### D7: UI Brief is optional

Not every feature has a user interface. API-only, CLI, background jobs — these skip the UI brief step entirely. The flow adapts to what's needed.
