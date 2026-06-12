---
name: woos-story-decomposition
description: Decompose a PRD + engineering design into AI-friendly story checkpoints sized for a single review-round, with explicit verification signals and rollback boundaries.
version: 1.0.0
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

# Woos Story Decomposition

## Purpose

Produce the minimum set of stories needed for an AI coding loop to converge.

Stories in this workflow are **not** the unit of work assignment for humans. They are the unit of:

- one bounded implement → verify → review iteration
- one rollback boundary (when the loop fails, only this story is reverted)
- one traceability anchor (PRD AC → story → tests → code)
- one DCR isolation scope (when a design issue is found, only the affected stories halt)

Story sizing, fields, and acceptance rules are derived from those four needs — not from human estimation, sprint cadence, or owner assignment.

## When to Run

- Standard mode only. Lite skips this gate (the entire Lite feature is small enough to be a single implicit story).
- After Gate 1R (Design Review) returns `PASS` and before Gate 3 (Story Execution Loop).

## Required Invocation (hard gate)

- The orchestrator performs the decomposition. `woos-product-planner` MUST be dispatched in fresh context **with `mode: story-review`** to review the resulting story set before Gate 3 starts.
- `woos-product-planner` review covers: AC coverage completeness, dependency-order correctness, sizing (one review-round bound), and overlap/duplication.
- If `woos-product-planner` is not invoked with `mode: story-review`, return `NOT_RUN` and stop.
- If `woos-product-planner` is unavailable, return `BLOCKED` and stop.
- The dispatched `woos-product-planner` agent MUST run with `dispatch_mode: "fresh_context"`. In-context self-validation is invalid.

## Input Contract

- Approved PRD: `docs/prd/<version>/<feature-id>.md`
- Engineering design: `docs/engineering/<version>/<feature-id>-design.md` (output of Gate 1)
- Architecture: `docs/product/<project>-architecture.md`
- Roadmap: `docs/product/<project>-roadmap.md`
- Optional: `docs/prd/<version>/<feature-id>-interface.md`, `docs/design/<version>/<feature-id>-ui-brief.md`

## Output

- One file per story: `docs/stories/<version>/<feature-id>/story-<NNN>.md` (`<NNN>` zero-padded from `001`)
- Dependency-order list recorded in `run-manifest.yaml` under `gate_results.gate-2-stories.execution_order` (sub-key of the existing `gate_results` map; no new top-level section required)
- `woos-product-planner` review report (saved with the gate output)

## Story Sizing Rules (AI-checkpoint semantics, not human estimation)

A correctly sized story is one that:

1. Covers **1 PRD acceptance criterion**, or at most a small cluster of strongly-coupled AC that share state and test setup (hard cap: 3 AC).
2. Can be **implemented, verified, and reviewed within a single review-round** (`review_round_max = 2` budget — a story that needs 2+ rounds to converge was too big).
3. Has a **single rollback boundary** — failure means reverting only this story's diff, not the whole feature.
4. Touches a **bounded, declarable file set** — the story declares which files/modules it expects to change, so failure isolation and re-entry know what to revert.

Sizing **is not** based on:

- Estimated hours/days
- Owner or assignee
- Sprint or iteration capacity
- Number of "tasks" in a checklist

There is no fixed "3-8 stories per feature" rule. Decompose as finely as needed for the loop to converge; the right count is whatever produces stories that satisfy the four rules above.

## Required Story Template

```markdown
# Story <NNN>: <short verb-phrase title>

## Purpose
One sentence: what behavior change this story produces. Phrase as user-visible or system-visible outcome, not as a task list.

## Linked Acceptance Criteria
- AC-<id> from `docs/prd/<version>/<feature-id>.md` (one preferred, up to 3 if strongly coupled)

## Verification Signal (machine-checkable PASS predicate)
Concrete, deterministic check the AI must run to claim PASS. Examples:
- "`pytest tests/auth/test_login.py::test_invalid_password` exits 0"
- "`curl -s localhost:8080/health | jq -r .status` returns `ok`"
- "`npm run lint -- src/users/` exits 0 AND `npm run typecheck` exits 0"

If verification requires more than one command, list them in order. Vague predicates ("login works", "no errors") are INVALID and the story MUST be rejected by the gate.

## Rollback Boundary
- Files / directories this story is allowed to modify (declared up-front; any change outside this set is a deviation)
- Git operation to revert on failure: e.g. `git restore src/auth/ tests/auth/` or `git revert <commit-range>`

## Dependencies
- None, or: depends on `story-<NNN>` (must be PASS before this story starts)

## Expected Diff Scope (soft hint to the implementer)
- Files expected to be added/modified (best-effort estimate; deviation is allowed but flagged)
- Out-of-scope: list anything explicitly NOT in this story to prevent scope creep

## Status
pending | in_progress | completed | blocked

## Failure Log (filled by Gate 3 on failure)
- attempt 1: <verification signal output excerpt>
- attempt 2: <verification signal output excerpt>
- ...
```

The orchestrator MUST reject stories that omit `Verification Signal` or `Rollback Boundary`, or whose verification signal is not machine-checkable.

## Hard Gate Rules

- Every PRD AC MUST map to at least one story. Coverage gaps return `REQUEST_CHANGES`.
- No story may depend on a story that is not in the set.
- The dependency graph MUST be a DAG (cycles return `REQUEST_CHANGES`).
- Stories MUST be totally ordered by the orchestrator into `execution_order` consistent with the DAG.
- `Verification Signal` MUST be a runnable command (or commands), not prose.
- `Rollback Boundary` MUST name concrete paths or a concrete git command, not "revert my changes".

## Lite Mode Adjustments

Lite skips this gate entirely. In Lite, the feature itself is treated as one implicit story; verification is performed by `verification-loop` against the PRD's AC list directly. There is no `docs/stories/` directory in Lite runs.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- `stories_count`
- `execution_order` (list of story IDs in dependency order)
- `ac_coverage_map` (AC ID → story IDs)
- `unmapped_acs` (empty on PASS)
- `oversized_stories` (any story whose linked AC cluster > 3 or whose declared scope spans unbounded files; empty on PASS)
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
        "artifact_ref": "docs/stories/<version>/<feature-id>/",
        "output_digest": "sha256:..."
      }
    ],
    "stories_count": 0,
    "ac_coverage_complete": true,
    "dag_validated": true,
    "all_stories_have_verification_signal": true,
    "all_stories_have_rollback_boundary": true
  }
}
```

`PASS` is INVALID if `ac_coverage_complete`, `dag_validated`, `all_stories_have_verification_signal`, or `all_stories_have_rollback_boundary` is `false`. Missing `invocation_evidence` MUST return `BLOCKED`.

## Escalation

- `woos-product-planner` returns `REQUEST_CHANGES` → orchestrator revises the story set; max 2 revision rounds before `woos-human-handoff`.
- Repeated `oversized_stories` after 2 revisions → escalate; the underlying PRD AC is likely itself too coarse and may need a DCR back to product.
