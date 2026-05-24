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

## BMAD Knowledge Architecture

This workflow adapts the [BMAD](https://github.com/bmad-agent/bmad-agent) methodology — a multi-agent product development framework — into a Hermes-native skill structure. BMAD provides three types of domain knowledge injected into sub-agents at dispatch time (per E7):

### Personas (Role Identity)

Each persona defines a sub-agent's identity, thinking style, communication principles, and behavioral constraints. Injected verbatim into the sub-agent prompt.

| Persona | File | Used In | Purpose |
|---------|------|---------|---------|
| **PM (John)** | `references/persona-pm.md` | Steps 2, 3, 4, 8 | Product thinking — "Why does this matter to users?" Drives requirements, PRD authoring, and handoff packaging |
| **Analyst** | `references/persona-analyst.md` | Discovery Steps 1–3 | Research-oriented — competitive analysis, market research, pain point extraction |
| **Architect** | `references/persona-architect.md` | Discovery Step 5 | System-level thinking — components, boundaries, data flow, technical risks |
| **UX Designer (Sally)** | `references/persona-ux-designer.md` | Steps 6, 7 | User experience — interaction patterns, accessibility, information hierarchy |
| **PRD Validator** | `references/persona-prd-validator.md` | Steps 5, 5R | Critical reviewer — finds gaps, contradictions, untestable criteria |

### Frameworks (Domain Knowledge)

Frameworks provide methodology and discipline for specific tasks. They define HOW to think about a problem, not just what to produce.

| Framework | File | Stage | Purpose |
|-----------|------|-------|---------|
| `framework-prd.md` | PRD discipline | Design Flow | "PRDs emerge from user interviews, not template filling." Shape → extract → validate cycle |
| `framework-validate-prd.md` | PRD validation | Design Flow | Review gate methodology — what makes a PRD "done" |
| `framework-ux-design.md` | UX design | Design Flow | UI brief authoring principles — layout, flows, accessibility |
| `framework-ux-validate.md` | UX validation | Design Flow | UI brief review methodology |
| `framework-epics-and-stories.md` | Story breakdown | Design Flow | How to decompose PRD into build tasks for handoff |
| `framework-implementation-readiness.md` | Readiness check | Design Flow | Criteria for "ready to hand to engineering" |
| `framework-market-research.md` | Market research | Discovery | Competitive landscape analysis methodology |
| `framework-competitive-analysis.md` | Competitive analysis | Discovery | Structured competitor evaluation framework |
| `framework-customer-pain-points.md` | Pain discovery | Discovery | User pain extraction and validation |
| `framework-create-architecture.md` | Architecture | Discovery | How to produce a system architecture overview |
| `framework-architecture-validation.md` | Architecture review | Discovery | 7-point architecture validation checklist |

### Templates (Output Structure)

Templates define the exact section structure sub-agents must follow. Checked by E3 (structural compliance).

| Template | File | Stage | Purpose |
|----------|------|-------|---------|
| `template-prd-template.md` | PRD structure | Design Flow | Mandatory sections: Background, Personas, FR, NFR, User Flows, Edge Cases, Metrics |
| `template-prd-validation-checklist.md` | Review structure | Design Flow / Discovery | Structured review output format |
| `template-brief-template.md` | Capture structure | Discovery | Idea capture output format |
| `requirements-template.md` | Requirements structure | Design Flow | Step 2 output: Problem, Goals, Stories, Constraints, Risks |
| `readiness-template.md` | Readiness structure | Design Flow | Step 9 output: Checklist + Verdict |

### Stage × Knowledge Matrix

| Stage | Personas Used | Frameworks Used | Purpose |
|-------|--------------|-----------------|---------|
| **Phase 1: Capture** | Analyst | — | Gather and structure raw idea |
| **Phase 2: Discovery** | Analyst, PM, Architect, PRD Validator | market-research, competitive-analysis, customer-pain-points, create-architecture, architecture-validation | Research problem space, produce roadmap + architecture |
| **Phase 3: Design Flow** | PM, UX Designer, PRD Validator | prd, validate-prd, ux-design, ux-validate, epics-and-stories, implementation-readiness | Write PRD, review, UI brief, package handoff |
