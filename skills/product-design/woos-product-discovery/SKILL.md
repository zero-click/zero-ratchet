---
name: woos-product-discovery
description: "Stage 2 orchestrator: transform an existing idea-capture artifact into a validated roadmap + architecture by routing dedicated discovery skills."
version: 3.2.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, discovery, roadmap, planning, research, orchestrator]
    stage: 2
    flow: woos-idea-to-design
    related_skills:
      - woos-problem-validation
      - woos-product-research
      - woos-roadmap-authoring
      - woos-roadmap-review-gate
      - woos-architecture-overview
      - woos-architecture-review-gate
---

# Product Discovery (Orchestrator)

> **🚨 STOP. Read this section FIRST. It overrides any instinct to "just do the work yourself."**
>
> You are an ORCHESTRATOR. You do NOT produce research, roadmaps, or architecture yourself.
> You dispatch dedicated discovery skills and validate their outputs. That is your ONLY job.

## ⛔ Enforcement Rules (NON-NEGOTIABLE)

### P0: Explicit Step Dispatch (MANDATORY)

Before executing any step, state the step being run and the exact:

- skill name
- input file(s)
- output file

**Rules:**
- The next action must be dispatching the declared skill or running the bounded direct step
- If you catch yourself writing research, roadmap, or architecture content instead of dispatching, stop

### P1: Orchestrator Does NOT Create Content

You MUST NOT write research findings, roadmap sections, architecture designs, or review verdicts yourself. Every piece of creative/analytical content comes from a dispatched sub-agent.

The orchestrator MAY directly execute only one bounded bookkeeping step:
- Step 5 (Decision Log append)

**Self-check:** If you are writing more than 3 sentences of domain content (not orchestration bookkeeping), you are doing the sub-agent's job. Stop. Dispatch instead.

### P2: No Step Merging or Skipping

- Each step = separate sub-agent dispatch = separate output file
- Steps execute in order; you cannot jump ahead
- If a step fails → fix and retry, do NOT skip

### P3: Output Validation Before Advancing

After each sub-agent completes, verify:
1. Output file EXISTS at declared path
2. Output is substantive (not a stub or placeholder)
3. If review gate → verdict is explicit (PASS / REQUEST_CHANGES)

Only then advance to next step.

**Required outputs by step:**

| Step | Required result |
|------|-----------------|
| Step 1 | `## Problem Validation` appended to `00-idea-capture.md` with `PROCEED`, `PIVOT`, or `PARK` |
| Step 2 | `docs/research/<topic>.md` exists and includes cited recommendation |
| Step 3 | `docs/product/<project>-roadmap.md` exists with roadmap sections present |
| Step 3R | `docs/reviews/<project>-roadmap-review-rN.md` exists with explicit `PASS` or `REQUEST_CHANGES` |
| Step 4 | `docs/product/<project>-architecture.md` exists with architecture sections present |
| Step 4R | `docs/reviews/<project>-architecture-review-rN.md` exists with explicit `PASS` or `REQUEST_CHANGES` |
| Step 5 | `## Decision Log` in roadmap is updated from accepted prior outputs |

---

## Purpose

Turn an existing idea-capture artifact into an actionable product roadmap + system architecture. This is **Stage 2** of the woos-idea-to-design flow. Run once per project.

All file paths (`docs/`, `ideas/`) are relative to a **project root directory** which MUST be a git repository.

## When to Use

- `ideas/<slug>/00-idea-capture.md` already exists
- Starting product discovery after idea capture
- Need to validate market/technical feasibility

## Prerequisite

- `woos-idea-capture` has already produced `ideas/<slug>/00-idea-capture.md`

## When to Skip

Skip when ALL true:
- `docs/product/<project>-roadmap.md` exists with versioned scope + metrics
- `docs/product/<project>-architecture.md` exists

If skipping:

- do **not** rerun Steps 1–5
- go directly to the **Human Approval Gate** below
- proceed to `woos-product-design-flow` only after explicit human sign-off

---

## Steps

### Step 1: Problem Validation

| | |
|---|---|
| **Skill** | `woos-problem-validation` |
| **Input** | `ideas/<slug>/00-idea-capture.md` |
| **Output** | `ideas/<slug>/00-idea-capture.md` → appends `## Problem Validation` |

**Advance when:** verdict is `PROCEED`.

**Transitions:**
- `PROCEED` → continue to Step 2
- `PIVOT` → revise via `woos-idea-capture`, then restart Discovery
- `PARK` → stop Discovery and record the outcome

---

### Step 2: Research

| | |
|---|---|
| **Skill** | `woos-product-research` |
| **Input** | `ideas/<slug>/00-idea-capture.md` |
| **Output** | `docs/research/<topic>.md` |

**Advance when:** research file exists, is substantive, and includes a recommendation.

---

### Step 3: Roadmap

| | |
|---|---|
| **Skill** | `woos-roadmap-authoring` |
| **Input** | `ideas/<slug>/00-idea-capture.md` + `docs/research/<topic>.md` |
| **Output** | `docs/product/<project>-roadmap.md` |

**Advance when:** roadmap file exists and is substantive.

---

### Step 3R: Roadmap Review Gate

| | |
|---|---|
| **Skill** | `woos-roadmap-review-gate` |
| **Input** | `docs/product/<project>-roadmap.md` + `ideas/<slug>/00-idea-capture.md` |
| **Output** | `docs/reviews/<project>-roadmap-review-rN.md` |

**Review loop:** `REQUEST_CHANGES` → fix roadmap → re-run gate. Max 2 rounds before asking the user for direction.

---

### Step 4: System Architecture Overview

| | |
|---|---|
| **Skill** | `woos-architecture-overview` |
| **Input** | `docs/product/<project>-roadmap.md` + `ideas/<slug>/00-idea-capture.md` |
| **Output** | `docs/product/<project>-architecture.md` |

**Advance when:** architecture file exists and is substantive.

---

### Step 4R: Architecture Review Gate

| | |
|---|---|
| **Skill** | `woos-architecture-review-gate` |
| **Input** | `docs/product/<project>-architecture.md` + `docs/product/<project>-roadmap.md` |
| **Output** | `docs/reviews/<project>-architecture-review-rN.md` |

**Review loop:** `REQUEST_CHANGES` → fix architecture → re-run gate. Max 2 rounds before asking the user for direction.

---

### Step 5: Decision Log

| | |
|---|---|
| **Skill** | direct orchestrator step |
| **Input** | `docs/product/<project>-roadmap.md` + `docs/research/<topic>.md` + `docs/product/<project>-architecture.md` + passed review outputs |
| **Output** | `docs/product/<project>-roadmap.md` → appends to `## Decision Log` |

Append only decisions that were already accepted in Steps 1–4R:
- scope inclusions/exclusions
- research-backed positioning choices
- architecture direction

Each entry must include **Decision**, **Rationale**, and **Alternatives Considered**.

Do NOT invent new analysis here. This is bookkeeping based on prior accepted outputs.

---

## 🚦 Human Approval Gate (Mandatory)

After all steps done, this is a **hard gate** — you MUST NOT proceed to Phase 3 (PRD work) without explicit human approval.

This requirement also applies when Discovery is skipped because roadmap and architecture files already exist.

**Present to user:**
1. Output the **full content** of `docs/product/<project>-roadmap.md`
2. Output the **full content** of `docs/product/<project>-architecture.md`
3. State the inferred mode as a fact (not a question):
   - Roadmap contains multiple features for this version → "Will use Strict mode (multi-feature version)"
   - Roadmap contains a single feature → "Will use Standard mode (single feature)"
4. Ask: "Please review the roadmap and architecture above. If satisfied, say 'start PRD' to proceed. If you have changes, let me know."

**Rules:**
- Show the COMPLETE file contents, not summaries
- Mode is stated, not asked — it's determined by roadmap content
- If user disagrees with mode inference, respect their override
- Do NOT proceed until user explicitly says "start PRD" or equivalent
- If user has questions or wants changes → return to the relevant discovery step → re-present full files → wait again
- This gate is always mandatory

Wait for user approval, then continue to Phase 3.

## Handoff

On completion (after human approval):
- Roadmap: `docs/product/<project>-roadmap.md`
- Architecture: `docs/product/<project>-architecture.md`
- Mode: inferred from roadmap content unless the user overrides it
- Next: invoke `woos-product-design-flow` (Phase 3)

## Failure Handling

| Situation | Action |
|-----------|--------|
| User can't articulate the idea | Ask simpler questions; offer examples |
| Research reveals infeasibility | Report honestly; suggest alternatives |
| User rejects roadmap at checkpoint | Return to relevant step |
| Architecture too uncertain | Flag as risk; proceed with assumptions documented |
| Review loop hits max rounds without convergence | Ask user for direction |
