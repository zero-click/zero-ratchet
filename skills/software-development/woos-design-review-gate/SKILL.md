---
name: woos-design-review-gate
description: Independent feature design review gate for Hermes workflow. Uses architect review and returns PASS or REQUEST_CHANGES.
version: 1.6.0
author: Hermes Profile
license: MIT
---

# Woos Design Review Gate

## Purpose

Run a strict design review gate before coding starts.

## Required reviewer

- `architect`

## Required Invocation (hard gate)

- MUST invoke `architect`.
- MUST invoke `woos-review-context` before and after reviewer execution.
- If not invoked, return `NOT_RUN` and stop.
- If unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or non-whitelisted reviewer.

## Reviewer Isolation (hard gate)

- The `architect` reviewer MUST be dispatched as a separate agent instance with fresh context (e.g., via task/spawn tool). In-context skill injection where the same LLM session plays the reviewer role is NOT a valid invocation.
- The dispatched agent receives only the review inputs (design doc, linked PRD/capability artifacts, prior review context). It MUST NOT inherit the implementer's session history or reasoning.
- `invocation_evidence` MUST include `dispatch_mode: "fresh_context"`. Any other value is invalid and MUST return `BLOCKED`.

## Contract

- Input: design doc path + linked PRD/capability artifacts + prior review context
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output content: concrete mismatches, risks, and required revisions
- Output fields (required):
  - `reviewer_used: architect`
  - `review_round`
  - `review_dimensions_covered`
  - `completeness_check`
  - `resolved_prior_findings`
  - `carry_forward_findings`
  - `review_context_file`
  - `baseline_compliance_status: PASS | REQUEST_CHANGES`
  - `deviation_detected: true|false`
  - `deviation_adr_path` (required when deviation_detected=true)
  - `approval_ref` (required when deviation_detected=true)
  - `unconfirmed_constraints_frozen: true|false`
  - `blocking_findings`

## Mandatory Review Protocol

1. Load prior findings through `woos-review-context`.
2. Require all required architect dimensions to be checked.
3. Require one-pass complete findings; partial-first feedback is invalid.
4. Update `woos-review-context` with resolved/carry-forward findings.
5. Persist review result to the same `<workspace_root>/hep/review-context/<run_id>.yaml`.
6. Reject baseline deviations without ADR+approval.
7. Reject unconfirmed architectural freezes.

## Escalation Policy

- `review_round_max`: 2
- `reconciliation_attempt_max`: 1 (within each round)
- `max_review_runtime_seconds`: provided by `woos-run-orchestrator`
- If any limit is exceeded, return `BLOCKED` and invoke `woos-human-handoff`.

## Machine-Readable Enforcement Output (required)

```json
{
  "enforcement": {
    "required_invocations": ["architect", "woos-review-context"],
    "actually_invoked": ["architect", "woos-review-context"],
    "missing_invocations": [],
    "invocation_evidence": [
      {
        "skill": "architect",
        "dispatch_mode": "fresh_context",
        "invoked_at": "2026-05-12T22:00:00Z",
        "artifact_ref": "docs/design/<feature>.md",
        "output_digest": "sha256:..."
      }
    ],
    "baseline_compliance_status": "PASS",
    "deviation_detected": false,
    "deviation_adr_path": "",
    "approval_ref": "",
    "unconfirmed_constraints_frozen": false,
    "completeness_passed": true
  }
}
```

Missing `invocation_evidence` MUST return `BLOCKED`.
