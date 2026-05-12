---
name: woos-human-handoff
description: Define explicit escalation, takeover payload, and resume protocol for autonomous workflow failures.
version: 1.1.0
author: Hermes Profile
license: MIT
---

# Woos Human Handoff

## Purpose

Standardize when and how autonomous execution escalates to a human operator.

## Escalation Triggers

- Retry budget exhausted
- Review-loop threshold exceeded (`REQUEST_CHANGES` repeats)
- Critical security or compliance uncertainty
- Contradictory requirements blocking deterministic output
- High-risk production-impacting change without confidence

## Required Handoff Payload

- `run_id`
- `failed_stage`
- `failure_summary`
- `attempts_made`
- `review_rounds_attempted`
- `artifacts_reviewed`
- `recommended_next_actions`
- `resume_conditions`

## Resume Rules

- Human decision must be explicit: `approve_resume` | `change_scope` | `abort`.
- Resumed run starts from the failed gate unless scope changed.
- All human overrides must be logged in final PR readiness notes.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `handoff_required`: boolean
- `handoff_payload`
- `resume_decision`
