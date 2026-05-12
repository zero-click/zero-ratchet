---
name: woos-run-orchestrator
description: Orchestrate autonomous workflow runs with queueing, concurrency, timeout, and retry controls.
version: 1.5.0
author: Hermes Profile
license: MIT
---

# Woos Run Orchestrator

## Purpose

Provide execution control plane for near-unattended workflow runs.

## Required Runtime Policy

- `queue_policy`: FIFO | priority
- `max_concurrency`
- `timeout_seconds` per stage
- `retry_policy` (attempts + backoff)
- `cancellation_policy`
- `review_loop_policy` (`review_round_max=2`, `reconciliation_attempt_max=1`, escalation action)
- `review_context_policy` (load/update enforcement at review gates)
- `review_runtime_policy` (`max_review_runtime_seconds` per reviewer invocation)
- `agent_memory_policy` (persisted reviewer context per run)
- `run_manifest_policy` (`run_manifest_required=true`, verifier hard-fail rules)

## Run Manifest Verifier

Runtime root resolution:

- `hep_root = <workspace_root>/hep` (canonical default)
- All run artifacts MUST be persisted under `hep_root` for discoverability.
- Runtime directories are **lazy-created by orchestrator at run start**; pre-existing `runs/` is NOT required.

Required runtime directories:

- `<hep_root>/runs/<run_id>/`
- `<hep_root>/review-context/`

Required file: `<hep_root>/runs/<run_id>/run-manifest.yaml`

Required sections:

- `phase_order`
- `gate_results` (must include gate enforcement payloads)
- `baseline_decisions` (deviation status + ADR/approval refs when needed)
- `escalation_counters`
- `final_status`

If file or required sections are missing, status MUST be `BLOCKED`.

## Execution Contract

1. Admit run with a unique run id.
2. Initialize runtime directories under `<workspace_root>/hep` when missing.
3. Assign stage ownership and dependencies.
4. Enforce timeout/retry policy.
5. Emit stage status transitions.
6. Detect repeated `REQUEST_CHANGES` loops and trigger escalation.
7. Enforce review runtime limit; timeout returns `BLOCKED` and triggers handoff.
8. Verify run-manifest completeness before finalization.
9. Trigger failure state machine and human handoff when needed.

## Counter Precedence

1. If `reconciliation_attempt_max` exceeded -> `BLOCKED` + handoff.
2. Else if `review_round_max` exceeded -> `BLOCKED` + handoff.
3. Else if `max_review_runtime_seconds` exceeded -> `BLOCKED` + handoff.
4. Else if run-manifest verifier fails -> `BLOCKED` + handoff.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `run_id`
- `stage_statuses`
- `timeouts`
- `retries`
- `review_loops_detected`
- `escalations`
- `handoff_triggered`
- `run_manifest_verified`
