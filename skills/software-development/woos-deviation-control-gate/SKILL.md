---
name: woos-deviation-control-gate
description: Block unresolved implementation drift against PRD, product context, and engineering design artifacts.
version: 1.1.0
author: Hermes Profile
license: MIT
---

# Woos Deviation Control Gate

## Purpose

Stop silent drift between planned intent and final implementation.

## Required Inputs

- Approved PRD
- Approved engineering design artifact (Standard mode only; absent in Lite — see Lite Mode Adjustments below)
- Product context artifacts: roadmap + architecture (+ interface summary/UI brief/upstream interfaces when available)
- Current implementation diff and test results

## Required Invocation (hard gate)

- MUST dispatch `code-reviewer` (or an equivalent whitelisted reviewer) in fresh context with a deviation-control focus. In-context self-review where the implementer's session re-labels itself as reviewer is NOT a valid invocation.
- The dispatched agent receives only the inputs listed above plus prior review context. It MUST NOT inherit the implementer's session history.
- MUST invoke `woos-review-context` before and after reviewer execution.
- If the reviewer is not invoked, return `NOT_RUN` and stop.
- If the reviewer is unavailable, return `BLOCKED` and stop.
- `invocation_evidence` MUST include `dispatch_mode: "fresh_context"`. Any other value MUST return `BLOCKED`.

## Drift Classification

- `none`
- `intentional_documented`
- `intentional_undocumented`
- `unintentional`

## Hard Gate Rules

- `intentional_undocumented` or `unintentional` => `REQUEST_CHANGES`.
- `intentional_documented` only passes when all affected artifacts are updated.
- Unknown artifact baseline => `BLOCKED`.

## Lite Mode Adjustments

- In Lite mode there is no engineering-design artifact (Gate 1 is skipped). Drift classification is performed against PRD + roadmap + architecture + supporting interface/UI artifacts only.
- Absence of `engineering-design` in Lite is expected and MUST NOT be classified as drift or BLOCKED.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- `execution_mode`: `Lite` | `Standard`
- `engineering_design_present`: `true|false`
- `deviation_findings`
- `deviation_type`
- `artifact_update_required`
- `artifact_update_status`

## Machine-Readable Enforcement Output (required)

```json
{
  "enforcement": {
    "required_invocations": ["code-reviewer", "woos-review-context"],
    "actually_invoked": ["code-reviewer", "woos-review-context"],
    "missing_invocations": [],
    "invocation_evidence": [
      {
        "skill": "code-reviewer",
        "dispatch_mode": "fresh_context",
        "invoked_at": "2026-06-12T00:00:00Z",
        "artifact_ref": "git diff HEAD + docs/engineering/<version>/<feature-id>-design.md",
        "output_digest": "sha256:..."
      }
    ],
    "execution_mode": "Standard",
    "engineering_design_present": true,
    "deviation_type": "none",
    "artifact_update_required": false,
    "artifact_update_status": "n/a"
  }
}
```

Missing `invocation_evidence` MUST return `BLOCKED`. A `status: PASS` without a populated `enforcement` block is INVALID and MUST be rejected by the orchestrator.
