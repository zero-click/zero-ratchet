---
name: woos-idea-to-delivery
description: End-to-end delivery flow from idea capture through PR. Bridges research agent (idea → product design → handoff) and coding agent (technical design → implement → verify → PR). Product side focuses on WHAT/WHY; engineering side focuses on HOW. Includes DCR feedback loop.
version: 3.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [delivery, idea, prd, design, handoff, review, workflow, end-to-end, dcr]
    related_skills:
      - woos-idea-capture
      - woos-product-discovery
      - woos-product-design-flow
      - woos-ui-design-brief
      - woos-build-handoff
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
Capture → Product Discovery → Product Design Flow (PRD → PRD Review → Handoff)
    ↓
[Engineering Side]
Technical Design → Implement → Verify → Code Review → PR
    ↓ (if design issue found)
DCR → back to Product Side
```

- PRD Review: independent sub-agent
- UI Brief: not included (Standard keeps scope tight)
- Code Review: dispatch independent reviewer
- DCR: available for product issues found during implementation

### Strict — Full Hard-Gate Flow

For: multi-feature versions, high-uncertainty, UX-heavy, or security/compliance-sensitive.

```text
[Product Side]
Capture → Product Discovery → Product Design Flow (Priority → PRD → [PRD Review] → UI Brief → [UI Review] → Analyze → Handoff → [Integration])
    ↓
[Engineering Side]
Technical Design → [Design Review] → TDD → Implement → Verify
→ [Security Review] → [Code Review] → PR
    ↓ (if design issue found)
DCR → back to Product Side
```

- All gates active, including security reviewer
- PRD Review: independent dispatch
- UI Brief: opt-in when feature has user-facing UI
- Analyze Gate + Version Integration Gate (multi-feature)
- Design Review (engineering side): independent dispatch
- DCR: mandatory for any product assumption violation

## Tier Selection — Timing & Confirmation

**⚠️ Mode is NOT decided at the start.** The flow is:

```text
1. Capture idea (mode-agnostic — just gather intent)
2. Product Discovery (research, roadmap, architecture)
3. 🚦 Human Approval Gate — present results + RECOMMEND a mode
4. User confirms mode → proceed to Product Design Flow in that mode
```

**Why:** You can't judge complexity before understanding the problem. Capture and Discovery run in a mode-agnostic way. Only after the user sees the full picture do they (and you) have enough information to choose.

**At the Human Approval Gate, present:**
1. Full roadmap + architecture files
2. Mode recommendation with rationale, using this guide:

```text
Is it a multi-feature version release?                → Strict
Is it security/compliance sensitive?                  → Strict
Is it high-uncertainty or UX-heavy?                   → Strict
Is it a normal single feature?                        → Standard
Is scope clear, single-purpose, low risk?             → Lite
Is it a typo/docs fix?                                → No workflow needed
```

3. Ask user: "建议使用 [X] 模式，是否同意？还是想用其他模式？"
4. User confirms → record mode in run-manifest → proceed

**Exception — Early Lite Detection:** If the idea is obviously trivial at Capture time (typo fix, 1-liner, user explicitly says "简单改个东西"), you MAY suggest Lite immediately and skip Discovery. But this still requires user confirmation.

## Phase Definitions

### Product Side (Research Agent)

#### Phase 1 — Capture & Interview

**Skill:** `woos-idea-capture`

- Captures raw idea through guided interview
- Determines scope and urgency
- Output: `ideas/<slug>/00-idea-capture.md`
- **User override:** `GREENLIGHT NEXT STAGE` skips remaining questions

#### Phase 2 — Product Discovery

**Skill:** `woos-product-discovery`

- Research existing landscape
- Competitive analysis
- Product roadmap with versioned delivery → **Roadmap Review Gate** (independent sub-agent)
- System architecture overview → **Architecture Review Gate** (independent sub-agent)
- Output: `docs/product/<project>-roadmap.md` + `docs/product/<project>-architecture.md`

**🚦 Human Approval Gate:** After Stage 2 completes, present FULL roadmap + architecture files to user. Do NOT proceed to Phase 3 until user explicitly approves (e.g., "开始拆 PRD").

**Lite: skip.**

#### Phase 3 — Product Design Flow

**Skill:** `woos-product-design-flow`

- Select version scope from roadmap
- Write requirements + PRD → **PRD Review Gate** (independent sub-agent)
- UI Design Brief (optional) → **UI Brief Review Gate** (independent sub-agent)
- Analyze gate (product consistency)
- Package into handoff

**Output:** `docs/handoff/<version>/<feature>.md`

**Lite: abbreviated** — only Mission + Tasks + AC + Verification.

**⚠️ Enforcement:** `woos-product-design-flow` has strict Enforcement Rules (E1–E6). Every step MUST produce its declared output file and pass structural validation before proceeding. No step merging, no skipping on failure, no partial reviews. See the skill for details.

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
│   ├── prd/<version>/<feature>.md           ← Phase 3 output
│   ├── design/
│   │   ├── <version>/<feature>-ui-brief.md ← Phase 3 output (Strict, optional)
│   │   └── <version>/<feature>.md          ← Phase 4 output (engineering)
│   ├── handoff/<version>/<feature>.md       ← Phase 3 output (main)
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
│   ├── Phase 1: woos-idea-capture
│   ├── Phase 2: woos-product-discovery
│   └── Phase 3: woos-product-design-flow
│       ├── woos-ui-design-brief (optional)
│       └── woos-build-handoff
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
