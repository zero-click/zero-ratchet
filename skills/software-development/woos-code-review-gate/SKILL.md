---
name: woos-code-review-gate
description: Independent code/security review gate for Hermes workflow. Uses code-reviewer and security-reviewer where applicable.
version: 1.2.0
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
- If required reviewer is not invoked, return `NOT_RUN` and stop.
- If required reviewer is unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or non-whitelisted reviewer.

## Contract

- Input: current diff + linked artifacts (PRD/design/capability)
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output content: blocking and non-blocking findings
- Output fields (required):
  - `reviewers_used`
  - `code_reviewer_status`
  - `security_reviewer_status` (when required)
  - `spec_alignment_status: PASS | REQUEST_CHANGES`
  - `spec_deviation_findings`
  - `intentional_deviations`
  - `blocking_findings`

## Spec Alignment Requirements (hard gate)

- Review MUST explicitly compare implementation against linked PRD/design/capability artifacts.
- Any behavior/interface/data/policy deviation MUST be recorded in `spec_deviation_findings`.
- If deviation is intentional, add rationale and artifact update status in `intentional_deviations`.
- If unresolved deviation exists, set `spec_alignment_status: REQUEST_CHANGES`.

Gate passes only when all required reviewers are clear and `spec_alignment_status` is `PASS`.
