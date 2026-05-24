---
name: woos-product-discovery
description: "Stage 1 orchestrator: transform a raw idea into a validated product roadmap. Dispatches sub-agents per step with domain knowledge. Technical architecture belongs in engineering phase."
version: 3.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, discovery, roadmap, planning, research, orchestrator]
    stage: 1
    flow: woos-idea-to-delivery
---

# Product Discovery (Orchestrator)

> **🚨 STOP. Read this section FIRST. It overrides any instinct to "just do the work yourself."**
>
> You are an ORCHESTRATOR. You do NOT produce research or roadmaps yourself.
> You dispatch sub-agents and validate their outputs. That is your ONLY job.
>
> Before EVERY step: output a Pre-flight block (see below). No pre-flight = invalid execution.

## ⛔ Enforcement Rules (NON-NEGOTIABLE)

### P0: Pre-flight Checkpoint (MANDATORY)

Before executing ANY step, you MUST output this block in the conversation:

```
┌─────────────────────────────────────────────────────┐
│ 🛫 PRE-FLIGHT: Step <N> — <Name>                    │
├─────────────────────────────────────────────────────┤
│ Persona:    <file path> → reading...                │
│ Knowledge:  <file path(s)> → reading...             │
│ Template:   <file path or "none">                   │
│ Input:      <file path(s)>                          │
│ Output:     <file path>                             │
├─────────────────────────────────────────────────────┤
│ ✅ Persona loaded: <line count> lines               │
│ ✅ Knowledge loaded: <line count> lines             │
│ ✅ Template loaded: <line count> lines / N/A        │
├─────────────────────────────────────────────────────┤
│ Dispatching sub-agent with injected context...      │
└─────────────────────────────────────────────────────┘
```

**Rules:**
- If you cannot produce this block → you have NOT read the files → STOP and read them
- The line counts prove you actually read the files (not faking it)
- After this block, the NEXT action must be dispatching a sub-agent (not doing the work yourself)
- If you catch yourself writing research/analysis/roadmap content instead of dispatching → STOP, you are violating P0

### P1: Orchestrator Does NOT Create Content

You MUST NOT write research findings, roadmap sections, or review verdicts yourself. Every piece of creative/analytical content comes from a dispatched sub-agent.

**Self-check:** If you are writing more than 3 sentences of domain content (not orchestration bookkeeping), you are doing the sub-agent's job. Stop. Dispatch instead.

### P2: Sub-agent Dispatch Format

When dispatching a sub-agent, the prompt MUST contain these sections in order:

```
## Your Identity
[full verbatim content of persona .toml file]

## Domain Knowledge
[full verbatim content of knowledge/framework file(s)]

## Template to Follow (if applicable)
[full verbatim content of template file]

## Task
[step-specific instructions from this SKILL.md]

## Input Files
[paths to read — sub-agent reads these itself]

## Output
Write your output to: [exact output file path]
```

### P3: No Step Merging or Skipping

- Each step = separate sub-agent dispatch = separate output file
- Steps 1-5 execute in order; you cannot jump ahead
- If a step fails → fix and retry, do NOT skip

### P4: Output Validation Before Advancing

After each sub-agent completes, verify:
1. Output file EXISTS at declared path
2. Output is substantive (not a stub or placeholder)
3. If review gate → verdict is explicit (PASS / REQUEST_CHANGES)

Only then advance to next step.

---

## Purpose

Turn a fuzzy idea into an actionable product roadmap. This is **Stage 1** of the woos-idea-to-delivery flow. Run once per project.

**Scope boundary:** This phase produces WHAT to build (product intent, personas, features, metrics). It does NOT produce HOW to build it (architecture, tech stack, data models). Technical decisions belong in the engineering phase.

All file paths (`.hep/`, `docs/`, `ideas/`) are relative to a **project root directory** which MUST be a git repository.

## When to Use

- User says "I want to build X" or shares a raw idea
- Starting a new project or major initiative
- Need to validate market/technical feasibility

## When to Skip

Skip when ALL true:
- `docs/product/<project>-roadmap.md` exists with versioned scope + metrics

If skipping → go directly to `woos-product-design-flow` (Stage 2).

---

## Steps

### Step 1: Idea Capture

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/analyst.toml` |
| **Knowledge** | `references/bmad/templates/brief-template.md` |
| **Input** | _(user conversation)_ |
| **Output** | `ideas/<slug>/00-idea-capture.md` |
| **Side effect** | Creates `.hep/runs/<run_id>/run-manifest.yaml` (state tracking begins here) |

**Skill:** `woos-idea-capture`

Socratic interview the user (or parse a written idea) to extract:
- What problem is being solved
- For whom
- What "done" looks like at a high level
- Constraints and non-goals

After capture, the orchestrator initializes the run manifest.

---

### Step 2: Problem Validation

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/analyst.toml` |
| **Knowledge** | `references/bmad/frameworks/customer-pain-points.md` |
| **Input** | `ideas/<slug>/00-idea-capture.md` |
| **Output** | `ideas/<slug>/00-idea-capture.md` → appends `## Problem Validation` |

Before investing in research, validate the problem is worth solving.

**Must answer:**
- Is this a real problem? (Evidence: user complaints, data, observed behavior)
- How frequently does it occur?
- How painful is it? (Workaround exists and is acceptable? Or blocking?)
- How many people have this problem?
- Are they already paying (time/money) to solve it today?

**Decision framework:**

| Signal | Score |
|--------|-------|
| Users actively complaining / requesting | Strong |
| Workaround exists but is painful | Strong |
| Data shows drop-off / failure at this point | Strong |
| "It would be cool" with no evidence | Weak — probe deeper |
| Only requester has this problem | Weak — validate breadth |

**Verdict:** `PROCEED` / `PIVOT` / `PARK`

- **PROCEED** → continue to Step 3
- **PIVOT** → reframe problem, return to Step 1 with new angle
- **PARK** → not worth solving now, record in ideas index

---

### Step 3: Research & Validation

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/analyst.toml` |
| **Knowledge** | `references/bmad/frameworks/market-research.md` + `references/bmad/frameworks/competitive-analysis.md` |
| **Input** | `ideas/<slug>/00-idea-capture.md` (full, including Problem Validation) |
| **Output** | `docs/research/<topic>.md` |

Investigate:
- Market landscape and competitors
- Existing solutions or reusable approaches
- Feasibility concerns (not tech stack selection — just "is this doable?")
- Risks and unknowns

**Gate:** Research must cite sources and include a recommendation. If critical unknowns remain, flag as blockers.

---

### Step 4: Product Vision & Roadmap

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/create-prd.md` |
| **Input** | `ideas/<slug>/00-idea-capture.md` + `docs/research/<topic>.md` |
| **Output** | `docs/product/<project>-roadmap.md` |

Synthesize into a roadmap document containing:
- Vision (who, what problem, value proposition)
- User Personas
- Core Experience
- Versioned Roadmap (V1/V2/V3 with scope, features, non-goals, metrics)
- Constraints
- Decision Log

---

### Step 4R: Roadmap Review Gate

| | |
|---|---|
| **Sub-agent** | ✅ (independent reviewer) |
| **Persona** | `references/bmad/personas/prd-validator.toml` |
| **Knowledge** | `references/bmad/frameworks/validate-prd.md` + `references/bmad/templates/prd-validation-checklist.md` |
| **Input** | `docs/product/<project>-roadmap.md` + `ideas/<slug>/00-idea-capture.md` |
| **Output** | `docs/reviews/<project>-roadmap-review-rN.md` |

**Checklist:**

| # | Criterion | Fix Hint |
|---|-----------|----------|
| R1 | Vision differentiated | Add a "Unlike X, we…" statement that names the unique angle |
| R2 | Versioning logical | Move items with no V1 dependency into V2+; ensure V1 is shippable alone |
| R3 | Metrics measurable | Replace vague words ("fast", "many") with specific numbers or observable events |
| R4 | Non-goals effective | Rewrite as concrete "we will NOT do X even if Y" statements |
| R5 | Decision Log sound | Add real alternative that was considered; explain why it lost |
| R6 | Personas grounded | Cite observed behavior or data; remove hypothetical "ideal user" language |

**Review findings format:**
```markdown
# Roadmap Review — Round N

| # | Criterion | Status | Finding | Fix Hint | Fixed? |
|---|-----------|--------|---------|----------|--------|
| R1 | Vision differentiated | ✅ | — | — | — |
| R2 | Versioning logical | ❌ | "V1 includes auth + payments" | Move to V2+ | ☐ |

## Summary
PASS: X/6 | FAIL: Y/6 → [PASS | REQUEST_CHANGES]
```

**Fix flow:**
1. If `REQUEST_CHANGES` → dispatch fix agent (pm persona) with findings + roadmap
2. Fix agent edits roadmap in-place, marks `Fixed? ☑` in findings
3. Re-dispatch reviewer (round N+1), checks only `Fixed? ☑` rows
4. Max 2 rounds → ask user if no convergence

**Result:** `PASS` → proceed to Step 5

---

### Step 5: Decision Log

| | |
|---|---|
| **Sub-agent** | ❌ (orchestrator does this directly) |
| **Input** | `docs/product/<project>-roadmap.md` |
| **Output** | `docs/product/<project>-roadmap.md` → appends to `## Decision Log` |

Record key decisions made during discovery:
- Scope inclusions/exclusions and why
- Market positioning decisions
- Product direction trade-offs

Each entry: **Decision** + **Rationale** + **Alternatives Considered**

This log is **append-only** across stages.

---

## State Persistence

### Run Manifest Schema

```yaml
run_id: "<uuid>"
project: "<project-slug>"
created_at: "<ISO8601>"
updated_at: "<ISO8601>"

stages:
  product-discovery:
    status: in_progress  # pending | in_progress | done | blocked
    current_step: 5
    steps:
      1-idea-capture: { status: done, output: "ideas/<slug>/00-idea-capture.md" }
      2-problem-validation: { status: done, output: "ideas/<slug>/00-idea-capture.md#problem-validation" }
      3-research: { status: done, output: "docs/research/<topic>.md" }
      4-roadmap: { status: done, output: "docs/product/<project>-roadmap.md" }
      4r-roadmap-review: { status: done, round: 2, result: PASS }
      5-decision-log: { status: pending }
```

### Recovery Protocol

On start (or restart after crash):
1. Read `.hep/runs/<run_id>/run-manifest.yaml`
2. Find first step where `status != done`
3. Check if output file exists:
   - **EXISTS + well-formed** → mark done, advance
   - **EXISTS + incomplete** → resume (re-dispatch sub-agent with existing content)
   - **NOT EXISTS** → start step from scratch
4. Continue from that point

### Update Rules
- Write manifest BEFORE dispatching sub-agent (`status: in_progress`)
- Write manifest AFTER sub-agent returns (`status: done` + output path)
- Review steps record: `round: N`, `result: PASS|REQUEST_CHANGES`

---

## 🚦 Human Approval Gate (Mandatory)

After all steps done, this is a **hard gate** — you MUST NOT proceed to Stage 2 (PRD) without explicit human approval.

**Present to user:**
1. Output the **full content** of `docs/product/<project>-roadmap.md`
2. State the inferred mode as a fact (not a question):
   - Roadmap contains multiple features for this version → "Will use Strict mode (multi-feature version)"
   - Roadmap contains a single feature → "Will use Standard mode (single feature)"
3. Ask: "Please review the roadmap above. If satisfied, say 'start PRD' to proceed. If you have changes, let me know."

**Rules:**
- Show the COMPLETE file content, not a summary
- Mode is stated, not asked — it's determined by roadmap content
- If user disagrees with mode inference, respect their override
- Do NOT proceed until user explicitly says "start PRD" or equivalent
- If user has questions or wants changes → make changes → re-present full file → wait again
- This gate CANNOT be skipped by `checkpoints: []` — it is always mandatory

Wait for user approval → record mode in run-manifest → mark `stages.product-discovery.status: completed`

## Handoff

On completion (after human approval):
- Roadmap: `docs/product/<project>-roadmap.md`
- Mode: recorded in `run-manifest.yaml` (inferred from roadmap)
- Technical preferences (if any): recorded in idea-capture as deferred — engineering phase will confirm
- Next: invoke `woos-product-design-flow` (Stage 2)

## Failure Handling

| Situation | Action |
|-----------|--------|
| User can't articulate the idea | Ask simpler questions; offer examples |
| Research reveals infeasibility | Report honestly; suggest alternatives |
| Run orchestrator unavailable | Proceed without run_id; note in roadmap |
| User rejects roadmap at checkpoint | Return to relevant step |
| Review loops 3x without convergence | Ask user for direction |
