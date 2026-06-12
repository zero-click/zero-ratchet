---
name: woos-failure-state-machine
description: Define deterministic failure transitions for autonomous workflow runs.
version: 1.1.0
author: Hermes Profile
license: MIT
---

# Woos Failure State Machine

## Purpose

Prevent stalls and infinite loops by enforcing deterministic post-failure actions.

## State Model

- `RUNNING`
- `FAILED_RETRYABLE`
- `FAILED_NON_RETRYABLE`
- `DEGRADED`
- `ESCALATED_TO_HUMAN`
- `RESUMED`
- `COMPLETED`

## Transition Policy

1. First retryable failure -> `FAILED_RETRYABLE` -> invoke `woos-systematic-debugging` before retry.
2. Retry limit reached -> `DEGRADED` if safe degraded path exists.
3. Non-retryable or unsafe degraded path -> `ESCALATED_TO_HUMAN`.
4. Human approval + recovery plan -> `RESUMED`. The recovery plan MUST specify `resume_gate` (the gate to re-enter); default is the gate that triggered the escalation. The orchestrator re-enters that gate at round 0 with the human-supplied corrective context.
5. Repeated review loop (`REQUEST_CHANGES` at/above `review_round_max`) -> `ESCALATED_TO_HUMAN`.
6. `woos-systematic-debugging` returns `ESCALATED` (3 fix attempts exhausted) -> `ESCALATED_TO_HUMAN`.

## Required Controls

- `max_retries` per gate
- `timeout_seconds` per gate
- `review_round_max` per review gate (consistent with `woos-design-review-gate`, `woos-code-review-gate`, `woos-agent-decision`, `woos-run-orchestrator`)
- `escalation_conditions`
- `resume_conditions` (include `resume_gate`: which gate to re-enter on `RESUMED`)

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `current_state`
- `transition_reason`
- `next_action`
