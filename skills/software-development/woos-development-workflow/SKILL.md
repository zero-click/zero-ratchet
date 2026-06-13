---
name: woos-development-workflow
description: "Stage 3 of idea-to-delivery: gated engineering workflow that receives PRD, roadmap, and architecture inputs, decomposes into stories, and executes with TDD, review, and shipping gates."
version: 4.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [engineering, workflow, tdd, review, stories, traceability]
    stage: 3
    upstream: woos-product-design-flow
---

# Woos Development Workflow

## Purpose

**Stage 3** of the idea-to-delivery pipeline. Receives product design outputs from `woos-product-design-flow`, decomposes the PRD into engineering stories, and delivers a production-ready PR through gated execution.

Rule: every gate must invoke exactly one **gate wrapper skill**, then satisfy that wrapper's minimal contract.

## Product Input Contract

Engineering starts from the same feature ID used by product design:

```text
<feature-id> = <two-digit-order>-<feature-slug>
Example: 01-user-auth, 02-project-dashboard
```

**Required inputs:**

- PRD: `docs/prd/<version>/<feature-id>.md`
- Roadmap: `docs/product/<project>-roadmap.md`
- Architecture: `docs/product/<project>-architecture.md`

**Additional product design inputs when available:**

- Interface summary: `docs/prd/<version>/<feature-id>-interface.md`
- UI brief: `docs/design/<version>/<feature-id>-ui-brief.md`
- Upstream interfaces: `docs/prd/<version>/<upstream-feature-id>-interface.md`

## Baseline-First Governance

1. Default all affected domains (UI/backend/database/infra) to mainstream, maintainable, evolvable baselines.
2. Any below-baseline or outlier decision requires ADR + explicit approval.
3. Freeze constraints only when user-provided or ADR-approved.
4. Design/code review gates must fail when deviation lacks ADR+approval evidence.

## Git Branch/Worktree Policy

- `git-workflow` is required for branch strategy, commit/PR flow, and merge/rebase conventions.

Mandatory bootstrap:

1. Invoke `woos-run-orchestrator` first to initialize run state and produce `run_id`.
2. Review gates MUST NOT run without orchestrator-issued `run_id`.

## Execution Profiles

Default profile is **Standard**.  
Use **Lite** only for low-risk small changes that do not need a structured plan or independent plan review.

### Lite (small/low-risk)

```text
Run Orchestrator → Git → Product Intake → Implement → Verify → Review → Ship → Workflow Memory
```

Criteria: limited scope, low coupling, no architecture/API changes, no security impact.

Lite skips Gate 1 (Feature Plan) and Gate 1R (Plan Review). Review (formerly Code Review) and Ship (formerly PR Readiness) still run, but their `spec_alignment` / `traceability` checks omit the engineering-plan artifact and skip the AC-coverage / scope-drift checks (see those skills' Lite Mode Adjustments).

### Standard (default full-gate flow)

```text
Run Orchestrator → Git → Product Intake → Feature Plan → Plan Review → Story Loop (TDD+Implement+Verify) → Review → Ship → Workflow Memory
```

Use when: default for product-designed features, multi-file change, design choices needed, moderate/high risk, security-sensitive scope, significant architecture/API/UI/database changes, or full traceability required.

Standard includes conditional hard gates such as API design review, browser QA, database migration review, deployment patterns, security review, production audit, and architecture conformance when their triggers apply.

## Skill Whitelist

Only these skills are allowed in this workflow:

| Gate | Skill | Source |
|------|-------|--------|
| Run Orchestrator | `woos-run-orchestrator` | local |
| Git Workflow | `git-workflow` | imported |
| Product Intake | _(reads PRD + roadmap + architecture)_ | from product pipeline |
| Codebase Onboarding | `codebase-onboarding` | imported (first run) |
| Feature Plan | `woos-feature-plan` | local |
| ADR Capture | `architecture-decision-records` | imported |
| API Design Review | `api-design` | imported (conditional) |
| Plan Review | `woos-plan-review-gate` | local |
| TDD | `tdd-workflow` | imported |
| Implement | `coding-standards` | imported |
| Database Migrations | `database-migrations` | imported (conditional) |
| Verify | `verification-loop` | imported |
| E2E Testing | `e2e-testing` | imported (conditional) |
| Browser QA | `browser-qa` | imported (conditional) |
| Review (code + security + AC coverage + scope drift) | `woos-code-review-gate` | local |
| Security Review | `security-review` | imported |
| Deployment Patterns | `deployment-patterns` | imported (conditional) |
| Production Audit | `woos-production-audit` | local (conditional) |
| Ship (traceability matrix + PR readiness) | `woos-pr-readiness` | local |
| Workflow Memory | `woos-workflow-memory` | local |
| Review Context (cross-gate) | `woos-review-context` | local |
| Failure State Machine | `woos-failure-state-machine` | local |
| Systematic Debugging | `woos-systematic-debugging` | local |
| Human Handoff | `woos-human-handoff` | local |

If a required skill is unavailable, status is `BLOCKED` and the workflow stops.

## Gate Status Model

- `NOT_RUN`: required skill was not invoked
- `BLOCKED`: required skill unavailable or external dependency missing
- `REQUEST_CHANGES`: gate failed, revise and rerun
- `PASS`: gate complete, proceed to next

Progression rule: `NOT_RUN/BLOCKED/REQUEST_CHANGES → PASS → next gate`

## Enforcement Rules (Non-Negotiable)

These rules prevent known failure modes observed in production agent runs.

### E1: Sub-Agent Knowledge Injection Protocol

Before dispatching ANY review sub-agent (Gate 1R, Gate 3), the orchestrator MUST:

1. Read the relevant imported skill file(s) for that gate
2. Inject the full skill content into the sub-agent's context/prompt
3. The sub-agent must receive domain knowledge, not just a role name

**Gate 1R dispatch must include:** full content of `woos-plan-review-gate` + `architecture-decision-records`
**Gate 3 dispatch must include:** full content of `security-review` (+ `woos-production-audit` if applicable)

Skipping this = sub-agent works without methodology = shallow "LGTM" output.

### E2: Structured Review Output Format

All review gates (1R, 3) MUST produce structured findings, not prose verdicts.

**Required output format:**

```markdown
## Review: <gate name>

### Findings
| # | Severity | Category | Finding | Location | Recommendation |
|---|----------|----------|---------|----------|----------------|
| 1 | critical | security | ... | src/auth.go:42 | ... |
| 2 | warning  | design   | ... | ... | ... |

### Verdict
- Status: PASS / REQUEST_CHANGES
- Blockers: <count>
- Warnings: <count>

### Evidence
- Files reviewed: <list>
- Skills applied: <list>
- Time spent: <duration>
```

A review that returns only "PASS" or "Looks good" without the findings table is INVALID. Rerun.

### E3: Conditional Skill Activation Rules

Conditional skills activate based on these concrete triggers (not agent judgment):

| Skill | Triggers When |
|-------|--------------|
| `api-design` | PRD or interface summary defines REST/GraphQL endpoints, OR plan defines new API routes |
| `browser-qa` | PRD or UI brief describes UI behavior, OR stories produce `.tsx`/`.vue`/`.svelte`/HTML files |
| `e2e-testing` | Stories produce integration test files, OR PRD AC reference user flows spanning multiple pages |
| `database-migrations` | Plan defines schema changes, OR stories create/modify migration files |
| `deployment-patterns` | Plan has rollout/rollback section with deployment/infra changes, or migration rollout risk |
| `woos-production-audit` | PRD flags security/compliance-sensitive scope, high-risk rollout, or production reliability risk |
| `security-review` | Any story touches auth, input validation, secrets, API endpoints, or payment flows |
| `codebase-onboarding` | First run on this repository (no prior run-manifest exists) |

**Rule:** If trigger condition is met, activation is MANDATORY, not optional. Agent cannot skip.

---

## Gate Definitions

### Gate 0 — Product Intake

**Required input:**

- PRD: `docs/prd/<version>/<feature-id>.md`
- Roadmap: `docs/product/<project>-roadmap.md`
- Architecture: `docs/product/<project>-architecture.md`

**Additional product design input when available:**

- Interface summary: `docs/prd/<version>/<feature-id>-interface.md`
- UI brief: `docs/design/<version>/<feature-id>-ui-brief.md`
- Upstream interfaces: `docs/prd/<version>/<upstream-feature-id>-interface.md`

**Minimal contract:**

1. Required product inputs exist.
2. PRD contains goals/background, functional requirements, acceptance criteria, and edge cases.
3. Roadmap provides product direction and selected version context.
4. Architecture provides system constraints.
5. Record product input paths and feature ID in run-manifest for traceability.

**If required inputs do NOT exist:** Redirect to `woos-product-design-flow`. Do not proceed without PRD, roadmap, and architecture.

### Gate 1 — Feature Plan

**Skill:** `woos-feature-plan`

**Minimal contract:**

1. Plan artifact at `docs/engineering/<version>/<feature-id>-plan.md` containing: Overview, Architecture, Test Strategy, Rollout & Rollback, Security & Risk, Baseline & Deviation Decision Record, and Story Table.
2. Architecture / baseline / risk / rollout sections authored via `woos-architect` (`mode: author`).
3. Story Table validated by `woos-product-planner` (`mode: planning`) before the plan is finalized.
4. If API endpoints are defined or changed: invoke `api-design` for review.
5. If database schema changes: reference `database-migrations` for migration strategy.
6. If deployment strategy needed: reference `deployment-patterns` for rollout/rollback.
7. Baseline/deviation rows complete for every affected domain; deviations captured via `architecture-decision-records`.
8. Story Table satisfies the Gate 1 hard rules from `woos-feature-plan`:
   - Every PRD AC mapped to ≥1 story (no orphan AC)
   - DAG (no cycles), all `Depends` references resolve
   - Concrete `Diff Scope` per story (no globs, no prose); no two unordered stories share a file
   - Hard cap of 3 strongly-coupled AC per story
9. Interface/API contracts and data-model details are NOT duplicated here — those live in `docs/prd/<version>/<feature-id>-interface.md` (produced by product flow Step 6.5).

### Gate 1R — Plan Review

**Skill:** `woos-plan-review-gate`

**Minimal contract:**

1. Two independent reviewers dispatched in fresh context:
   - `woos-architect` (`mode: review`) on architecture / baseline / risk / rollout / security sections
   - `woos-product-planner` (`mode: story-review`) on the Story Table section
2. Sub-agents MUST be injected with relevant skill content (per E1): `architecture-decision-records` for the architect; `woos-product-planner` story-review dimensions for the planner.
3. Output MUST follow structured findings format (per E2), split by reviewer.
4. Uses `woos-review-context` to load/update cumulative findings.
5. Reviewer-conflict rule: any REQUEST_CHANGES → overall REQUEST_CHANGES (no separate arbitration skill needed; both reviewers' findings are merged into the structured output).
6. Returns `PASS` or `REQUEST_CHANGES`.
7. Escalates to `woos-human-handoff` when review loop threshold (2 rounds) exceeded.

### Gate 2 — Story Execution Loop

Execute stories in dependency order (`run-manifest.yaml: gate-1-plan.execution_order`). For **each story**, look up its row in the Story Table section of `docs/engineering/<version>/<feature-id>-plan.md` for the linked AC and allowed diff scope:

#### 3.1 TDD

**Skill:** `tdd-workflow`

1. **RED**: Write failing test for the AC linked to this story (test file must live inside the story's `Diff Scope`)
2. **GREEN**: Implement minimum code to pass
3. **REFACTOR**: Clean up while keeping tests green

If RED-GREEN stalls (2+ consecutive failed attempts): activate `woos-systematic-debugging`.

#### 3.2 Implement

**Skill:** `coding-standards`

- Implement strictly within the story's `Diff Scope`; any change outside is a deviation and MUST be reported.
- The linked PRD AC defines what behavior to produce; the tests written in step 3.1 define how PASS is judged. There is no separate "implementation tasks" checklist and no per-story narrative — the PRD AC + the test files ARE the source of truth.
- Changes are minimal, scoped, convention-aligned.
- Design issue discovered → write DCR (see DCR section), do NOT improvise.

#### 3.3 Verify

**Skill:** `verification-loop`

- Run the project's test runner. PASS = green for the new tests AND no regression in previously passing tests.
- Run lint / type check.
- Capture command output (exit code + last lines of stdout/stderr) into `run-manifest.yaml` under `gate_results.gate-2-execution.<story-id>.failure_log` on failure.

#### 3.4 Story Verification Gate

Per-story check:
- **PASS** (new tests green, no regressions, lint/typecheck clean) → mark story `status: completed` in run-manifest, next story
- **FAIL (1st)** → append attempt to runtime `failure_log`, fix within the story's `Diff Scope` and retry
- **FAIL (2nd)** → activate `woos-systematic-debugging`
- **FAIL (3rd)** → rollback with `git restore -- <diff_scope>` (or `git revert <range>` if already committed), mark `status: blocked`, continue with other stories

#### 3.5 Failure Isolation

- A blocked story does NOT block independent stories (per the DAG)
- Blocked stories are retried after all other stories complete
- On retry, revert state via `git restore -- <diff_scope>` first; do not stack failed attempts
- If still blocked → write DCR with context (see DCR section)

### Gate 3 — Review

**Skill:** `woos-code-review-gate`

This single gate absorbs what previous iterations split across Executable Acceptance, Deviation Control, and Code/Security Review. The hard rules below run in one pass against the diff + plan + PRD.

1. Dispatch `woos-code-reviewer` in fresh context (no self-review).
2. Sub-agent MUST be injected with relevant skill content (per E1):
   - Always: `coding-standards` knowledge
   - If security-sensitive (per E3 triggers): full `security-review` skill content
3. If security-sensitive: dispatch `woos-security-reviewer` with `security-review` knowledge.
4. If the woos-code-reviewer flags an architecture-level concern beyond the approved plan, dispatch `woos-architect` with `mode: consult` to confirm interpretation before final verdict. Independent architecture review is owned by Gate 1R; Gate 3 escalates findings rather than re-deriving the architecture verdict.
5. If applicable (per E3 triggers): invoke `woos-production-audit` for pre-merge readiness.
6. Output MUST follow structured findings format (per E2). "LGTM" without findings table = INVALID, rerun.
7. Standard-mode hard checks (skipped in Lite):
   - **AC coverage** — every PRD AC listed in the plan's Story Table has at least one passing test in scope (`ac_coverage_status: PASS`).
   - **Scope drift** — every file in the diff appears in some story's declared `Diff Scope`, or is recorded as an intentional deviation with rationale (`scope_drift_status: PASS`).
   - **Spec alignment / baseline deviation** — already in the skill's contract; baseline deviations need ADR + approval.
8. Uses `woos-review-context` for cumulative findings.
9. Reviewer-conflict rule: any REQUEST_CHANGES → overall REQUEST_CHANGES. Both reviewers' findings are merged in the structured output table.
10. **PASS** → Gate 4. **REQUEST_CHANGES** → return to Gate 2 (specific story or plan update).
11. 2 rounds without convergence → `woos-human-handoff`.

### Gate 4 — Ship

**Skill:** `woos-pr-readiness` (readiness check + traceability matrix) + `git-workflow` (PR creation)

1. Re-run `verification-loop` as a final safety net (catches any regression introduced after the last Gate 2 story finished).
2. All tests pass (unit + integration + e2e as applicable). Lint clean, type check passes.
3. No TODO/FIXME/HACK without linked issues.
4. **Generate** `docs/traceability/<version>/<feature-id>-traceability.md` mechanically from the plan's Story Table + last verification-loop test outcomes (Standard mode only; skipped in Lite). The same matrix is inlined into the PR body.
5. Conventional commit messages.
6. PR description includes: story summary, test plan, traceability matrix, blocked stories (if any with DCR refs).
7. When `woos-pr-readiness` returns `PASS`, dispatch `git-workflow` to run `gh pr create`. PR creation is NOT performed by the readiness skill. Record the resulting PR URL in `run-manifest.yaml` under `gate-4-pr.pr_url`.

### Post — Workflow Memory Update

**Skill:** `woos-workflow-memory`

1. Capture failures, rework causes, mitigation patterns.
2. Record story decomposition quality (too granular? too broad?).
3. Record whether DCR was triggered and outcome.
4. Persist reusable guidance for next run.

---

## DCR (Design Change Request)

**Trigger:** At any step, if a design issue is discovered that cannot be resolved within scope.

**Action:**

1. Write `docs/feedback/<version>/<feature-id>-dcr-<NNN>.md` (`<NNN>` zero-padded, starting at `001`; allocate the next free number — never overwrite an existing DCR file, since one feature may produce multiple DCRs during a single run):

```markdown
# DCR: <Issue Title>

## Issue Description
(What's wrong with the current design)

## Impact Scope
(Which implementation tasks / AC / stories are affected)

## Proposed Resolution
(Suggested fix)

## Priority
(blocking / non-blocking)
```

2. Stop work on affected stories.
3. Continue with unaffected stories if possible.
4. DCR flows back to the upstream product-design stage for resolution.

---

## Step Completion Rule (MANDATORY)

After completing ANY gate, you MUST:

1. Update `run-manifest.yaml` — mark the gate as `completed`.
2. State: **"Gate N: <name> — DONE ✅. Next: Gate N+1: <name>"**
3. Do NOT proceed to the next gate until current gate's work is confirmed.

**Run-manifest `gates` format:**

```yaml
gates:
  gate-0-product-intake: completed
  gate-1-plan: completed
  gate-1r-review: completed
  gate-2-execution: in_progress
  gate-3-review: pending
  gate-4-pr: pending
  post-memory: pending
```

---

## Lite Mode (simplified)

| Step | Skill | What |
|------|-------|------|
| L0 | `woos-run-orchestrator` + `git-workflow` | Run bootstrap + git baseline |
| L1 | `woos-product-intake` (Gate 0) | Read product inputs (PRD, roadmap, architecture, optional interface/UI) |
| L2 | direct implementation | Implement tasks directly (no story decomposition) |
| L3 | `verification-loop` | Verify (test + lint) |
| L4 | `woos-code-review-gate` | Independent code review in fresh context (`execution_mode=Lite`, engineering-plan omitted, AC-coverage & scope-drift checks skipped) |
| L5 | `woos-pr-readiness` + `git-workflow` | Readiness check then PR creation via `gh pr create` (no traceability matrix in Lite) |
| L6 | `woos-workflow-memory` | Capture failures and reusable patterns |

Lite explicitly skips: Gate 1 Feature Plan, Gate 1R Plan Review.

---

## Failure Handling

| Situation | Action |
|-----------|--------|
| Product inputs missing or invalid | BLOCKED — redirect to product pipeline |
| Single story fails 3× | Mark BLOCKED, continue others |
| Build/test fails 2× (within story) | `woos-systematic-debugging` |
| Review fails 2× | `woos-human-handoff` escalation |
| Design issue found | DCR → back to product pipeline |
| Overall timeout | `woos-failure-state-machine` (retry → degrade → escalate) |
| Required skill unavailable | BLOCKED — report which skill |
| All stories blocked | `woos-human-handoff` — fundamental design issue |

## Stop Conditions

Stop and surface blocker when:

- Required skill not invoked (`NOT_RUN`)
- Required skill unavailable (`BLOCKED`)
- Gate returns `REQUEST_CHANGES`
- Review loop threshold exceeded without convergence

## Runtime Control

Cross-gate control skills:

- `woos-run-orchestrator`: queue policy, concurrency limits, timeout/retry
- `woos-failure-state-machine`: deterministic transition (retry → degrade → human_handoff)
- `woos-human-handoff`: escalation trigger, handoff payload, resume conditions
- `woos-review-context`: cumulative findings across review gates

Persistence:

- Run manifest: `<workspace_root>/hep/runs/<run_id>/run-manifest.yaml`
- Review context: `<workspace_root>/hep/review-context/<run_id>.yaml`
- Engineering plan (incl. Story Table): `<workspace_root>/docs/engineering/<version>/<feature-id>-plan.md`
- For gated runs, `run_id` is mandatory; if missing, return `BLOCKED`.

## File Layout

```text
<project-root>/
├── hep/
│   ├── runs/<run_id>/
│   │   └── run-manifest.yaml
│   └── review-context/<run_id>.yaml
├── docs/
│   ├── product/<project>-roadmap.md      ← required input
│   ├── product/<project>-architecture.md ← required input
│   ├── prd/<version>/<feature-id>.md     ← required input
│   ├── prd/<version>/<feature-id>-interface.md ← optional product input
│   ├── design/<version>/<feature-id>-ui-brief.md ← optional product input if UI
│   ├── engineering/<version>/<feature-id>-plan.md ← output of Gate 1 (incl. Story Table)
│   ├── feedback/<version>/<feature-id>-dcr-<NNN>.md ← DCR output (back to product-design stage, one file per DCR)
│   └── traceability/<version>/<feature-id>-traceability.md ← traceability output
└── (implementation files)
```
