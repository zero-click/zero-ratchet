---
name: woos-prd-review-gate
description: Independent PRD review gate for Hermes workflow. Executes product-planner + architect reviews and returns PASS or REQUEST_CHANGES.
version: 1.6.0
author: Hermes Profile
license: MIT
---

# Woos PRD Review Gate

## Purpose

Run a strict PRD review gate after PRD drafting and before design.

## Required reviewers

1. `product-planner`
2. `architect`

Both must review the same PRD artifact independently.

## Required Invocation (hard gate)

- MUST invoke `product-planner` and `architect`.
- MUST invoke `woos-review-context` before and after reviewer execution.
- MUST invoke `woos-agent-decision` if `product_planner_status` and `architect_status` conflict.
- If either one is not invoked, return `NOT_RUN` and stop.
- If either one is unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or generic reviewer.

## Reviewer Isolation (hard gate)

- Each reviewer MUST be dispatched as a separate agent instance with fresh context (e.g., via task/spawn tool). In-context skill injection where the same LLM session plays the reviewer role is NOT a valid invocation.
- The dispatched agent receives only the review inputs (PRD artifact, feature context, constraints, prior review context). It MUST NOT inherit the implementer's session history or reasoning.
- `invocation_evidence` MUST include `dispatch_mode: "fresh_context"`. Any other value is invalid and MUST return `BLOCKED`.

## Contract

- Inputs: PRD path, feature context, constraints, prior review context
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output content: concrete findings and required edits
- Output fields (required):
  - `reviewers_used: [product-planner, architect]`
  - `product_planner_status`
  - `architect_status`
  - `review_round`
  - `review_dimensions_covered`
  - `completeness_check`
  - `resolved_prior_findings`
  - `carry_forward_findings`
  - `review_context_file`
  - `decision_resolution` (required when reviewer statuses conflict)
  - `unconfirmed_constraints_frozen: true|false`
  - `blocking_findings`

If either reviewer requests changes, gate result is `REQUEST_CHANGES`.

## Mandatory Review Protocol

1. Load prior findings through `woos-review-context`.
2. Require each reviewer to cover all mandated dimensions in their own skill contract.
3. Require one-pass complete findings; partial-first feedback is invalid.
4. Update `woos-review-context` with resolved/carry-forward findings.
5. Persist review result to the same `<workspace_root>/hep/review-context/<run_id>.yaml`.
6. If reviewer statuses conflict, resolve through `woos-agent-decision` before final gate status.
7. Reject unconfirmed architectural freezes that lack user or ADR approval.

## Escalation Policy

- `review_round_max`: 2
- `reconciliation_attempt_max`: 1 (within each round)
- `max_review_runtime_seconds`: provided by `woos-run-orchestrator`
- If any limit is exceeded, return `BLOCKED` and invoke `woos-human-handoff`.

## Machine-Readable Enforcement Output (required)

```json
{
  "enforcement": {
    "required_invocations": ["product-planner", "architect", "woos-review-context"],
    "actually_invoked": ["product-planner", "architect", "woos-review-context"],
    "missing_invocations": [],
    "invocation_evidence": [
      {
        "skill": "product-planner",
        "dispatch_mode": "fresh_context",
        "invoked_at": "2026-05-12T22:00:00Z",
        "artifact_ref": "docs/prd/<feature>.md",
        "output_digest": "sha256:..."
      }
    ],
    "conflict_detected": false,
    "conflict_resolution_required": false,
    "conflict_resolution_invoked": false,
    "unconfirmed_constraints_frozen": false,
    "completeness_passed": true
  }
}
```

If `conflict_detected` is `true`, `conflict_resolution_required` and `conflict_resolution_invoked` MUST be `true`.
Missing `invocation_evidence` MUST return `BLOCKED`.
