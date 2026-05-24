# Product Design Workflow

A skill-driven product design pipeline for AI coding agents. Takes a raw idea from capture through research, PRD, review gates, and delivers a build-ready handoff to engineering.

## Purpose

This workflow enforces structured product thinking before code is written. It ensures:

- **WHAT/WHY** is fully defined before engineering decides **HOW**
- Every decision is documented and traceable (roadmap → requirements → PRD → handoff)
- Quality gates prevent weak specs from reaching engineering
- Cross-feature consistency is validated before build starts

## Quick Start

1. Start a conversation with the agent and describe your idea
2. The agent activates `woos-idea-to-delivery` (entry point skill)
3. Follow the guided flow — the agent handles orchestration, sub-agent dispatch, and gating

**Trigger phrases:** "I have an idea for...", "let's build...", "design this feature", "start V1"

## Workflow Flowchart

```
                         ┌─────────────┐
                         │  Raw Idea   │
                         └──────┬──────┘
                                │
                    ┌───────────▼───────────┐
                    │   Phase 1: Capture    │
                    │  (woos-idea-capture)  │
                    └───────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │  Trivially simple?  │
                     └──┬──────────────┬───┘
                   Yes  │              │  No
                        │              │
              ┌─────────▼──┐   ┌───────▼──────────────┐
              │ User says  │   │   Phase 2: Discovery  │
              │"confirm    │   │ (woos-product-discovery)│
              │  Lite"     │   └───────────┬───────────┘
              └─────┬──────┘               │
                    │          ┌────────────▼────────────┐
                    │          │  🚦 Human Approval Gate │
                    │          │  Show full roadmap +    │
                    │          │  architecture, wait for │
                    │          │  "start PRD"            │
                    │          └────────────┬────────────┘
                    │                      │
                    │          Mode inferred from roadmap:
                    │          • Single feature → Standard
                    │          • Multi-feature → Strict
                    │                      │
          ┌─────────▼──────────────────────▼────────┐
          │       Phase 3: Product Design Flow      │
          │      (woos-product-design-flow)         │
          │                                         │
          │  ┌─────────────────────────────────┐    │
          │  │  Per Feature (Standard/Strict): │    │
          │  │                                 │    │
          │  │  Step 1: Select Version Scope   │    │
          │  │  Step 2: Requirement Contract   │    │
          │  │  Step 3: Priority Ranking  [S]  │    │
          │  │  Step 4: PRD Authoring          │    │
          │  │  Step 5: PRD Review Gate        │    │
          │  │  Step 6: UI Brief         [S]   │    │
          │  │  Step 7: UI Brief Review  [S]   │    │
          │  │  Step 8: Build Handoff          │    │
          │  │  Step 9: Readiness Check        │    │
          │  └─────────────────────────────────┘    │
          │                                         │
          │  Step 10: Version Integration Gate [S]  │
          │  (Cross-feature audit after ALL pass)   │
          └─────────────────┬───────────────────────┘
                            │
               ┌────────────▼────────────┐
               │  Build-Ready Handoff    │
               │  → Engineering Stage    │
               └─────────────────────────┘

  [S] = Strict mode only
  Standard: Steps 1, 2, 4, 5, 8, 9
  Lite: Mission → Tasks → AC → Handoff (no gates)
```

## Phase Breakdown

### Phase 1 — Capture (`woos-idea-capture`)

**What:** Transform a raw idea into a structured document through guided interview.

- Mode-agnostic — just gathers product intent
- Assesses complexity to decide Lite branch vs full flow
- Output: `ideas/<slug>/00-idea-capture.md`

### Phase 2 — Discovery (`woos-product-discovery`)

**What:** Research the problem space, produce a roadmap and architecture overview.

- Competitive analysis, landscape research
- Versioned product roadmap with feature prioritization
- System architecture overview (components, boundaries)
- Internal review gates: Roadmap Review + Architecture Review
- Ends with **🚦 Human Approval Gate** — mandatory human review before proceeding

### Phase 3 — Design Flow (`woos-product-design-flow`)

**What:** Turn the roadmap into build-ready specs. This is the core orchestrator.

| Step | Name | What It Does |
|------|------|--------------|
| 1 | Select Version Scope | Extract features from roadmap, confirm boundaries |
| 2 | Requirement Contract | Structured requirements per template (goals, AC, risks) |
| 3 | Priority Ranking | MoSCoW/RICE/Kano ranking, P0/P1/P2 cut-line |
| 4 | PRD Authoring | Full PRD following template (user stories, flows, edge cases, metrics) |
| 5 | PRD Review Gate | Phase A: structural check + Phase B: 7-item quality checklist |
| 6 | UI Brief | Visual direction, wireframes, interaction patterns |
| 7 | UI Brief Review | Accessibility, consistency, completeness review |
| 8 | Build Handoff | Package everything into a single handoff file for engineering |
| 9 | Readiness Check | Final validation: AC testable, flows complete, no gaps |
| 10 | Integration Gate | Deep cross-feature audit (shared concepts, constants, API contracts) |

## Three Execution Modes

| Mode | When | Steps | Review Gates |
|------|------|-------|--------------|
| **Lite** | Trivially simple, < 2 days work | Mission → Tasks → AC → Handoff | None |
| **Standard** | Single feature, moderate complexity | 1 → 2 → 4 → 5 → 8 → 9 | PRD Review |
| **Strict** | Multi-feature, UX-heavy, high-risk | 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 | All gates |

**Mode is NOT chosen upfront.** It's determined at two natural points:
1. After Capture: trivial → Lite (user confirms)
2. After Discovery: inferred from roadmap content (single feature = Standard, multi-feature = Strict)

## Enforcement Rules

The workflow includes 6 non-negotiable enforcement rules (E1–E6) to prevent agents from cutting corners:

- **E1:** No step merging — each step = separate output file
- **E2:** Output validation gate — file must exist before advancing
- **E3:** Template compliance — required sections verified by heading
- **E4:** Full checklist in reviews — every criterion checked, no blanket passes
- **E5:** No silent step skipping — failures are fixed, not skipped
- **E6:** No self-review — fresh sub-agent for every review

## Skill Map

| Skill | Role |
|-------|------|
| `woos-idea-to-delivery` | **Entry point** — umbrella orchestrator, tier routing |
| `woos-idea-capture` | Phase 1 — idea interview and structuring |
| `woos-product-discovery` | Phase 2 — research, roadmap, architecture |
| `woos-product-design-flow` | Phase 3 — PRD pipeline orchestrator |
| `woos-ui-design-brief` | Step 6 — UI direction and wireframes |
| `woos-build-handoff` | Step 8 — handoff packaging |

## Key Design Principles

1. **Product defines WHAT/WHY, Engineering decides HOW** — no architecture in PRD
2. **File-based handoff** — all state in human-readable markdown, version-controllable
3. **Independent reviewers** — fresh sub-agent context for every review gate
4. **Template-driven** — mandatory templates with `[NEEDS CLARIFICATION: ...]` markers
5. **Human-in-the-loop** — mandatory approval gate before PRD phase begins
6. **Bidirectional feedback** — engineering can issue Design Change Requests (DCR) back to product
