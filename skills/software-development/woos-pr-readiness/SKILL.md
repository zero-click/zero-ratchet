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
- Check implementation traceability against approved artifacts (PRD/design/capability)
- Check artifact updates are complete when intentional deviations exist
- Return `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output fields (required):
  - `verification_skill_used: verification-loop`
  - `verification_summary`
  - `traceability_matrix` (AC/requirement -> test -> code changes)
  - `artifact_sync_status: PASS | REQUEST_CHANGES`
  - `artifact_update_notes`

Gate passes only when `artifact_sync_status` is `PASS`.
