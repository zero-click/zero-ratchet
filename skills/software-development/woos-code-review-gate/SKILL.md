---
name: woos-code-review-gate
description: Independent code/security review gate for Hermes workflow. Uses code-reviewer and security-reviewer where applicable.
version: 1.7.0
author: Hermes Profile
license: MIT
---

# Woos Code Review Gate

## Purpose

Enforce independent review before PR readiness.

## Required reviewers

- Always: `code-reviewer`
- Security-sensitive scope: `security-reviewer` (additional)

## Required Invocation (hard gate)

- MUST invoke `code-reviewer` for every code change.
- MUST invoke `security-reviewer` when scope includes auth, input handling, secrets, payments, external callbacks, or sensitive data flows.
- MUST invoke `woos-review-context` before and after reviewer execution.
- MUST invoke `woos-agent-decision` when reviewer conclusions conflict.
- If required reviewer is not invoked, return `NOT_RUN` and stop.
- If required reviewer is unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or non-whitelisted reviewer.

## Contract

- Input: current diff + linked artifacts (PRD/design/capability) + prior review context
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output content: blocking and non-blocking findings
- Output fields (required):
  - `reviewers_used`
  - `code_reviewer_status`
  - `security_reviewer_status` (when required)
  - `review_round`
  - `review_dimensions_covered`
  - `completeness_check`
  - `resolved_prior_findings`
  - `carry_forward_findings`
  - `review_context_file`
  - `spec_alignment_status: PASS | REQUEST_CHANGES`
  - `spec_deviation_findings`
  - `intentional_deviations`
  - `baseline_compliance_status: PASS | REQUEST_CHANGES`
  - `deviation_detected: true|false`
  - `deviation_adr_path` (required when deviation_detected=true)
  - `approval_ref` (required when deviation_detected=true)
  - `unconfirmed_constraints_frozen: true|false`
  - `blocking_findings`

## Spec Alignment Requirements (hard gate)

- Review MUST explicitly compare implementation against linked PRD/design/capability artifacts.
- Any behavior/interface/data/policy deviation MUST be recorded in `spec_deviation_findings`.
- If deviation is intentional, add rationale and artifact update status in `intentional_deviations`.
- If unresolved deviation exists, set `spec_alignment_status: REQUEST_CHANGES`.

Gate passes only when all required reviewers are clear and `spec_alignment_status` is `PASS`.

## Security Scope Trigger (hard gate)

`security_scope_detected` MUST be derived from explicit evidence, not reviewer intuition only.

- Required trigger checklist:
  - auth/session/authorization logic changed
  - input validation/trust boundary changed
  - secret/token/credential handling changed
  - external callback/webhook/payment flow changed
  - sensitive data access/logging policy changed
- Output field required: `security_scope_evidence`

## Mandatory Review Protocol

1. Load prior findings through `woos-review-context`.
2. Require all required reviewer dimensions to be checked.
3. Require one-pass complete findings; partial-first feedback is invalid.
4. Resolve reviewer disagreement through `woos-agent-decision`.
5. Update `woos-review-context` with resolved/carry-forward findings.
6. Persist review result to the same `<workspace_root>/hep/review-context/<run_id>.yaml`.
7. Reject baseline deviations without ADR+approval.
8. Reject unconfirmed architectural freezes.

## Escalation Policy

- `review_round_max`: 2
- `reconciliation_attempt_max`: 1 (within each round)
- `max_review_runtime_seconds`: provided by `woos-run-orchestrator`
- If any limit is exceeded, return `BLOCKED` and invoke `woos-human-handoff`.

## Machine-Readable Enforcement Output (required)

```json
{
  "enforcement": {
    "required_invocations": ["code-reviewer", "woos-review-context"],
    "conditionally_required_invocations": ["security-reviewer", "woos-agent-decision"],
    "actually_invoked": ["code-reviewer", "woos-review-context"],
    "missing_invocations": [],
    "invocation_evidence": [
      {
        "skill": "code-reviewer",
        "invoked_at": "2026-05-12T22:00:00Z",
        "artifact_ref": "git diff HEAD",
        "output_digest": "sha256:..."
      }
    ],
    "baseline_compliance_status": "PASS",
    "deviation_detected": false,
    "deviation_adr_path": "",
    "approval_ref": "",
    "unconfirmed_constraints_frozen": false,
    "security_scope_detected": false,
    "security_scope_evidence": [],
    "conflict_detected": false,
    "completeness_passed": true
  }
}
```

When `security_scope_detected` is `true`, `security-reviewer` MUST appear in `actually_invoked`.
When `conflict_detected` is `true`, `woos-agent-decision` MUST appear in `actually_invoked`.
Missing `invocation_evidence` MUST return `BLOCKED`.
