# Product Design Workflow

[English](./README.md) | [中文](./README.zh.md)

The product half of the pipeline. Takes a raw idea through capture → discovery → PRD, with review gates and a mandatory human approval point before engineering touches code.

Entry skill: **`woos-idea-to-design`** (umbrella orchestrator).

## Quick Start

Describe an idea to the agent — trigger phrases like "I have an idea for…", "let's build…", "design this feature", "start V1" route to `woos-idea-to-design`. The orchestrator handles phase progression, sub-agent dispatch, and gating. You only get prompted at decision points.

## Pipeline

```
Raw idea
   │
   ▼  woos-idea-capture
ideas/<slug>/00-idea-capture.md
   │
   │  trivial? ─yes→ user confirms Lite ────────┐
   │                                            │
   ▼  woos-product-discovery                    │
docs/product/<project>-roadmap.md               │
docs/product/<project>-architecture.md          │
   │                                            │
   ▼  🚦 mandatory human approval               │
   │                                            │
   ▼  woos-product-design-flow                  │
docs/prd/<version>/<feature-id>.md  ◀───────────┘
docs/prd/<version>/<feature-id>-interface.md  (Strict only)
docs/design/<version>/<feature-id>-ui-brief.md  (when UI)
```

Mode is inferred automatically, not chosen manually:

| Mode | When | Phase 3 steps |
|------|------|---------------|
| Lite | Trivial, < 2 days | PRD |
| Standard | Single feature, moderate risk | PRD → PRD Review |
| Strict | Multi-feature, UX-heavy, high uncertainty | Full per-feature: PRD → PRD Review → UI → UI Review → Analyze → Interface Summary → Integration |

## Phase 1 — Capture

| | |
|---|---|
| Skill | `woos-idea-capture` |
| Does | Guided interview that turns a raw idea into a structured intent document |
| Output | `ideas/<slug>/00-idea-capture.md` |

## Phase 2 — Discovery

| | |
|---|---|
| Skill | `woos-product-discovery` (orchestrator) |
| Does | Validate the problem, research the space, produce a roadmap and an architecture sketch — each gated by independent review |
| Output | `docs/product/<project>-roadmap.md` + `docs/product/<project>-architecture.md` |
| Sub-skills | `woos-problem-validation`, `woos-product-research`, `woos-roadmap-authoring` (+ review gate), `woos-architecture-overview` (+ review gate) |
| Exit | 🚦 mandatory human approval before Phase 3 |

## Phase 3 — Design Flow

| | |
|---|---|
| Skill | `woos-product-design-flow` (orchestrator) |
| Does | Per-feature: turn the roadmap entry into a reviewed PRD (plus UI brief and interface summary in Strict mode) |
| Output | `docs/prd/<version>/<feature-id>.md` and friends |

Steps in Strict mode:

| Step | Skill / Action | Output |
|------|----------------|--------|
| 1 | Orchestrator selects version scope | — |
| 1.5 | Orchestrator analyzes feature dependencies, sets execution order | — |
| 2 | `woos-prd-authoring` | `<feature-id>.md` |
| 3 | `woos-product-prd-review-gate` (fresh context) | PRD review verdict |
| 4 | `woos-ui-design-brief` (when UI in scope) | `<feature-id>-ui-brief.md` |
| 4R | `woos-ui-brief-review` (fresh context) | UI review verdict |
| 5 | `woos-prd-consistency-audit` (fresh context) | Audit verdict |
| 5.5 | Orchestrator extracts shared interface contract | `<feature-id>-interface.md` |
| 6 | `woos-version-integration-audit` (fresh context, incremental from 2nd feature) | Integration verdict |

Lite and Standard run a subset — see the [`woos-product-design-flow` SKILL](./woos-product-design-flow/SKILL.md) for the per-mode step list.

After every feature: ⭐ checkpoint — deliver to engineering now or design the next feature first?

## Enforcement Rules (P0–P7)

Non-negotiable rules in `woos-product-design-flow` that prevent step-skipping, template ignorance, and shallow review:

| Rule | Principle |
|------|-----------|
| P0 | Explicit step dispatch — state skill, inputs, output before each step |
| P1 | Orchestrator does NOT author artifacts (except Steps 1, 1.5, 6.5) |
| P2 | No merging or skipping steps |
| P3 | Validate output file existence and structure before advancing |
| P4 | No self-review — every gate runs in fresh sub-agent context |
| P5 | Subagent isolation for Steps 4, 5R, 6, 7 |
| P6 | Fix propagation — any rename or change MUST be greped + synced across all version docs |
| P7 | Upstream interface awareness — downstream features receive upstream interface summaries |

## DCR (back from engineering)

Engineering issues a Design Change Request at `docs/feedback/<version>/<feature-id>-dcr-<NNN>.md` when implementation discovers a wrong product assumption. The orchestrator reads it, decides scope, and either updates the PRD directly (small) or re-runs from Step 3 / Step 5 (large).

## Knowledge Layer

The product flow is built on the [BMAD](https://github.com/bmad-agent/bmad-agent) methodology, surfaced through:

- **Personas** injected into specific review steps (UX Designer "Sally" for UI brief review, PRD Validator for PRD and roadmap review)
- **Frameworks** for PRD shaping, UX validation, market research, architecture coherence
- **Templates** with `[NEEDS CLARIFICATION: …]` markers that block weak specs from passing
- **Single-PRD artifact shape** — requirements live inside the PRD; architecture and story breakdown happen downstream rather than through a parallel per-feature `requirements.md`

Authoritative details live inside each skill's `SKILL.md` and the framework files referenced from there.
