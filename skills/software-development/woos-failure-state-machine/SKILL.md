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

1. First retryable failure -> `FAILED_RETRYABLE` -> bounded retry.
2. Retry limit reached -> `DEGRADED` if safe degraded path exists.
3. Non-retryable or unsafe degraded path -> `ESCALATED_TO_HUMAN`.
4. Human approval + recovery plan -> `RESUMED`.
5. Repeated review loop (`REQUEST_CHANGES` at/above max rounds) -> `ESCALATED_TO_HUMAN`.

## Required Controls

- `max_retries` per gate
- `timeout_seconds` per gate
- `max_review_rounds` per review gate
- `escalation_conditions`
- `resume_conditions`

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `current_state`
- `transition_reason`
- `next_action`
