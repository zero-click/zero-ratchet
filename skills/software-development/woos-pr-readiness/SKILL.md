---
name: woos-pr-readiness
description: Final pre-PR gate. Reruns verification-loop, auto-generates the traceability matrix from the plan's Stories/Tasks section + test outcomes, confirms commit/PR discipline, then triggers PR creation.
version: 2.0.0
author: Hermes Profile
license: MIT
---

# Woos PR Readiness

## Purpose

Confirm work is ready for commit/PR handoff, and produce the artifacts the PR description needs (traceability matrix + test plan summary).

## Required Invocation (hard gate)

- MUST invoke `verification-loop` first (final pass — Gate 2 already ran it per-task; this run catches any regression introduced after the last task finished).
- If `verification-loop` is not invoked, return `NOT_RUN` and stop.
- If unavailable, return `BLOCKED` and stop.
- Do not replace with manual "looks good" checks only.

## Contract

- Check git diff/status is understood and scoped
- Check verification outcomes are explicitly reported
- Check conventional commit and PR test plan readiness
- Check implementation traceability against approved artifacts that exist for the active mode:
  - **Standard:** PRD, roadmap, architecture, engineering plan, supporting interface/UI artifacts when available.
  - **Lite:** PRD, roadmap, architecture, supporting interface/UI artifacts when available. There is no engineering plan artifact in Lite (Gate 1 is skipped); absence of `engineering-plan` MUST NOT cause `REQUEST_CHANGES` and MUST NOT be fabricated.
- Check artifact updates are complete when intentional deviations exist
- **Produce the traceability matrix** as `docs/traceability/<version>/<feature-id>-traceability.md` (Standard mode only)
- Return `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output fields (required):
  - `verification_skill_used: verification-loop`
  - `verification_summary`
  - `execution_mode: Lite | Standard`
  - `engineering_plan_present: true|false`
  - `traceability_matrix_path` (Standard mode: file path of generated matrix; Lite: omitted)
  - `traceability_matrix_inline` (rendered table for embedding in the PR body)
  - `artifact_sync_status: PASS | REQUEST_CHANGES`
  - `artifact_update_notes`

Gate passes only when `artifact_sync_status` is `PASS`.

## Traceability Matrix Generation (Standard mode)

This skill OWNS the traceability artifact. Generation is a pure join over the plan's Stories/Tasks section and the last `verification-loop` results — no LLM judgment required.

**Inputs:**
- Plan's Stories section at `docs/engineering/<version>/<feature-id>-plan.md` (each story declares `AC`; each task under a story declares `Diff Scope`)
- The last `verification-loop` run's per-file test outcome (PASS/FAIL counts per test file)

**Procedure:** for each PRD AC, find the story whose `AC` list contains it; collect every task under that story; attribute every test file inside any of those tasks' `Diff Scope` to the AC. Within each file, count PASS/FAIL from the verification-loop output. No test-name → AC mapping is required, because the plan's task `Diff Scope` already declares which test files belong to which story (and thus which AC).

**Output:** `docs/traceability/<version>/<feature-id>-traceability.md`

```markdown
# <feature-id> Traceability

| PRD AC | Story | Task(s) | Test File(s) (from Diff Scope) | Last Run |
|--------|-------|---------|--------------------------------|----------|
| FR-1.a | S1    | S1.t1   | store/persist_test.go          | ✅ 4/4 PASS |
| FR-1.b | S1    | S1.t2   | store/persist_test.go          | ✅ 4/4 PASS |
| FR-3.a | S2    | S2.t1   | store/lifecycle_test.go        | ✅ 2/2 PASS |
```

Embed the same table in the PR body (via `traceability_matrix_inline`).

If any AC has no test file in any of its story's tasks' `Diff Scope`, or any test file shows a FAIL, return `REQUEST_CHANGES`. (This is a safety net — Gate 3's AC-coverage check should have caught it first.)

## Post-Pass Action (PR creation)

When the gate returns `PASS`, the orchestrator MUST dispatch `git-workflow` to run `gh pr create` using the test plan and traceability matrix produced here. PR creation is NOT performed by this skill; this skill only certifies readiness and produces the matrix. The orchestrator records the resulting PR URL in `run-manifest.yaml` under `gate-4-pr.pr_url`.

