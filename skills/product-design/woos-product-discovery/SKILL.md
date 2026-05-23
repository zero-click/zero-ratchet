---
name: woos-product-discovery
description: "Stage 1 of woos-idea-to-delivery: transform a raw idea into a structured product roadmap with vision, user personas, versioned scope, constraints, and decision log. Includes idea capture, market research, constitution initialization, and roadmap authoring."
version: 2.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, discovery, roadmap, planning, research]
    stage: 1
    flow: woos-idea-to-delivery-v2
---

# Product Discovery

## Purpose

Turn a fuzzy idea into an actionable product roadmap. This is **Stage 1** of the woos-idea-to-delivery flow. Run once per project; subsequent versions iterate in Stage 2 (woos-product-design-flow).

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

**Skill:** `woos-idea-capture`

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

### Step 3: Run Initialization

**Skill:** `woos-run-orchestrator`

Initialize run state:
- Create `.hep/runs/<run_id>/run-manifest.yaml`
- Record run_id for cross-stage traceability
- Set `checkpoints: [stage1-done]` in run-manifest

### Step 4: Product Vision & Roadmap

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
- Technical Constraints: (known from research)

### V2 — <Expansion Name>
- Scope: ...
- Depends on V1: ...

### V3 — <Vision Name>
- ...

## Constraints
- Timeline: (if any)
- Resources: (if any)
- Known technical constraints: (if any)

## Decision Log
| # | Decision | Rationale | Alternatives Considered |
|---|----------|-----------|------------------------|
| D1 | (e.g. use SQLite) | (e.g. local-first, zero deploy) | (e.g. PostgreSQL — too heavy) |
```

**Output:** `docs/product/<project-slug>-roadmap.md`

### Step 4R: Roadmap Review Gate

**Reviewer:** Independent sub-agent dispatched in fresh context (product-strategist persona).

**Checklist:**

| # | Criterion | What to check |
|---|-----------|---------------|
| R1 | Vision differentiated | Not generic — clearly states what makes this product unique |
| R2 | Versioning logical | V1 is truly minimal; each version builds on prior without circular deps |
| R3 | Metrics measurable | Success metrics are specific numbers or observable behaviors |
| R4 | Non-goals effective | Actually prevent scope creep (not vague disclaimers) |
| R5 | Decision Log sound | Rationale isn't circular; alternatives are real options considered |
| R6 | Personas grounded | Based on real user behavior, not hypothetical ideal users |

**Dispatch:** `delegate_task` → fresh context, product-strategist role, read only roadmap + idea-capture.

**Review Findings Output:** `docs/reviews/<project>-roadmap-review-rN.md`

```markdown
# Roadmap Review — Round N

| # | Criterion | Status | Finding | Fixed? |
|---|-----------|--------|---------|--------|
| R1 | Vision differentiated | ✅ PASS | — | — |
| R2 | Versioning logical | ❌ FAIL | "V1 includes auth + payments — too large for MVP" | ☐ |
| R3 | Metrics measurable | ❌ FAIL | "DAU target missing a number" | ☐ |
| R4 | Non-goals effective | ✅ PASS | — | — |
| R5 | Decision Log sound | ✅ PASS | — | — |
| R6 | Personas grounded | ❌ FAIL | "Persona assumes all users are technical" | ☐ |

## Summary
PASS: 3/6 | FAIL: 3/6 → REQUEST_CHANGES
```

**Flow:**
1. Reviewer outputs findings with ❌/✅ per criterion
2. Author agent fixes each ❌ item, marks `Fixed? ☑` in findings file
3. Re-review: reviewer checks only `Fixed? ☑` rows — verifies fix is adequate
4. New issues found during re-review → append as new rows

**Results:**
- **PASS** → all criteria ✅ → proceed to Step 5
- **REQUEST_CHANGES** → return to Step 4, fix per findings checklist

Max 2 rounds. If no convergence → ask user for direction.

### Step 5: System Architecture Overview

After the roadmap is defined, produce a high-level system architecture that spans all planned versions. This prevents per-feature designs from conflicting later.

**Must answer:**
- What are the major system components/services?
- How do they communicate? (API, events, shared DB, etc.)
- What is the data architecture? (storage types, data flow)
- What cross-feature infrastructure is needed? (auth, queues, event bus, etc.)
- Which features have architectural coupling and must be co-designed?
- What are the system-level technical risks?

**Does NOT answer:**
- Detailed per-feature design (that's Stage 2)
- Specific code structure or file layout
- Implementation timeline (that's the roadmap)

**Output:** `docs/product/<project-slug>-architecture.md`

```markdown
# <Project Name> — System Architecture

## Overview
High-level system diagram description.

## Components
| Component | Responsibility | Interfaces |
|-----------|---------------|------------|
| ... | ... | ... |

## Data Architecture
- Storage types and boundaries
- Data flow between components

## Shared Infrastructure
- Auth/identity
- Messaging/events
- Observability

## Cross-Feature Dependencies
Which features share components or data, and what coordination is needed.

## Technical Risks
System-level risks that affect multiple features.

## Architecture Decisions
| # | Decision | Rationale | Alternatives |
|---|----------|-----------|-------------|
| A1 | ... | ... | ... |
```

### Step 5R: Architecture Review Gate

**Reviewer:** Independent sub-agent dispatched in fresh context (system-architect persona).

**Checklist:**

| # | Criterion | What to check |
|---|-----------|---------------|
| A1 | Component boundaries | Each component has clear single responsibility, no overlap |
| A2 | Communication consistency | Patterns are uniform (not mixing REST + gRPC + events without reason) |
| A3 | Data decoupling | No unnecessary shared state between features |
| A4 | Infrastructure proportional | Shared infra justified for V1 scope (not over-engineered) |
| A5 | Dependencies manageable | Cross-feature deps are identified and don't block independent delivery |
| A6 | Risks realistic | Not alarmist or dismissive; actionable mitigations exist |
| A7 | Version-aligned | V1 can ship without V2's components being built |

**Dispatch:** `delegate_task` → fresh context, system-architect role, read roadmap + architecture.

**Review Findings Output:** `docs/reviews/<project>-architecture-review-rN.md`

```markdown
# Architecture Review — Round N

| # | Criterion | Status | Finding | Fixed? |
|---|-----------|--------|---------|--------|
| A1 | Component boundaries | ✅ PASS | — | — |
| A2 | Communication consistency | ❌ FAIL | "Auth uses REST but notifications use WebSocket push without justification" | ☐ |
| A3 | Data decoupling | ✅ PASS | — | — |
| A4 | Infrastructure proportional | ❌ FAIL | "Event bus overkill for V1 — only 2 producers" | ☐ |
| A5 | Dependencies manageable | ✅ PASS | — | — |
| A6 | Risks realistic | ✅ PASS | — | — |
| A7 | Version-aligned | ✅ PASS | — | — |

## Summary
PASS: 5/7 | FAIL: 2/7 → REQUEST_CHANGES
```

**Flow:**
1. Reviewer outputs findings with ❌/✅ per criterion
2. Author agent fixes each ❌ item, marks `Fixed? ☑` in findings file
3. Re-review: reviewer checks only `Fixed? ☑` rows — verifies fix is adequate
4. New issues found during re-review → append as new rows

**Results:**
- **PASS** → all criteria ✅ → proceed to Step 6
- **REQUEST_CHANGES** → return to Step 5, fix per findings checklist

Max 2 rounds. If no convergence → ask user for direction.

### Step 6: Decision Log Initialization

Record key decisions made during discovery in the roadmap's Decision Log:
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

## Checkpoint: Stage 1 Completion

After roadmap + architecture are written, **pause and present to user**:

1. Output a concise summary:
   - Vision (1 sentence)
   - V1 scope (bullet list)
   - Architecture overview (key components)
   - Key risks / open questions
   - Decision Log highlights
2. **Wait for user confirmation** before proceeding to Stage 2
3. If user wants changes → return to relevant step
4. If user confirms → mark run-manifest `stage1-status: completed`

**Checkpoint behavior is controlled by:** `run-manifest.yaml` → `checkpoints: [stage1-done]`

To skip checkpoint (fully autonomous): set `checkpoints: []` in run-manifest.

## Handoff to Next Stage

On completion, tell the user:
- Roadmap is ready at `docs/product/<project>-roadmap.md`
- Architecture overview is at `docs/product/<project>-architecture.md`
- Next step: pick a version (e.g., V1) and invoke `woos-product-design-flow`

## File Layout

```text
<project-root>/
├── .hep/
│   └── runs/<run_id>/run-manifest.yaml
├── docs/
│   ├── product/
│   │   ├── <project>-roadmap.md        ← roadmap output (with Decision Log)
│   │   └── <project>-architecture.md   ← system architecture output
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
| Run orchestrator unavailable | Proceed without run_id; note in roadmap |
| User rejects roadmap at checkpoint | Return to relevant step |
| Architecture too uncertain | Flag as risk; proceed with assumptions documented |

## Cross-Stage Skills Used

| Skill | Purpose |
|-------|---------|
| `woos-idea-capture` | Step 1 |
| `deep-research` | Step 2 |
| `woos-run-orchestrator` | Step 3 |
| `woos-product-planning-workflow` | Step 4 |
| `woos-run-orchestrator` | Step 4 |
