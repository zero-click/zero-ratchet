---
name: woos-plan-review-gate
description: Independent feature plan review gate. Reviews the combined engineering plan (architecture decisions + story table) produced by woos-feature-plan, using woos-architect and woos-product-planner in fresh contexts. Returns PASS or REQUEST_CHANGES.
version: 2.0.0
author: Hermes Profile
license: MIT
---

# Woos Plan Review Gate

## Purpose

Run a strict review of the engineering plan before coding starts. One gate covers both:

1. **Architecture decisions** (baseline conformance, ADR completeness, risk coverage, rollout/rollback adequacy, security surface)
2. **Story decomposition** (AC coverage, DAG validity, sizing, diff-scope concreteness, non-overlap)

Replaces the prior Gate 1R (`woos-design-review-gate`) and the planner-review step that was embedded inside the old Gate 2 `woos-story-decomposition` skill.

## Required reviewers

- `woos-architect` — architecture / baseline / risk dimensions
- `woos-product-planner` (`mode: story-review`) — story-table dimensions

Both MUST run; a one-reviewer pass is invalid.

## Required Invocation (hard gate)

- MUST invoke `woos-architect` with `mode: review` on the architecture / baseline / risk / rollout / security sections of the plan.
- MUST invoke `woos-product-planner` with `mode: story-review` on the Story Table section of the plan.
- MUST invoke `woos-review-context` before and after each reviewer execution.
- If any required reviewer is not invoked, return `NOT_RUN` and stop.
- If a required reviewer is unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or non-whitelisted reviewer.

## Reviewer Isolation (hard gate)

- Each reviewer MUST be dispatched as a separate agent instance with fresh context (e.g. via task/spawn tool). In-context skill injection where the same LLM session plays the reviewer role is NOT a valid invocation.
- Each dispatched agent receives only the review inputs (the plan doc, linked PRD, roadmap, architecture, optional interface summary / UI brief / upstream interfaces, and prior review context). It MUST NOT inherit the implementer's session history or reasoning.
- `invocation_evidence` MUST include `dispatch_mode: "fresh_context"` for each reviewer. Any other value is invalid and MUST return `BLOCKED`.

## Contract

- **Input:** plan doc path (`docs/engineering/<version>/<feature-id>-plan.md`) + linked PRD, roadmap, architecture, and any supporting interface / UI artifacts + prior review context
- **Output status:** `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- **Output content:** concrete mismatches, risks, required revisions — split by reviewer
- **Output fields (required):**
  - `reviewers_used: [woos-architect, woos-product-planner]`
  - `review_round`
  - `architect_dimensions_covered`
  - `planner_dimensions_covered`
  - `completeness_check`
  - `resolved_prior_findings`
  - `carry_forward_findings`
  - `review_context_file`
  - `baseline_compliance_status: PASS | REQUEST_CHANGES`
  - `deviation_detected: true|false`
  - `deviation_adr_path` (required when `deviation_detected=true`)
  - `approval_ref` (required when `deviation_detected=true`)
  - `unconfirmed_constraints_frozen: true|false`
  - `ac_coverage_complete: true|false`
  - `dag_validated: true|false`
  - `diff_scopes_concrete: true|false`
  - `no_unordered_overlaps: true|false`
  - `blocking_findings`

## Mandatory Review Protocol

1. Load prior findings through `woos-review-context`.
2. Dispatch `woos-architect` (`mode: review`) with the full plan + supporting artifacts; require all architect dimensions to be checked.
3. Dispatch `woos-product-planner` (`mode: story-review`) with the plan's Story Table and supporting artifacts; require all five story-review dimensions to be checked (AC coverage, DAG, sizing, diff-scope concreteness, non-overlap).
4. Require one-pass complete findings from each reviewer; partial-first feedback is invalid.
5. Reconcile reviewer outputs via `woos-agent-decision` when verdicts conflict (e.g. architect says PASS, planner says REQUEST_CHANGES — overall verdict is REQUEST_CHANGES).
6. Update `woos-review-context` with resolved / carry-forward findings.
7. Persist review result to `<workspace_root>/hep/review-context/<run_id>.yaml`.
8. Reject baseline deviations without ADR + approval.
9. Reject unconfirmed architectural freezes.
10. Reject story tables with orphan AC, DAG cycles, vague diff scopes, or unordered overlap.

## Escalation Policy

- `review_round_max`: 2
- `reconciliation_attempt_max`: 1 (within each round)
- `max_review_runtime_seconds`: provided by `woos-run-orchestrator`
- If any limit is exceeded, return `BLOCKED` and invoke `woos-human-handoff`.

## Machine-Readable Enforcement Output (required)

```json
{
  "enforcement": {
    "required_invocations": ["woos-architect", "woos-product-planner", "woos-review-context"],
    "actually_invoked": ["woos-architect", "woos-product-planner", "woos-review-context"],
    "missing_invocations": [],
    "invocation_evidence": [
      {
        "skill": "woos-architect",
        "mode": "review",
        "dispatch_mode": "fresh_context",
        "invoked_at": "2026-06-13T22:00:00Z",
        "artifact_ref": "docs/engineering/<version>/<feature-id>-plan.md",
        "output_digest": "sha256:..."
      },
      {
        "skill": "woos-product-planner",
        "mode": "story-review",
        "dispatch_mode": "fresh_context",
        "invoked_at": "2026-06-13T22:03:00Z",
        "artifact_ref": "docs/engineering/<version>/<feature-id>-plan.md#story-table",
        "output_digest": "sha256:..."
      }
    ],
    "baseline_compliance_status": "PASS",
    "deviation_detected": false,
    "deviation_adr_path": "",
    "approval_ref": "",
    "unconfirmed_constraints_frozen": false,
    "ac_coverage_complete": true,
    "dag_validated": true,
    "diff_scopes_concrete": true,
    "no_unordered_overlaps": true,
    "completeness_passed": true
  }
}
```

Missing `invocation_evidence` for either reviewer MUST return `BLOCKED`.
