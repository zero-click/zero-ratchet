---
name: woos-product-planning-workflow
description: Product-level planning workflow for Hermes. Inspired by BMAD-style planning, it converts a product idea or initiative into feature map, delivery phases, and a recommended next implementation slice before entering engineering-workflow.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, planning, roadmap, epic, story, phase, bmad]
---

# Woos Product Planning Workflow

## Why this skill exists

`engineering-workflow` is optimized for delivering a concrete feature slice.  
When the input is still at **product / initiative / roadmap** level, jumping directly into PRD/design/coding creates two common failures:

1. implementation starts before feature boundaries are stable
2. the next slice is chosen ad hoc, without delivery phase structure

This skill adds a **product-level planning entry lane** before implementation.

It is inspired by BMAD-style planning flow:

- start from a project brief / initiative statement
- shape product intent into feature groups and epics
- define delivery phases
- identify the next story-worthy implementation slice
- only then hand off that slice into the engineering workflow

## When to use

Use this skill when:

- the user is discussing a product, initiative, roadmap, or large capability set
- multiple features are still mixed together
- delivery needs phase planning before implementation
- you need a recommended next slice, not immediate coding
- the user asks for product design / product planning / roadmap decomposition

Do **not** use it for:

- a single already-scoped engineering task
- trivial fixes or direct coding requests
- pure technical refactors with no product planning dimension

## Default entry rule

For product-facing repositories, prefer this order:

```text
Idea / initiative
-> woos-product-planning-workflow
-> choose next slice
-> engineering-workflow
```

Do **not** jump from vague `PRODUCT.md`, founder notes, or roadmap prose directly into implementation if feature boundaries and delivery phases are still unclear.

## Inputs

Gather only what is needed:

1. Product brief / initiative statement
   - problem, target users, desired outcome
2. Existing product context
   - `PRODUCT.md`, roadmap notes, issue threads, strategy docs, demos
3. Delivery constraints
   - team size, dependency sequencing, launch timing, compliance, migration risk
4. Existing system context (lightweight)
   - current architecture, major constraints, known platform limits

If critical product truth is missing, record it as an open question instead of inventing it.

## Core workflow

### Step 1 — Frame the initiative

Compress the ask into a short product brief:

- problem/opportunity
- target user/operator
- outcome after launch
- why now

Output:

- `initiative_summary`
- `success_outcome`
- `planning_scope`

### Step 2 — Build the feature map

Decompose the initiative into feature groups / epics.

Each feature should answer:

- what user-visible capability it adds
- what dependencies it has
- whether it is foundational, enabling, or polish

Rules:

- prefer 3-7 feature groups for an initiative-level plan
- separate product capabilities from technical enablers
- do not prematurely decompose into code tasks

Output:

- `feature_map`
- `dependency_notes`

### Step 3 — Define delivery phases

Cluster the feature map into phases.

Recommended phase model:

1. **Foundation** — platform/enablers/risk retirement
2. **Core capability** — minimum lovable / minimum viable user path
3. **Expansion** — important follow-on capabilities
4. **Polish / scale / ops** — optimization, analytics, operational hardening

Rules:

- phase boundaries must be outcome-based, not arbitrary dates
- each phase must have explicit entry/exit criteria
- cross-phase dependencies must be named

Output:

- `delivery_phases`
- `phase_goals`
- `entry_exit_criteria`

### Step 4 — Pick the next implementation slice

From the phases, identify the **single best next slice** to feed into engineering.

A valid next slice must be:

- small enough for one engineering workflow run
- valuable enough to validate direction
- not blocked by unresolved prerequisite decisions
- expressible as one feature PRD/design lane

Rules:

- prefer the smallest slice that unlocks learning or downstream work
- if architecture risk is dominant, pick a risk-retiring slice first
- if product uncertainty is dominant, pick a user-validation slice first

Output:

- `recommended_next_slice`
- `why_this_slice_now`
- `not_chosen_yet`

### Step 5 — Handoff into engineering workflow

Prepare a clean handoff for `engineering-workflow`.

The handoff must include:

- slice objective
- scope boundaries
- acceptance intent
- dependencies and blockers
- whether Standard or Strict engineering profile is recommended

If the slice is still too vague for engineering, stop and return `REQUEST_CHANGES`.

## Artifact recommendation

Preferred artifact:

`docs/product/<initiative>-plan.md`

If repo conventions differ, follow repo convention. The artifact should be durable and reusable across sessions.

## Required output structure

Return results in this order:

```text
STATUS
- PASS | REQUEST_CHANGES | BLOCKED

INITIATIVE
- concise summary
- target users
- desired outcome

FEATURE MAP
- feature groups / epics
- dependency notes

DELIVERY PHASES
- phase list
- goals
- entry/exit criteria

RECOMMENDED NEXT SLICE
- selected slice
- rationale
- explicit non-selected items

HANDOFF TO ENGINEERING
- ready_for_woos_development_workflow: true/false
- recommended_profile: Lite | Standard | Strict
- requirement seed for next workflow run

OPEN QUESTIONS
- missing truth / blockers / assumptions
```

## Minimal contract

This skill is successful only if:

1. product intent is decomposed into a feature map
2. delivery phases are explicit
3. one recommended next slice is selected
4. the engineering handoff is concrete enough for `engineering-workflow`
5. unresolved product truth is listed explicitly instead of guessed

## Hard gate rules

Return `REQUEST_CHANGES` when:

- features are still mixed together with no stable boundaries
- no delivery phase structure is defined
- more than one “next slice” is proposed without prioritization
- the recommended slice is still too large or ambiguous for engineering

Return `BLOCKED` when:

- essential source material is unavailable and planning cannot proceed
- external decision makers must clarify a blocking product question first

## Suggested follow-on sequence

After this skill passes:

1. create/update the product planning artifact
2. choose the recommended next slice
3. invoke `engineering-workflow` for that slice
4. inside engineering workflow, continue through requirement -> PRD -> design -> implement

## Invocation examples

- "Use `woos-product-planning-workflow` to turn this initiative into feature groups, delivery phases, and the next implementation slice."
- "Plan this product at roadmap level first; do not start coding."
- "Break this initiative into phases, then tell me what the next engineering slice should be."

## Relation to BMAD-style planning

This skill intentionally borrows the useful planning structure from BMAD-style workflows:

- initiative/brief first
- product decomposition before coding
- phase-aware planning
- next-slice handoff into implementation

But it stays aligned with this Hermes profile:

- thin, explicit skill contract
- durable artifacts over chat-only planning
- clear handoff into `engineering-workflow`
- no hidden roleplay dependency on separate personas unless explicitly requested
