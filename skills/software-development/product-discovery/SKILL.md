---
name: product-discovery
description: "Stage 1 of idea-to-delivery: transform a raw idea into a structured product roadmap with vision, user personas, versioned scope, constraints, and decision log. Includes idea capture, market research, constitution initialization, and roadmap authoring."
version: 2.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, discovery, roadmap, planning, research]
    stage: 1
    flow: idea-to-delivery-v2
---

# Product Discovery

## Purpose

Turn a fuzzy idea into an actionable product roadmap. This is **Stage 1** of the idea-to-delivery flow. Run once per project; subsequent versions iterate in Stage 2 (feature-design-flow).

## Project Root Requirement

**CRITICAL:** All file paths in this skill (`.hep/`, `docs/`, `ideas/`) are relative to a **project root directory**. The project root MUST be a real git repository (e.g. `~/code/my-project/`).

**DO NOT** write files to the kanban scratch workspace. The scratch workspace is temporary and will be garbage-collected after task completion.

If running via kanban:
1. If the task has a `workspace_path` pointing to a git repo, use that.
2. If the task is in scratch mode, **clone or create the target repo first**, then write all files there.
3. Ask the user for the project directory if not specified.

## When to Use

- User says "I want to build X" or shares a raw idea
- Starting a new project or major initiative
- Need to validate market/technical feasibility before committing

## When to Skip

Skip this stage when ALL of these are true:
- A product roadmap already exists at `docs/product/<project>-roadmap.md`
- Roadmap has clear versioned scope with success metrics
- Constitution file exists at `.hep/constitution.md`

If skipping, go directly to `feature-design-flow` (Stage 2).

## Steps

### Step 1: Idea Capture

**Skill:** `idea-capture`

Socratic interview the user (or parse a written idea) to extract:
- What problem is being solved
- For whom
- What "done" looks like at a high level
- Constraints and non-goals

**Output:** `ideas/<slug>/00-idea-capture.md` + `ideas/<slug>/README.md`

### Step 2: Research & Validation

**Skill:** `deep-research` (when scope needs thorough validation)

or just ask targeted questions (when scope is narrow).

Investigate:
- Market landscape and competitors
- Technical feasibility and architecture options
- Existing solutions or reusable components
- Risks and unknowns

**Output:** `docs/research/<topic>.md`

**Gate:** Research must cite sources and include a recommendation. If critical unknowns remain, flag them as blockers in the roadmap.

### Step 3: Constitution Initialization

**When:** First time this flow runs for a project. Skip if `.hep/constitution.md` already exists.

Create `.hep/constitution.md` with:
- Tech stack choices (language, framework, database, deployment)
- Architecture conventions (monorepo vs multi-repo, API style)
- Coding standards references
- Baseline decisions (what's default; deviations require ADR)
- Team conventions (naming, directory structure, testing requirements)

Source from:
- Existing codebase (if any)
- User preferences
- Research findings from Step 2

### Step 4: Run Initialization

**Skill:** `woos-run-orchestrator`

Initialize run state:
- Create `.hep/runs/<run_id>/run-manifest.yaml`
- Record run_id for cross-stage traceability
- 🆕 Set `checkpoints: [stage1-done]` in run-manifest

### Step 5: Product Vision & Roadmap

**Skill:** `woos-product-planning-workflow`

Synthesize everything into a single roadmap document:

```markdown
# <Project Name> — Product Roadmap

## Vision
(Who it's for, what problem, core value proposition)

## User Personas
(Target user profiles)

## Core Experience
(What the primary interaction feels like)

## Roadmap

### V1 — <MVP Name>
- Scope: (what's included)
- Core Features: (numbered list)
- Non-goals: (what's explicitly out of scope)
- Success Metrics: (how to measure success)
- Technical Constraints: (from constitution)

### V2 — <Expansion Name>
- Scope: ...
- Depends on V1: ...

### V3 — <Vision Name>
- ...

## Constraints
- Tech stack: (from constitution)
- Timeline: (if any)
- Resources: (if any)

## 🆕 Decision Log
| # | Decision | Rationale | Alternatives Considered |
|---|----------|-----------|------------------------|
| D1 | (e.g. use SQLite) | (e.g. local-first, zero deploy) | (e.g. PostgreSQL — too heavy) |

## Constitution Reference
- `.hep/constitution.md`
```

**Output:** `docs/product/<project-slug>-roadmap.md`

### Step 6: 🆕 Decision Log Initialization

Record key decisions made during discovery in the roadmap's Decision Log:
- Tech stack choices and why
- Scope inclusions/exclusions and why
- Architecture direction and why
- Market positioning decisions

Each entry must include:
- **Decision**: What was decided
- **Rationale**: Why (one sentence)
- **Alternatives Considered**: What else was on the table

This log is **append-only** across stages — Stage 2 and Stage 3 will add to it, never delete.

## Mode Selection

This stage has no Lite/Standard split. Either you do product discovery or you skip it.

If the idea is small enough to not warrant a full discovery, skip directly to `feature-design-flow` Lite mode.

## 🆕 Checkpoint: Stage 1 Completion

After roadmap is written, **pause and present to user**:

1. Output a concise roadmap summary:
   - Vision (1 sentence)
   - V1 scope (bullet list)
   - Key risks / open questions
   - Decision Log highlights
2. **Wait for user confirmation** before proceeding to Stage 2
3. If user wants changes → return to Step 5 (or Step 1 if fundamental)
4. If user confirms → mark run-manifest `stage1-status: completed`

**Checkpoint behavior is controlled by:** `run-manifest.yaml` → `checkpoints: [stage1-done]`

To skip checkpoint (fully autonomous): set `checkpoints: []` in run-manifest.

## Handoff to Next Stage

On completion, tell the user:
- Roadmap is ready at `docs/product/<project>-roadmap.md`
- Constitution is at `.hep/constitution.md`
- Next step: pick a version (e.g., V1) and invoke `feature-design-flow`

## File Layout

```text
<project-root>/
├── .hep/
│   ├── constitution.md
│   └── runs/<run_id>/run-manifest.yaml
├── docs/
│   ├── product/<project>-roadmap.md     ← main output (with Decision Log)
│   └── research/<topic>.md
└── ideas/
    └── <slug>/
        ├── 00-idea-capture.md
        └── README.md
```

## Failure Handling

| Situation | Action |
|-----------|--------|
| User can't articulate the idea | Ask simpler questions; offer examples |
| Research reveals infeasibility | Report findings honestly; suggest alternatives |
| Constitution conflicts with idea | Flag conflict; suggest ADR or scope change |
| Run orchestrator unavailable | Proceed without run_id; note in roadmap |
| User rejects roadmap at checkpoint | Return to Step 5 (or Step 1 if fundamental) |

## Cross-Stage Skills Used

| Skill | Purpose |
|-------|---------|
| `idea-capture` | Step 1 |
| `deep-research` | Step 2 |
| `woos-product-planning-workflow` | Step 5 |
| `woos-run-orchestrator` | Step 4 |
