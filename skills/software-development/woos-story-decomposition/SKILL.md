---
name: woos-story-decomposition
description: Produce a lean story plan (table) for the Gate 3 execution loop — execution order plus diff scope per story. PRD AC is the spec; tests are the verification. No per-story prose documents.
version: 2.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [story, decomposition, ai-checkpoint, engineering, gate]
    related_skills:
      - woos-development-workflow
      - woos-feature-design
      - woos-product-planner
---

# Woos Story Decomposition (Lean)

## Purpose

Produce the **execution plan** the Gate 3 loop needs to converge:

- which AC are addressed in what order
- which files each story is allowed to touch (rollback boundary + deviation gate)
- nothing else

PRD acceptance criteria are the specification. Test code is the verification. The story plan is a 4-column table — not a per-story narrative document.

A story exists for one reason only: it is the smallest unit that can be implemented, tested, reviewed, and **reverted** independently when the loop fails.

## When to Run

- Standard mode only. Lite skips this gate (the Lite feature is itself a single implicit story).
- After Gate 1R (Design Review) returns `PASS`, before Gate 3 (Story Execution Loop).

## Required Invocation (hard gate)

- The orchestrator authors `plan.md`. `woos-product-planner` MUST be dispatched in fresh context with `mode: story-review` to validate the plan before Gate 3 starts.
- The dispatched `woos-product-planner` agent MUST run with `dispatch_mode: "fresh_context"`. In-context self-validation is invalid.
- If `woos-product-planner` is not invoked with `mode: story-review`, return `NOT_RUN` and stop.
- If `woos-product-planner` is unavailable, return `BLOCKED` and stop.

## Input Contract

- Approved PRD: `docs/prd/<version>/<feature-id>.md`
- Engineering design: `docs/engineering/<version>/<feature-id>-design.md` (output of Gate 1)
- Architecture: `docs/product/<project>-architecture.md`
- Roadmap: `docs/product/<project>-roadmap.md`
- Optional: `docs/prd/<version>/<feature-id>-interface.md`, `docs/design/<version>/<feature-id>-ui-brief.md`

## Output

Single file per feature: `docs/stories/<version>/<feature-id>/plan.md`.

```markdown
# <feature-id> Story Plan

> AC IDs reference `docs/prd/<version>/<feature-id>.md`.
> Rollback for any story: `git restore -- <diff_scope>` (or `git revert <range>` once committed).

| ID  | AC           | Depends | Diff Scope                                       |
|-----|--------------|---------|--------------------------------------------------|
| s01 | FR-1.a       | -       | store/persist.go, store/persist_test.go          |
| s02 | FR-1.b       | s01     | store/persist.go, store/persist_test.go          |
| s03 | FR-3.a       | s01     | store/lifecycle.go, store/lifecycle_test.go      |
| s04 | FR-4.b, FR-4.c | s01   | store/recover.go, store/recover_test.go          |
```

**Column rules:**

- **ID**: `s<NN>` zero-padded from `s01`, stable across the run.
- **AC**: one PRD AC ID per row (hard cap: 3 strongly-coupled AC sharing the same test setup, comma-separated).
- **Depends**: `-` or comma-separated story IDs that must be `completed` before this one starts.
- **Diff Scope**: comma-separated concrete paths (files or directories) the story is allowed to add/modify. This is the rollback boundary AND the deviation-control whitelist. Vague entries (`src/`, `**`, "wherever needed") are INVALID.

The orchestrator also records, in `run-manifest.yaml` under `gate_results.gate-2-stories`:

```yaml
gate-2-stories:
  status: PASS
  execution_order: [s01, s02, s03, s04]
  ac_coverage_map:
    FR-1.a: [s01]
    FR-1.b: [s02]
    FR-3.a: [s03]
    FR-4.b: [s04]
    FR-4.c: [s04]
  planner_review_path: docs/reviews/<version>/<feature-id>-story-review.md
```

Per-story runtime state (`status`, `attempts`, `failure_log`) lives in `run-manifest.yaml`, not in `plan.md`. `plan.md` is immutable once Gate 2 passes; runtime updates do NOT edit it.

## Sizing Rules (AI-checkpoint semantics)

A correctly sized story is one that:

1. Covers **1 PRD acceptance criterion** (hard cap: 3 strongly-coupled AC sharing test setup).
2. Can be **implemented, tested, and reviewed within a single review-round** (`review_round_max = 2`).
3. Has a **bounded, declarable diff scope** so failure isolation and revert know what to touch.
4. Has no overlap on the same files as another story it does not depend on (avoids interleaved revert).

Sizing is NOT based on estimated hours, owner, sprint, or "number of tasks".

There is no fixed "N stories per feature" rule. Decompose as finely as needed for the Gate 3 loop to converge.

## Verification

There is no `Verification Signal` field. Gate 3's PASS predicate is: **the project's existing test runner reports green for the tests written in this story's TDD loop, AND no other AC's tests regress.** Story `s<NN>` is considered verified when the tests it introduced (which target its linked AC) pass.

The Gate 3 loop knows which tests belong to which story via the story's `Diff Scope` — new/modified test files inside that scope are this story's tests.

## Rollback

There is no `Rollback Boundary` field. Rollback for any failed story is:

```bash
# pre-commit
git restore -- <diff_scope>
# post-commit
git revert <story-commit-range>
```

The `Diff Scope` column IS the boundary.

## Hard Gate Rules

The orchestrator MUST reject the plan when any of these fail (return `REQUEST_CHANGES`):

- Every PRD AC appears in the `AC` column of at least one story (no orphan AC).
- The dependency graph is a DAG (no cycles).
- Every `Depends` entry resolves to a story ID in the same plan.
- Every `Diff Scope` is a comma-separated list of concrete paths (no globs that match unbounded sets, no prose).
- No two stories without a `Depends` relationship declare the same file in `Diff Scope` (overlap on a shared file requires an explicit ordering).
- No story declares more than 3 AC in the `AC` column.

Return `BLOCKED` (not `REQUEST_CHANGES`) if inputs are missing or the planner is unreachable.

## Lite Mode Adjustments

Lite skips this gate entirely. There is no `docs/stories/` directory in Lite runs. Verification runs directly against the PRD's AC list via `verification-loop`.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- `plan_path`: `docs/stories/<version>/<feature-id>/plan.md`
- `stories_count`
- `execution_order` (topological sort of the DAG)
- `ac_coverage_map` (AC ID → story IDs)
- `unmapped_acs` (empty on PASS)
- `overlap_violations` (empty on PASS)
- `planner_review_status`: `PASS` | `REQUEST_CHANGES`
- `planner_review_path`

## Machine-Readable Enforcement Output (required)

```json
{
  "enforcement": {
    "required_invocations": ["woos-product-planner"],
    "actually_invoked": ["woos-product-planner"],
    "missing_invocations": [],
    "invocation_evidence": [
      {
        "skill": "woos-product-planner",
        "mode": "story-review",
        "dispatch_mode": "fresh_context",
        "invoked_at": "2026-06-12T00:00:00Z",
        "artifact_ref": "docs/stories/<version>/<feature-id>/plan.md",
        "output_digest": "sha256:..."
      }
    ],
    "stories_count": 0,
    "ac_coverage_complete": true,
    "dag_validated": true,
    "diff_scopes_concrete": true,
    "no_unordered_overlaps": true
  }
}
```

`PASS` is INVALID if any of `ac_coverage_complete`, `dag_validated`, `diff_scopes_concrete`, or `no_unordered_overlaps` is `false`. Missing `invocation_evidence` MUST return `BLOCKED`.

## Escalation

- `woos-product-planner` returns `REQUEST_CHANGES` → orchestrator revises `plan.md`; max 2 revision rounds before `woos-human-handoff`.
- Repeated oversized stories or unresolvable overlap → escalate; the underlying PRD AC is likely itself too coarse and may need a DCR back to product.

## Migration Note (v1 → v2)

Prior versions of this skill produced one markdown file per story with fields `Purpose`, `Linked Acceptance Criteria`, `Verification Signal`, `Rollback Boundary`, `Expected Diff Scope`, `Status`, `Failure Log`. v2 collapses to a single per-feature `plan.md` table:

- `Linked AC` → `AC` column
- `Expected Diff Scope` + `Rollback Boundary` → `Diff Scope` column (boundary is implicit: `git restore -- <diff_scope>`)
- `Verification Signal` → removed; tests in the diff scope ARE the signal
- `Purpose` → removed; the AC link IS the purpose
- `Status`, `Failure Log` → moved to `run-manifest.yaml` runtime state
