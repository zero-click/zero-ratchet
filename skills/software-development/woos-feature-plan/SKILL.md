---
name: woos-feature-plan
description: Produce a single per-feature engineering plan combining technical design (architecture, test strategy, rollout, baseline/deviation) and the story execution table (ID | AC | Depends | Diff Scope). Replaces the prior split between woos-feature-design and woos-story-decomposition.
version: 3.0.0
author: Hermes Profile
license: MIT
---

# Woos Feature Plan

## Purpose

Produce the **engineering plan** for one feature: the technical decisions ADR-worthy enough to lock before code is written, plus the story execution table the Gate 2 loop will consume.

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
  - `ac_coverage_complete: true|false`
  - `dag_validated: true|false`
  - `diff_scopes_concrete: true|false`
  - `no_unordered_overlaps: true|false`

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

## Story Table
> AC IDs reference `docs/prd/<version>/<feature-id>.md`.
> Rollback for any story: `git restore -- <diff_scope>` (or `git revert <range>` once committed).

| ID  | AC             | Depends | Diff Scope                                       |
|-----|----------------|---------|--------------------------------------------------|
| s01 | FR-1.a         | -       | store/persist.go, store/persist_test.go          |
| s02 | FR-1.b         | s01     | store/persist.go, store/persist_test.go          |
| s03 | FR-3.a         | s01     | store/lifecycle.go, store/lifecycle_test.go      |
| s04 | FR-4.b, FR-4.c | s01     | store/recover.go, store/recover_test.go          |
```

### Sections explicitly NOT in this document

- **Interface / API contracts** — owned by `docs/prd/<version>/<feature-id>-interface.md`
- **Data model details beyond what affects rollout/migration** — same
- **Per-story narrative documents** — there are none; PRD AC is the spec, tests in the diff scope are the verification, `git restore -- <diff_scope>` is the rollback

## Story Table — Column Rules

- **ID**: `s<NN>` zero-padded from `s01`, stable across the run
- **AC**: one PRD AC ID per row; hard cap of 3 strongly-coupled AC sharing test setup, comma-separated
- **Depends**: `-` or comma-separated story IDs that must reach `completed` before this one starts
- **Diff Scope**: comma-separated concrete paths (files or directories) the story is allowed to add/modify. This is the rollback boundary AND the Gate 3 scope-drift whitelist. Vague entries (`src/`, `**`, "wherever needed") are INVALID.

## Story Sizing Rules (AI-checkpoint semantics)

A correctly sized story is one that:

1. Covers **1 PRD acceptance criterion** (hard cap: 3 strongly-coupled AC sharing test setup).
2. Can be **implemented, tested, and reviewed within a single review-round** (`review_round_max = 2`).
3. Has a **bounded, declarable diff scope** so failure isolation and revert know what to touch.
4. Has no overlap on the same files as another story it does not depend on.

Sizing is NOT based on estimated hours, owner, sprint, or "number of tasks". There is no fixed "N stories per feature" rule — decompose as finely as the Gate 2 loop requires to converge.

## Hard Gate Rules

Return `REQUEST_CHANGES` when any of these fail:

- Every PRD AC appears in the Story Table's `AC` column at least once (no orphan AC)
- The dependency graph is a DAG (no cycles)
- Every `Depends` entry resolves to a story ID in the same table
- Every `Diff Scope` is a comma-separated list of concrete paths (no globs that match unbounded sets, no prose)
- No two stories without a `Depends` relationship declare the same file in `Diff Scope`
- No story declares more than 3 AC in the `AC` column
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
  stories_count: 4
  execution_order: [s01, s02, s03, s04]
  ac_coverage_map:
    FR-1.a: [s01]
    FR-1.b: [s02]
    FR-3.a: [s03]
    FR-4.b: [s04]
    FR-4.c: [s04]
  planner_review_path: docs/reviews/<version>/<feature-id>-plan-review.md
```

Per-story runtime state (`status`, `attempts`, `failure_log`) lives in `run-manifest.yaml` under `gate_results.gate-2-execution.<story-id>`, not in `plan.md`. `plan.md` is immutable once Gate 1 passes; runtime updates do NOT edit it.

## Lite Mode Adjustments

Lite skips this gate entirely. There is no engineering plan document and no story table in Lite runs. Verification runs directly against the PRD's AC list via `verification-loop`.

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
        "artifact_ref": "docs/engineering/<version>/<feature-id>-plan.md#story-table",
        "output_digest": "sha256:..."
      }
    ],
    "baseline_compliance_status": "PASS",
    "deviation_detected": false,
    "deviation_adr_path": "",
    "approval_ref": "",
    "unconfirmed_constraints_frozen": false,
    "stories_count": 4,
    "ac_coverage_complete": true,
    "dag_validated": true,
    "diff_scopes_concrete": true,
    "no_unordered_overlaps": true
  }
}
```

`PASS` is INVALID if any of `ac_coverage_complete`, `dag_validated`, `diff_scopes_concrete`, or `no_unordered_overlaps` is `false`. Missing `invocation_evidence` MUST return `BLOCKED`.

## Escalation

- Reviewer returns `REQUEST_CHANGES` → orchestrator revises the plan; max 2 revision rounds before `woos-human-handoff`.
- Repeated oversized stories or unresolvable overlap → escalate; the underlying PRD AC is likely itself too coarse and may need a DCR back to product.

## Migration Note (v2 → v3)

v2 split engineering planning into `woos-feature-design` (→ `docs/engineering/<version>/<feature-id>-design.md`) and `woos-story-decomposition` (→ `docs/stories/<version>/<feature-id>/plan.md`), reviewed by `woos-design-review-gate` and an internal planner dispatch respectively.

v3 collapses both into a single `docs/engineering/<version>/<feature-id>-plan.md` reviewed once by `woos-plan-review-gate`. The `docs/stories/` directory is removed; the story table is a section inside the plan document. Interface/API contracts and data-model details move out of the engineering doc — they are owned by `docs/prd/<version>/<feature-id>-interface.md` (produced by `woos-product-design-flow` Step 6.5).
