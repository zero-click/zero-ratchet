---
name: woos-pr-readiness
description: Final pre-PR readiness gate for Hermes workflow. Confirms diff quality, verification visibility, traceability, and commit/PR discipline.
version: 1.2.0
author: Hermes Profile
license: MIT
---

# Woos PR Readiness

## Purpose

Confirm work is ready for commit/PR handoff.

## Required Invocation (hard gate)

- MUST invoke `verification-loop` first.
- If `verification-loop` is not invoked, return `NOT_RUN` and stop.
- If unavailable, return `BLOCKED` and stop.
- Do not replace with manual "looks good" checks only.

## Contract

- Check git diff/status is understood and scoped
- Check verification outcomes are explicitly reported
- Check conventional commit and PR test plan readiness
- Check implementation traceability against approved artifacts that exist for the active mode:
  - **Standard:** PRD, roadmap, architecture, engineering design, supporting interface/UI artifacts when available.
  - **Lite:** PRD, roadmap, architecture, supporting interface/UI artifacts when available. There is no engineering-design artifact in Lite (Gate 1 is skipped); absence of `engineering-design` MUST NOT cause `REQUEST_CHANGES` and MUST NOT be fabricated.
- Check artifact updates are complete when intentional deviations exist
- Return `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output fields (required):
  - `verification_skill_used: verification-loop`
  - `verification_summary`
  - `execution_mode: Lite | Standard`
  - `engineering_design_present: true|false`
  - `traceability_matrix` (AC/requirement -> test -> code changes)
  - `artifact_sync_status: PASS | REQUEST_CHANGES`
  - `artifact_update_notes`

Gate passes only when `artifact_sync_status` is `PASS`.

## Post-Pass Action (PR creation)

When the gate returns `PASS`, the orchestrator MUST dispatch `git-workflow` to run `gh pr create` using the test plan and traceability summary produced here. PR creation is NOT performed by this skill; this skill only certifies readiness. The orchestrator records the resulting PR URL in `run-manifest.yaml` under `gate-8-pr.pr_url`.
