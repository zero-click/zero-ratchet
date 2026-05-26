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
2. The agent activates `woos-idea-to-design` (entry point skill)
3. Follow the guided flow — the agent handles orchestration, sub-agent dispatch where needed, direct script checks for mechanical steps, and gating

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
          │  ┌──────────────────────────────────┐   │
          │  │  Per Feature (Standard/Strict):  │   │
          │  │                                  │   │
          │  │  Step 1:  Select Version Scope   │   │
          │  │  Step 2:  Requirement Contract   │   │
          │  │  Step 3:  PRD Authoring          │   │
          │  │  Step 4:  PRD Review Gate   [S]  │   │
          │  │  Step 5:  UI Brief          [S]  │   │
          │  │  Step 5R: UI Brief Review   [S]  │   │
          │  │  Step 6:  Analyze Gate      [S]  │   │
          │  │  Step 7:  Build Handoff          │   │
          │  │  Step 8:  Readiness Check   [S]  │   │
          │  └──────────────────────────────────┘   │
          │                                         │
          │  Step 9: Version Integration Gate  [S]  │
          │  (Cross-feature audit after ALL pass)   │
          └─────────────────┬───────────────────────┘
                            │
               ┌────────────▼────────────┐
               │  Build-Ready Handoff    │
               │  → Engineering Stage    │
               └─────────────────────────┘

  [S] = Strict mode only
  Standard: Steps 1, 2, 3, 4, 7, 8 (no UI or Integration path)
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
| 2 | Requirement Contract | `woos-requirement-contract` writes the per-feature requirements file including `P0/P1/P2` cut-line |
| 3 | PRD Authoring | `woos-prd-authoring` writes the PRD from the ranked requirements |
| 4 | PRD Review Gate | Isolated subagent runs dedicated review skill and returns `PASS` or `REQUEST_CHANGES` |
| 5 | UI Brief | Visual direction, wireframes, interaction patterns |
| 5R | UI Brief Review | Isolated subagent runs the dedicated UI review skill |
| 6 | Analyze Gate | Isolated subagent runs the audit skill with script-assisted consistency review |
| 7 | Build Handoff | Package everything into a single handoff file for engineering |
| 8 | Readiness Check | Isolated subagent runs the readiness audit skill |
| 9 | Integration Gate | Isolated subagent runs the cross-feature integration audit skill |

The orchestrator now only routes steps, validates outputs, and controls transitions. Review and audit gates (Steps 4, 5R, 6, 8, 9) must run in isolated subagent contexts so their skill loads stay out of the orchestrator context. Analyze, readiness, and integration still use a two-phase path: scripts extract complete structured data first, then the audit skill performs semantic comparison and writes the final judgment.

## Three Execution Modes

| Mode | When | Steps | Review Gates |
|------|------|-------|--------------|
| **Lite** | Trivially simple, < 2 days work | Mission → Tasks → AC → Handoff | None |
| **Standard** | Single feature, moderate complexity | 1 → 2 → 3 → 4 → 7 → 8 | PRD Review |
| **Strict** | Multi-feature, UX-heavy, high-risk | 1 → 2 → 3 → 4 → 5 → 5R → 6 → 7 → 8 → 9 | All gates |

**Mode is NOT chosen upfront.** It's determined at two natural points:
1. After Capture: trivial → Lite (user confirms)
2. After Discovery: inferred from roadmap content (single feature = Standard, multi-feature = Strict)

## Enforcement Rules

The workflow includes 6 non-negotiable enforcement rules (P0–P5) to prevent agents from cutting corners:

- **P0:** Explicit step dispatch — state the skill, inputs, and output before each step
- **P1:** Orchestrator does NOT create artifacts — only version scope selection stays direct
- **P2:** No step merging or silent skipping — each step has its own verified output
- **P3:** Output validation — file must exist and carry the expected verdict/sections before advancing
- **P4:** No self-review — fresh dedicated skill for every review or audit
- **P5:** Mandatory subagent isolation — Steps 4, 5R, 6, 8, and 9 run in isolated subagent contexts

## Skill Map

| Skill | Role |
|-------|------|
| `woos-idea-to-design` | **Entry point** — umbrella orchestrator, tier routing |
| `woos-idea-capture` | Phase 1 — idea interview and structuring |
| `woos-product-discovery` | Phase 2 — research, roadmap, architecture |
| `woos-problem-validation` | Discovery Step 1 — validate whether the problem is worth solving |
| `woos-product-research` | Discovery Step 2 — market, competitive, and feasibility research |
| `woos-roadmap-authoring` | Discovery Step 3 — roadmap authoring |
| `woos-roadmap-review-gate` | Discovery Step 3R — roadmap review gate |
| `woos-architecture-overview` | Discovery Step 4 — high-level architecture authoring |
| `woos-architecture-review-gate` | Discovery Step 4R — architecture review gate |
| `woos-product-design-flow` | Phase 3 — PRD pipeline orchestrator |
| `woos-requirement-contract` | Design Flow Step 2 — requirements contract authoring |
| `woos-prd-authoring` | Design Flow Step 3 — PRD authoring |
| `woos-product-prd-review-gate` | Step 4 — isolated PRD review gate |
| `woos-ui-design-brief` | Step 5 — UI direction and wireframes |
| `woos-ui-brief-review` | Step 5R — isolated UI brief review gate |
| `woos-prd-consistency-audit` | Step 6 — PRD/UI consistency audit |
| `woos-build-handoff` | Step 7 — handoff packaging |
| `woos-handoff-readiness-check` | Step 8 — handoff readiness gate |
| `woos-version-integration-audit` | Step 9 — cross-feature integration audit |

## Key Design Principles

1. **Product defines WHAT/WHY, Engineering decides HOW** — no architecture in PRD
2. **File-based handoff** — all state in human-readable markdown, version-controllable
3. **Independent reviewers** — fresh sub-agent context for every review gate; mechanical checks stay local/scripted
4. **Template-driven** — mandatory templates with `[NEEDS CLARIFICATION: ...]` markers
5. **Human-in-the-loop** — mandatory approval gate before PRD phase begins
6. **Bidirectional feedback** — engineering can issue Design Change Requests (DCR) back to product

## BMAD Knowledge Architecture

This workflow adapts the [BMAD](https://github.com/bmad-agent/bmad-agent) methodology — a multi-agent product development framework — into a Hermes-native skill structure. BMAD provides three types of domain knowledge used by the orchestrator and injected verbatim for sub-agent steps:

### Personas (Role Identity)

Each persona defines an execution lens for authoring or review steps that still need an explicit role stance.

| Persona | File | Used In | Purpose |
|---------|------|---------|---------|
| **PM (John)** | local to `woos-build-handoff` | Design Flow Step 7 | Product thinking — "Why does this matter to users?" Shapes handoff packaging |
| **UX Designer (Sally)** | local to `woos-ui-design-brief` / `woos-ui-brief-review` | Design Flow Steps 5, 5R | User experience — interaction patterns, accessibility, information hierarchy |
| **PRD Validator** | local to `woos-roadmap-review-gate` / `woos-product-prd-review-gate` | Discovery Step 3R, Design Flow Step 4 | Critical reviewer — finds gaps, contradictions, untestable criteria |

### Frameworks (Domain Knowledge)

Frameworks provide methodology and discipline for specific tasks. They define HOW to think about a problem, not just what to produce.

| Framework | File | Stage | Purpose |
|-----------|------|-------|---------|
| `framework-prd.md` | local to `woos-requirement-contract` / `woos-prd-authoring` | Design Flow | "PRDs emerge from user interviews, not template filling." Shape → extract → validate cycle |
| `framework-ux-design.md` | UX design | Design Flow | Dual-spine model (DESIGN.md + EXPERIENCE.md), elicit-not-impose, surface closure |
| `framework-ux-validate.md` | UX validation | Design Flow | UI brief review methodology |
| `framework-epics-and-stories.md` | local to `woos-build-handoff` | Design Flow | User-value grouping, standalone epics, FR coverage tracking |
| `framework-implementation-readiness.md` | Readiness check | Design Flow | Four-layer validation, traceability matrix, gap documentation |
| `framework-market-research.md` | Market research | Discovery | Scope clarification, multi-angle research, synthesis |
| `framework-competitive-analysis.md` | Competitive analysis | Discovery | Competitor identification, SWOT, differentiation strategy |
| `framework-customer-pain-points.md` | Pain discovery | Discovery | Pain categories, evidence classification, prioritization matrix |
| `framework-create-prd.md` | Roadmap authoring | Discovery | Discovery process, PRD discipline, versioned roadmap, decision log |
| `framework-create-architecture.md` | Architecture | Discovery | Requirements extraction, scale assessment, patterns, version alignment |
| `framework-architecture-validation.md` | Architecture review | Discovery | Coherence, coverage, readiness validation + completeness checklist |

### Templates (Output Structure)

Templates define the exact section structure outputs must follow. Checked by P3 (structural compliance).

| Template | Location | Stage | Purpose |
|----------|----------|-------|---------|
| `template-prd-template.md` | local to `woos-prd-authoring` | Design Flow | Mandatory sections: Background, Personas, FR, NFR, User Flows, Edge Cases, Metrics |
| `template-prd-validation-checklist.md` | local to `woos-product-prd-review-gate` | Design Flow | Structured PRD review output format |
| `requirements-template.md` | local to `woos-requirement-contract` | Design Flow | Step 2 output: Problem, Goals, Stories, Constraints, Risks |
| `readiness-template.md` | local to `woos-handoff-readiness-check` | Design Flow | Step 9 output: Checklist + Verdict |

### Stage × Knowledge Matrix

| Stage | Personas Used | Frameworks Used | Purpose |
|-------|--------------|-----------------|---------|
| **Phase 1: Capture** | — | — | Gather and structure raw idea |
| **Phase 2: Discovery** | Analyst, PM, Architect, PRD Validator | customer-pain-points, market-research, competitive-analysis, create-prd, create-architecture, architecture-validation | Research problem space, produce roadmap + architecture |
| **Phase 3: Design Flow** | PM, UX Designer, PRD Validator | prd, ux-design, ux-validate, epics-and-stories, implementation-readiness | Write PRD, review, UI brief, package handoff |
