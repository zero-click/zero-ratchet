---
name: woos-development-workflow
description: "Stage 3 of idea-to-delivery: gated engineering workflow that receives PRD, roadmap, and architecture inputs, decomposes into stories, and executes with TDD, traceability, and review gates."
version: 3.0.0
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
- `dmux-workflows` is required only when running parallel coding lanes.

Mandatory bootstrap:

1. Invoke `woos-run-orchestrator` first to initialize run state and produce `run_id`.
2. Review gates MUST NOT run without orchestrator-issued `run_id`.

## Execution Profiles

Default profile is **Standard**.  
Use **Lite** only for low-risk small changes that do not need story decomposition or independent design review.

### Lite (small/low-risk)

```text
Run Orchestrator → Git → Product Intake → Implement → Verify → Code Review → PR Readiness → Workflow Memory
```

Criteria: limited scope, low coupling, no architecture/API changes, no security impact.

Lite skips Gate 1 (Feature Design), Gate 1R (Design Review), Gate 2 (Story Decomposition), Gate 4 (Executable Acceptance), Gate 5 (Deviation Control), and Gate 6 (Traceability). Code Review and PR Readiness still run, but their `spec_alignment` / `traceability` checks omit the engineering-design artifact (see those skills' Lite Mode Adjustments).

### Standard (default full-gate flow)

```text
Run Orchestrator → Git → Product Intake → Feature Design → Design Review → Story Decomposition → Story Loop (TDD+Implement+Verify) → Executable Acceptance → Deviation Control → Traceability → Code Review → PR Readiness → Workflow Memory
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
| Parallel Orchestration | `dmux-workflows` | imported |
| Feature Design | `woos-feature-design` | local |
| ADR Capture | `architecture-decision-records` | imported |
| API Design Review | `api-design` | imported (conditional) |
| Design Review | `woos-design-review-gate` | local |
| TDD | `tdd-workflow` | imported |
| Implement | `coding-standards` | imported |
| Database Migrations | `database-migrations` | imported (conditional) |
| Verify | `verification-loop` | imported |
| E2E Testing | `e2e-testing` | imported (conditional) |
| Browser QA | `browser-qa` | imported (conditional) |
| Executable Acceptance | `woos-executable-acceptance-gate` | local |
| Deviation Control | `woos-deviation-control-gate` | local |
| Code/Security Review | `woos-code-review-gate` | local |
| Security Review | `security-review` | imported |
| Deployment Patterns | `deployment-patterns` | imported (conditional) |
| Production Audit | `production-audit` | imported (conditional) |
| PR Readiness | `woos-pr-readiness` | local |
| Workflow Memory | `woos-workflow-memory` | local |
| Review Context (cross-gate) | `woos-review-context` | local |
| Agent Decision (conflicts) | `woos-agent-decision` | local |
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

Before dispatching ANY review sub-agent (Gate 1R, Gate 7), the orchestrator MUST:

1. Read the relevant imported skill file(s) for that gate
2. Inject the full skill content into the sub-agent's context/prompt
3. The sub-agent must receive domain knowledge, not just a role name

**Gate 1R dispatch must include:** full content of `woos-design-review-gate` + `architecture-decision-records`
**Gate 7 dispatch must include:** full content of `security-review` (+ `production-audit` if applicable)

Skipping this = sub-agent works without methodology = shallow "LGTM" output.

### E2: Structured Review Output Format

All review gates (1R, 7) MUST produce structured findings, not prose verdicts.

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
| `api-design` | PRD or interface summary defines REST/GraphQL endpoints, OR design doc defines new API routes |
| `browser-qa` | PRD or UI brief describes UI behavior, OR stories produce `.tsx`/`.vue`/`.svelte`/HTML files |
| `e2e-testing` | Stories produce integration test files, OR PRD AC reference user flows spanning multiple pages |
| `database-migrations` | Design doc defines schema changes, OR stories create/modify migration files |
| `deployment-patterns` | Design doc has rollout/rollback section, deployment/infra changes, or migration rollout risk |
| `production-audit` | PRD flags security/compliance-sensitive scope, high-risk rollout, or production reliability risk |
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

### Gate 1 — Feature Design

**Skill:** `woos-feature-design`

**Minimal contract:**

1. Design artifact at `docs/engineering/<version>/<feature-id>-design.md`.
2. Covers: architecture, data model, interfaces, risk, rollout/rollback.
3. If API endpoints are defined or changed: invoke `api-design` for review.
4. If database schema changes: reference `database-migrations` for migration strategy.
5. If deployment strategy needed: reference `deployment-patterns` for rollout/rollback.
6. Baseline/deviation fields complete; deviations captured via `architecture-decision-records`.

### Gate 1R — Design Review

**Skill:** `woos-design-review-gate`

**Minimal contract:**

1. Independent design review using `architect` via local gate skill.
2. Sub-agent MUST be injected with `architecture-decision-records` skill content (per E1).
3. Output MUST follow structured findings format (per E2).
4. Uses `woos-review-context` to load/update cumulative findings.
5. Returns `PASS` or `REQUEST_CHANGES`.
6. Escalates to `woos-human-handoff` when review loop threshold (2 rounds) exceeded.

### Gate 2 — Story Decomposition

**Skill:** built-in (orchestrator decomposes)

Parse PRD, roadmap, architecture, and the engineering design artifact. Decompose into independent stories. Each story is a self-contained unit of work.

**Story file format:**

```markdown
# Story <NNN>: <task name>

## Implementation Tasks
- [ ] Task 1
- [ ] Task 2

## Acceptance Criteria
- AC-01: ...

## Verification
- Unit test: ...
- Integration test: ...

## Dependencies
- None (or: depends on story-NNN)

## Status: pending
```

**Output:** `docs/stories/<version>/<feature-id>/story-001.md`, `story-002.md`, ...

**Rules:**
- Each story covers 1–3 related PRD requirements, AC, or engineering design tasks
- Stories have clear dependencies (DAG order)
- Each story is independently verifiable
- Total stories should be manageable (typically 3–8 per feature)

### Gate 3 — Story Execution Loop

Execute stories in dependency order. For **each story**:

#### 3.1 TDD

**Skill:** `tdd-workflow`

1. **RED**: Write failing test for the story's behavior
2. **GREEN**: Implement minimum code to pass
3. **REFACTOR**: Clean up while keeping tests green

If RED-GREEN stalls (2+ consecutive failed attempts): activate `woos-systematic-debugging`.

#### 3.2 Implement

**Skill:** `coding-standards`

- Follow implementation tasks within the story
- Changes are minimal, scoped, convention-aligned
- Design issue discovered → write DCR (see DCR section), do NOT improvise

#### 3.3 Verify

**Skill:** `verification-loop`

- Run tests for the current story
- Run lint / type check
- Verify story-level AC

#### 3.4 Story Verification Gate

Per-story AC check:
- **PASS** → mark story `status: completed`, next story
- **FAIL (1st)** → fix and retry
- **FAIL (2nd)** → activate `woos-systematic-debugging`
- **FAIL (3rd)** → mark story `status: blocked`, continue with other stories

#### 3.5 Failure Isolation

- A blocked story does NOT block independent stories
- Blocked stories are retried after all other stories complete
- If still blocked → write DCR with context

### Gate 4 — Executable Acceptance

**Skill:** `woos-executable-acceptance-gate`

After ALL stories complete (or remaining are blocked):
1. Map ALL PRD AC to executable checks.
2. Missing automation is tracked as a blocker.
3. **PASS** → Gate 5. **REQUEST_CHANGES** → return to Gate 3 (specific story).

### Gate 5 — Deviation Control

**Skill:** `woos-deviation-control-gate`

1. Compare implementation against PRD, product architecture, and engineering design artifacts.
2. Unresolved deviations block progression.
3. Intentional deviations require updated artifacts + rationale.
4. **PASS** → Gate 6. **REQUEST_CHANGES** → return to Gate 3.

### Gate 6 — Requirement Traceability

**Skill:** built-in (traceability procedure)

Trace from original PRD through design to implementation and tests.

**Procedure:**

1. Read PRD from `docs/prd/<version>/<feature-id>.md`
2. Read engineering design from `docs/engineering/<version>/<feature-id>-design.md`
3. For each PRD AC, trace the chain:

| PRD AC | Design Spec | Code | Test | Status |
|--------|-------------|------|------|--------|
| AC-4.5.1 | §API endpoint | routes/tasks.py:fn | test_file:test_fn | ✅ Aligned |
| AC-6.2 | §Data model | N/A | N/A | ❌ Missing |

4. Classify each AC:
   - **✅ Aligned** — PRD, design, code, test all match
   - **⚠️ Deviated** — implemented differently (rationale required)
   - **❌ Missing** — not implemented or not tested
   - **🆕 Added** — implemented but not in PRD (extra scope)

5. Write output to `docs/traceability/<version>/<feature-id>-traceability.md`

**Gate rules:**
- **PASS** — all ACs ✅ or ⚠️ with rationale, zero ❌
- **REQUEST_CHANGES** — any ❌, or ⚠️ without rationale → return to Gate 3

### Gate 7 — Code/Security Review

**Skill:** `woos-code-review-gate`

1. Dispatch `code-reviewer` in fresh context (no self-review).
2. Sub-agent MUST be injected with relevant skill content (per E1):
   - Always: `coding-standards` knowledge
   - If security-sensitive (per E3 triggers): full `security-review` skill content
3. If security-sensitive: dispatch `security-reviewer` with `security-review` knowledge.
4. If the code-reviewer flags an architecture-level concern (component boundary, data model, or API contract change beyond the approved design), dispatch `architect` with `mode: consult` to confirm interpretation before final verdict. Independent architecture conformance is owned by Gate 1R (for the design) and Gate 5 (for drift); Gate 7 escalates findings rather than re-deriving the architecture verdict.
5. If applicable (per E3 triggers): invoke `production-audit` for pre-merge readiness.
6. Output MUST follow structured findings format (per E2). "LGTM" without findings table = INVALID, rerun.
7. Uses `woos-review-context` for cumulative findings.
8. Uses `woos-agent-decision` when reviewer verdicts conflict.
9. **PASS** → Gate 8. **REQUEST_CHANGES** → return to Gate 3.
10. 2 rounds without convergence → `woos-human-handoff`.

### Gate 8 — PR Readiness

**Skill:** `woos-pr-readiness` (readiness check) + `git-workflow` (PR creation)

1. All tests pass (unit + integration + e2e as applicable).
2. Lint is clean, type check passes.
3. No TODO/FIXME/HACK without linked issues.
4. Traceability matrix provided (requirement → test → code).
5. Conventional commit messages.
6. PR description includes: story summary, test plan, blocked stories (if any with DCR refs).
7. When `woos-pr-readiness` returns `PASS`, dispatch `git-workflow` to run `gh pr create`. PR creation is NOT performed by the readiness skill. Record the resulting PR URL in `run-manifest.yaml` under `gate-8-pr.pr_url`.

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
  gate-1-design: completed
  gate-1r-review: completed
  gate-2-stories: completed
  gate-3-execution: in_progress
  gate-4-acceptance: pending
  gate-5-deviation: pending
  gate-6-traceability: pending
  gate-7-codereview: pending
  gate-8-pr: pending
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
| L4 | `woos-code-review-gate` | Independent code review in fresh context (`execution_mode=Lite`, engineering-design omitted from spec alignment) |
| L5 | `woos-pr-readiness` + `git-workflow` | Readiness check then PR creation via `gh pr create` |
| L6 | `woos-workflow-memory` | Capture failures and reusable patterns |

Lite explicitly skips: Gate 1 Feature Design, Gate 1R Design Review, Gate 2 Story Decomposition, Gate 4 Executable Acceptance, Gate 5 Deviation Control, Gate 6 Traceability.

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
- `woos-agent-decision`: conflict resolution when reviewers disagree

Persistence:

- Run manifest: `<workspace_root>/hep/runs/<run_id>/run-manifest.yaml`
- Review context: `<workspace_root>/hep/review-context/<run_id>.yaml`
- Stories: `<workspace_root>/docs/stories/<version>/<feature-id>/`
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
│   ├── engineering/<version>/<feature-id>-design.md ← output of Gate 1
│   ├── stories/<version>/<feature-id>/   ← output of Gate 2
│   │   ├── story-001.md
│   │   ├── story-002.md
│   │   └── ...
│   ├── feedback/<version>/<feature-id>-dcr-<NNN>.md ← DCR output (back to product-design stage, one file per DCR)
│   └── traceability/<version>/<feature-id>-traceability.md ← traceability output
└── (implementation files)
```
