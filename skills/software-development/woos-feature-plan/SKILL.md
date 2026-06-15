---
name: woos-feature-plan
description: Produce a single per-feature engineering plan combining technical design (architecture, test strategy, rollout, baseline/deviation) and the Stories/Tasks section (agile `As a / I want / so that` + commit-sized tasks with concrete Diff Scope). Replaces the prior split between woos-feature-design and woos-story-decomposition.
version: 3.0.0
author: Hermes Profile
license: MIT
---

# Woos Feature Plan

## Purpose

Produce the **engineering plan** for one feature: the technical decisions ADR-worthy enough to lock before code is written, plus the Stories/Tasks section the Gate 2 loop will consume.

This is the engineering analog of Superpowers' plan mode: take a PRD (which is product-side WHAT/WHY plus a stable interface contract) and produce one document that tells the implementer how to build it and in what order.

## Why one document

Previously this was split into:

- `woos-feature-design` → a design doc with architecture, interfaces, data model, test strategy, rollout, risks
- `woos-story-decomposition` → a separate `plan.md` table with story IDs and diff scope

In practice the decomposition depends on the architecture decisions, so reviewing them separately produced two review rounds and one consistency gap. The interface and data-model sections also duplicated the PRD's `<feature-id>-interface.md`. v3 collapses both into a single `plan.md` and lets the PRD interface summary remain the source of truth for cross-feature contracts.

## Required Invocation (hard gate)

- MUST invoke `woos-architect` with `mode: author` to produce the architecture / baseline / risk / rollout sections.
- For multi-story or non-trivial scope, MUST also invoke `woos-product-planner` with `mode: planning` to validate the story decomposition before the document is finalized.
- If required invocation is missing, return `NOT_RUN` and stop.
- If a required component is unavailable, return `BLOCKED` and stop.
- Do not substitute with undocumented ad-hoc plan notes.

## Reviewer Isolation (hard gate)

- `woos-architect` (and `woos-product-planner` when invoked) MUST be dispatched as a separate agent instance with fresh context (e.g. via task/spawn tool). In-context skill injection where the same LLM session plays the reviewer role is NOT a valid invocation.
- The dispatched agent receives only the plan inputs (approved PRD, roadmap, architecture, optional interface summary / UI brief / upstream interfaces, prior context). It MUST NOT inherit the implementer's session history or reasoning.
- `invocation_evidence` MUST include `dispatch_mode: "fresh_context"`. Any other value is invalid and MUST return `BLOCKED`.

## Contract

- **Input:** approved PRD + roadmap + architecture (+ optional interface summary, UI brief, upstream interfaces)
- **Output file:** `docs/engineering/<version>/<feature-id>-plan.md`
- **Output status:** `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- **Output fields (required):**
  - `plan_owner: woos-architect`
  - `review_dependencies` (e.g. `woos-product-planner` for multi-story scope)
  - `baseline_compliance_status: PASS | REQUEST_CHANGES`
  - `deviation_detected: true|false`
  - `deviation_adr_path` (required when `deviation_detected=true`)
  - `approval_ref` (required when `deviation_detected=true`)
  - `unconfirmed_constraints_frozen: true|false`
  - `stories_count`
  - `tasks_count`
  - `story_statements_valid: true|false`
  - `ac_coverage_complete: true|false`
  - `dag_validated: true|false`
  - `diff_scopes_concrete: true|false`
  - `no_unordered_overlaps: true|false`
  - `doc_only_cap_ok: true|false`

## Required Document Structure

`docs/engineering/<version>/<feature-id>-plan.md` MUST contain these sections in this order:

```markdown
# <feature-id> Feature Plan

## Overview
One paragraph: what we are building, why now, what is intentionally out of scope.

## Architecture
Chosen approach + key technical decisions. Reference (do not duplicate) the PRD interface
summary at `docs/prd/<version>/<feature-id>-interface.md` for external contracts.

## Test Strategy
- Unit / integration / contract / e2e mix
- What is exercised at each level
- Coverage expectations (machine-checkable where possible)

## Rollout & Rollback
- Feature-flag strategy (if any)
- Migration ordering and backfill
- Rollback path (revert range, data restore, feature flag off)

## Security & Risk
- Threat surface introduced by this feature
- Top risks + mitigation
- Open questions that are NOT yet ADRs

## Baseline & Deviation Decision Record
For each affected domain (UI, backend, database, infra):
- Domain
- Mainstream baseline assumed
- Decision (`use baseline` | `deviate`)
- If deviation: ADR path + approval_ref

## Stories
See the Stories format and rules immediately below.
```

## Stories
> AC IDs reference `docs/prd/<version>/<feature-id>.md`.
> Rollback for any task: `git restore -- <diff_scope>` (or `git revert <range>` once committed).

A **Story** here uses the agile definition: a **vertical slice of user-perceivable value**, expressed as `As a <persona>, I want <capability>, so that <benefit>`. AC are the story's acceptance criteria (how done is judged). **Tasks** are the implementation breakdown of a story — they are the unit of commit, not the unit of value.

```
## Stories

### S1 — <agile story title>
**As a** <persona>, **I want** <capability>, **so that** <benefit>.
- **AC**: FR-1.a, FR-1.b, FR-1.c (refs PRD)
- **Tasks** (commit-sized):
  | Task | Diff Scope | Notes |
  |------|------------|-------|
  | t1: <verb-led summary> | path/a.go, path/a_test.go | TDD; covers FR-1.a |
  | t2: <verb-led summary> | path/b.go, path/b_test.go | covers FR-1.b/c |
- **Depends**: -

### S2 — <agile story title>
**As a** <persona>, **I want** <capability>, **so that** <benefit>.
- **AC**: FR-2.a, FR-3.a
- **Tasks**:
  | Task | Diff Scope | Notes |
  |------|------------|-------|
  | t1: ... | ... | ... |
- **Depends**: S1
```

### Sections explicitly NOT in this document

- **Interface / API contracts** — owned by `docs/prd/<version>/<feature-id>-interface.md`
- **Data model details beyond what affects rollout/migration** — same
- **Per-story narrative documents** — there are none; the agile story statement above + PRD AC is the spec, tests in the task diff scope are the verification, `git restore -- <diff_scope>` is the rollback

## Story / Task — Column Rules

**Story-level fields:**
- **ID**: `S<N>` (capital S), stable across the run
- **Story statement**: required, full `As a / I want / so that` sentence
- **AC**: comma-separated PRD AC IDs that this story's acceptance is judged against. No numeric cap.
- **Depends**: `-` or comma-separated Story IDs that must reach `completed` before this one starts

**Task-level fields (under each story):**
- **ID**: `t<n>` (lowercase t), local to the story (S1.t1, S1.t2, …)
- **Summary**: verb-led one-line description of the commit
- **Diff Scope**: comma-separated concrete paths the task is allowed to add/modify. This is the rollback boundary AND the Gate 3 scope-drift whitelist. Vague entries (`src/`, `**`, prose) are INVALID.
- **Notes** *(optional)*: free-text column in the Tasks table, typically used to call out which AC subset a task covers (e.g. `covers FR-1.a`). Traceability does NOT depend on this column — Gate 4 joins `AC → story → all of that story's tasks' Diff Scope`. The column is reviewer guidance only.

**Task ordering:** dependencies are declared only at the story level (`Depends` between stories). Inside a single story, tasks execute in their declared order (top-to-bottom in the Tasks table). Cross-story task-level dependencies are NOT supported — if a task needs another story's output, split it into a new story with a story-level `Depends`.

## Story Sizing Rules (agile semantics)

A correctly sized **story** satisfies **INVEST**:
- **Independent**: deliverable without waiting on another story (declare via `Depends` if not)
- **Negotiable**: the *how* is open; only the user value and AC are fixed
- **Valuable**: a real persona named in the PRD can perceive the value when this story ships
- **Estimable**: scope is concrete enough to bound effort
- **Small**: completable inside one review-round (`review_round_max = 2`)
- **Testable**: AC give a deterministic pass/fail

A correctly sized **task** is:
- A single coherent commit a reviewer can read in one sitting
- Bounded by a concrete `Diff Scope` (rollback unit)
- Either RED→GREEN (test+code) for code tasks, or one documentation slice for doc tasks
- No file overlap with another task under a **non-dependent** story (tasks inside the same story execute sequentially in declared order, so sharing a file between them is safe)

**Stories are decomposed by user value, not by AC count or file count.** Two AC that serve the same persona-perceived capability belong in the same story. Two AC that deliver independent capabilities belong in different stories. Use AC as acceptance evidence, not as splitting axis.

**Tasks are decomposed by commit atomicity.** Inside a story, slice into the fewest commits a reviewer can confidently review and revert independently. Do not create one task per AC by reflex.

**Doc-only stories:** one operator-facing document = at most one story, sliced into ≤3 doc tasks (or 1 task if a single coherent reading). N tasks per FR section is an antipattern.

**Reviewer self-check before finalizing the plan:** for each story, "would a product person agree this delivers a real persona a real capability?" If no → it is a task, fold it. For each task, "can a reviewer review and revert this commit in isolation?" If no → re-slice.

Sizing is NOT based on estimated hours, owner, sprint, AC count, or "1 commit per FR". There is no fixed "N stories per feature" rule — most features deliver 2–5 stories; large features deliver more, each still INVEST-compliant.

## Hard Gate Rules

Return `REQUEST_CHANGES` when any of these fail:

- Every story has a complete `As a / I want / so that` statement naming a PRD persona
- Every PRD AC appears in some story's `AC` list at least once (no orphan AC)
- Story dependency graph is a DAG (no cycles)
- Every `Depends` entry resolves to a Story ID in the same plan
- Every task has a concrete `Diff Scope` (no globs that match unbounded sets, no prose)
- No two tasks under non-dependent stories declare the same file in `Diff Scope`
- Doc-only features: each independent operator-facing document = at most 1 story, sliced into ≤3 doc tasks; a feature MUST NOT exceed 2 doc-only stories total
- Baseline & Deviation table is complete for every affected domain
- Any `deviate` row has an `adr_path` and `approval_ref`

Return `BLOCKED` (not `REQUEST_CHANGES`) when inputs are missing or a required reviewer is unreachable.

## Baseline and Deviation Rules (hard gate)

1. Default to mainstream, maintainable, evolvable baseline for each affected domain.
2. Any below-baseline or outlier decision requires ADR at `docs/adr/ADR-*.md`.
3. Deviation without explicit `approval_ref` MUST return `REQUEST_CHANGES`.
4. Do not freeze architectural constraints that were not user-provided or ADR-approved.
5. If `unconfirmed_constraints_frozen=true`, return `REQUEST_CHANGES`.

## Run-Manifest Updates

On PASS, the orchestrator records under `gate_results.gate-1-plan`:

```yaml
gate-1-plan:
  status: PASS
  plan_path: docs/engineering/<version>/<feature-id>-plan.md
  stories_count: 2
  tasks_count: 4
  execution_order: [S1.t1, S1.t2, S2.t1, S2.t2]
  ac_coverage_map:
    FR-1.a: [S1]
    FR-1.b: [S1]
    FR-1.c: [S1]
    FR-2.a: [S2]
    FR-3.a: [S2]
  planner_review_path: docs/reviews/<version>/<feature-id>-plan-review.md
```

Per-task runtime state (`status`, `attempts`, `failure_log`) lives in `run-manifest.yaml` under `gate_results.gate-2-execution.<story-id>.tasks.<task-id>`, not in `plan.md`. `plan.md` is immutable once Gate 1 passes; runtime updates do NOT edit it.

## Lite Mode Adjustments

Lite skips this gate entirely. There is no engineering plan document and no stories/tasks section in Lite runs. Verification runs directly against the PRD's AC list via `verification-loop`.

## Machine-Readable Enforcement Output (required)

```json
{
  "enforcement": {
    "required_invocations": ["woos-architect", "woos-product-planner"],
    "actually_invoked": ["woos-architect", "woos-product-planner"],
    "missing_invocations": [],
    "invocation_evidence": [
      {
        "skill": "woos-architect",
        "mode": "author",
        "dispatch_mode": "fresh_context",
        "invoked_at": "2026-06-13T00:00:00Z",
        "artifact_ref": "docs/engineering/<version>/<feature-id>-plan.md",
        "output_digest": "sha256:..."
      },
      {
        "skill": "woos-product-planner",
        "mode": "planning",
        "dispatch_mode": "fresh_context",
        "invoked_at": "2026-06-13T00:05:00Z",
        "artifact_ref": "docs/engineering/<version>/<feature-id>-plan.md#stories",
        "output_digest": "sha256:..."
      }
    ],
    "baseline_compliance_status": "PASS",
    "deviation_detected": false,
    "deviation_adr_path": "",
    "approval_ref": "",
    "unconfirmed_constraints_frozen": false,
    "stories_count": 2,
    "tasks_count": 4,
    "story_statements_valid": true,
    "ac_coverage_complete": true,
    "dag_validated": true,
    "diff_scopes_concrete": true,
    "no_unordered_overlaps": true,
    "doc_only_cap_ok": true
  }
}
```

`PASS` is INVALID if any of `story_statements_valid`, `ac_coverage_complete`, `dag_validated`, `diff_scopes_concrete`, `no_unordered_overlaps`, or `doc_only_cap_ok` is `false`. Missing `invocation_evidence` MUST return `BLOCKED`.

## Escalation

- Reviewer returns `REQUEST_CHANGES` → orchestrator revises the plan; max 2 revision rounds before `woos-human-handoff`.
- Repeated INVEST-failing stories (oversized, no clear user value) or unresolvable task overlap → escalate; the underlying PRD AC is likely itself too coarse and may need a DCR back to product.

## Migration Note (v2 → v3)

v2 split engineering planning into `woos-feature-design` (→ `docs/engineering/<version>/<feature-id>-design.md`) and `woos-story-decomposition` (→ `docs/stories/<version>/<feature-id>/plan.md`), reviewed by `woos-design-review-gate` and an internal planner dispatch respectively.

v3 collapses both into a single `docs/engineering/<version>/<feature-id>-plan.md` reviewed once by `woos-plan-review-gate`. The `docs/stories/` directory is removed; the Stories section (agile `As a / I want / so that` + Tasks tables) lives inside the plan document. Interface/API contracts and data-model details move out of the engineering doc — they are owned by `docs/prd/<version>/<feature-id>-interface.md` (produced by `woos-product-design-flow` Step 6.5).
