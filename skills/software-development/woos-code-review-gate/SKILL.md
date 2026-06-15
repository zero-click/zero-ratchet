---
name: woos-code-review-gate
description: Independent code/security review gate for Hermes workflow. Uses woos-code-reviewer and woos-security-reviewer where applicable.
version: 1.7.0
author: Hermes Profile
license: MIT
---

# Woos Code Review Gate

## Purpose

Enforce independent review before PR readiness.

## Required reviewers

- Always: `woos-code-reviewer`
- Security-sensitive scope: `woos-security-reviewer` (additional)

## Required Invocation (hard gate)

- MUST invoke `woos-code-reviewer` for every code change.
- MUST invoke `woos-security-reviewer` when scope includes auth, input handling, secrets, payments, external callbacks, or sensitive data flows.
- MUST invoke `woos-review-context` before and after reviewer execution.
- When reviewer conclusions conflict, the conflict-resolution rule is built-in: any REQUEST_CHANGES wins. Both reviewers' findings are merged into the structured output — no separate arbitration skill.
- If required reviewer is not invoked, return `NOT_RUN` and stop.
- If required reviewer is unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or non-whitelisted reviewer.

## Reviewer Isolation (hard gate)

- Each reviewer (`woos-code-reviewer`, `woos-security-reviewer`) MUST be dispatched as a separate agent instance with fresh context (e.g., via task/spawn tool). In-context skill injection where the same LLM session plays the reviewer role is NOT a valid invocation.
- The dispatched agent receives only the review inputs (current diff, linked artifacts, prior review context). It MUST NOT inherit the implementer's session history or reasoning.
- `invocation_evidence` MUST include `dispatch_mode: "fresh_context"`. Any other value is invalid and MUST return `BLOCKED`.

## Contract

- Input: current diff + linked artifacts (PRD, roadmap, architecture, engineering plan, and supporting interface/UI artifacts; engineering plan required in Standard mode, omitted in Lite mode where Gate 1 is skipped) + prior review context
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
  - `execution_mode: Lite | Standard`
  - `engineering_plan_present: true|false` (true required in Standard; false allowed only when `execution_mode=Lite`)
  - `spec_alignment_status: PASS | REQUEST_CHANGES`
  - `spec_deviation_findings`
  - `intentional_deviations`
  - `ac_coverage_status: PASS | REQUEST_CHANGES | SKIPPED`
  - `ac_coverage_gaps` (PRD AC IDs without a passing test)
  - `scope_drift_status: PASS | REQUEST_CHANGES | SKIPPED`
  - `scope_drift_findings` (files touched outside the union of all tasks' declared `Diff Scope`)
  - `baseline_compliance_status: PASS | REQUEST_CHANGES`
  - `deviation_detected: true|false`
  - `deviation_adr_path` (required when deviation_detected=true)
  - `approval_ref` (required when deviation_detected=true)
  - `unconfirmed_constraints_frozen: true|false`
  - `blocking_findings`

## Spec Alignment Requirements (hard gate)

- Review MUST explicitly compare implementation against the linked artifacts that exist for the active mode:
  - **Standard:** PRD, roadmap, architecture, engineering plan, supporting interface/UI artifacts when available.
  - **Lite:** PRD, roadmap, architecture, supporting interface/UI artifacts when available. There is no engineering plan artifact in Lite (Gate 1 is skipped); absence of `engineering-plan` MUST NOT cause `REQUEST_CHANGES` and MUST NOT be fabricated.
- Any behavior/interface/data/policy deviation MUST be recorded in `spec_deviation_findings`.
- If deviation is intentional, add rationale and artifact update status in `intentional_deviations`.
- If unresolved deviation exists, set `spec_alignment_status: REQUEST_CHANGES`.

## AC Coverage (hard gate, Standard mode only)

This gate absorbs what the prior Gate 3 (Executable Acceptance) used to do.

- For every PRD AC ID referenced in any story's `AC` list, the reviewer MUST locate at least one test in the current diff (or pre-existing passing test inside one of that story's tasks' `Diff Scope`) that exercises that AC.
- Missing-test AC IDs MUST be listed in `ac_coverage_gaps`.
- Any non-empty `ac_coverage_gaps` sets `ac_coverage_status: REQUEST_CHANGES`.
- Skipped in Lite mode — emit `ac_coverage_status: SKIPPED` (omit/empty `ac_coverage_gaps`).

## Scope Drift Detection (hard gate, Standard mode only)

This gate absorbs what the prior Gate 4 (Deviation Control) used to do.

- The reviewer MUST compare the union of all tasks' `Diff Scope` (across every story in the plan) against the actual files touched in the diff.
- Files touched but NOT in any task's `Diff Scope` MUST be listed in `scope_drift_findings`.
- Any non-empty `scope_drift_findings` sets `scope_drift_status: REQUEST_CHANGES` unless an intentional deviation with rationale is recorded in `intentional_deviations` (and the plan was updated accordingly).
- Skipped in Lite mode — emit `scope_drift_status: SKIPPED` (omit/empty `scope_drift_findings`).

Gate passes only when all required reviewers are clear AND every status field is `PASS` or `SKIPPED` (and `SKIPPED` is allowed only when `execution_mode=Lite`).

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
4. Resolve reviewer disagreement by merging both reviewers' findings into one structured table; overall verdict is REQUEST_CHANGES if any reviewer says so.
5. Update `woos-review-context` with resolved/carry-forward findings.
6. Persist review result to the same `<workspace_root>/.ratchet/review-context/<run_id>.yaml`.
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
    "conditionally_required_invocations": ["woos-security-reviewer"],
    "actually_invoked": ["code-reviewer", "woos-review-context"],
    "missing_invocations": [],
    "invocation_evidence": [
      {
        "skill": "code-reviewer",
        "dispatch_mode": "fresh_context",
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
    "completeness_passed": true
  }
}
```

When `security_scope_detected` is `true`, `woos-security-reviewer` MUST appear in `actually_invoked`.
Missing `invocation_evidence` MUST return `BLOCKED`.
