# Software Development Workflow

[English](./README.md) | [中文](./README.zh.md)

The engineering half of the pipeline. Takes the product design artifacts (PRD + roadmap + architecture) and turns them into a merged, production-ready PR through gated TDD and review.

Entry skill: **`woos-development-workflow`**.

## Quick Start

1. Make sure the product inputs exist: PRD, roadmap, architecture. Missing any = `BLOCKED`.
2. Hand the agent off to `woos-development-workflow`.
3. Mode is auto-selected from PRD scope and risk (Lite vs Standard). Each gate must PASS before the next starts.

## Pipeline

```
Product inputs (PRD + roadmap + architecture)
   │
   ▼  Bootstrap   woos-run-orchestrator → git-workflow
   ▼  Gate 0      Product Intake — validate inputs, record in run-manifest
   ▼  Gate 1      Feature Plan (architecture + story table)   woos-feature-plan
   ▼  Gate 1R     Plan Review (fresh context, 2 reviewers)    woos-plan-review-gate
   ▼  Gate 2      Story Loop (per story in DAG order)
   │              ├─ 2.1 TDD             tdd-workflow
   │              ├─ 2.2 Implement       coding-standards
   │              └─ 2.3 Verify          verification-loop
   ▼  Gate 3      Review (code + security + AC coverage + scope drift)  woos-code-review-gate
   ▼  Gate 4      Ship (traceability matrix + PR readiness)              woos-pr-readiness
   ▼  Post        Workflow Memory                  woos-workflow-memory
   ▼
PR created ✅

On unresolvable design issue → DCR → docs/feedback/<version>/<feature-id>-dcr-<NNN>.md
```

## Execution Modes

| Mode | When | Skipped gates |
|------|------|---------------|
| Lite | Low-risk, single small change, no arch impact | Gates 1, 1R; Gate 3 still runs but skips AC-coverage and scope-drift checks; Gate 4 skips traceability matrix |
| Standard (default) | Anything from a product-design pipeline | none |

Mode is determined by PRD scope and risk, not by the developer.

## Gate-by-Gate

| Gate | Skill | What it produces |
|------|-------|------------------|
| 0 Product Intake | (built-in) | Validates PRD + roadmap + architecture; records paths in `run-manifest.yaml`. First run on a repo: invokes `codebase-onboarding`. |
| 1 Feature Plan | `woos-feature-plan` (uses `woos-architect` `mode: author` + `woos-product-planner` `mode: planning`) | Single per-feature `docs/engineering/<version>/<feature-id>-plan.md` containing Architecture / Test Strategy / Rollout & Rollback / Security & Risk / Baseline & Deviation / **Story Table** (`ID \| AC \| Depends \| Diff Scope`). Interface/API contracts and data model live in the PRD's `<feature-id>-interface.md`, not here. |
| 1R Plan Review | `woos-plan-review-gate` (uses `woos-architect` `mode: review` + `woos-product-planner` `mode: story-review`) | One review covering both architecture decisions and story decomposition in fresh contexts; `PASS` / `REQUEST_CHANGES`. 2 failed rounds → `woos-human-handoff`. |
| 2 Story Loop | `tdd-workflow`, `coding-standards`, `verification-loop` | Per story (DAG order from the plan's Story Table): RED→GREEN→REFACTOR → implement → verify. Conditional: `database-migrations`, `e2e-testing`, `browser-qa`. A blocked story does NOT block independent stories. |
| 3 Review | `woos-code-review-gate` → `woos-code-reviewer` (+ `woos-security-reviewer` when triggered, `woos-production-audit` when applicable) | Fresh-context review with knowledge injection (E1). Hard checks in one pass: code/security findings (structured table per E2), **AC coverage** (every PRD AC has a passing test), **scope drift** (every changed file is in some story's Diff Scope), baseline/deviation alignment. |
| 4 Ship | `woos-pr-readiness` + `git-workflow` | Re-runs `verification-loop` as a safety net, mechanically generates `docs/traceability/<version>/<feature-id>-traceability.md` from the plan's Story Table + last test outcomes, attaches it to the PR body, then creates the PR via `gh pr create`. |
| Post Workflow Memory | `woos-workflow-memory` | Persists failure/rework patterns and plan-quality signals for future runs. |
| Post Workflow Memory | `woos-workflow-memory` | Persists failure/rework patterns and plan-quality signals for future runs. |

## Story Table (inside the Gate 1 plan)

Gate 1 embeds the story execution table as a section of `docs/engineering/<version>/<feature-id>-plan.md`. A 4-column table is the whole story-side product:

```markdown
| ID  | AC           | Depends | Diff Scope                              |
|-----|--------------|---------|-----------------------------------------|
| s01 | FR-1.a       | -       | store/persist.go, store/persist_test.go |
| s02 | FR-1.b       | s01     | store/persist.go, store/persist_test.go |
| s03 | FR-3.a       | s01     | store/lifecycle.go, store/lifecycle_test.go |
```

Why so thin: PRD AC is the spec, tests inside the diff scope are the verification, `git restore -- <diff_scope>` is the rollback. Story status and failure logs are runtime state in `run-manifest.yaml`. Sizing rule: 1 PRD AC per story (hard cap 3 strongly-coupled AC sharing test setup); no two unordered stories may share a file. See `woos-feature-plan/SKILL.md` for the authoritative schema.

## Enforcement Rules

Three non-negotiable rules learned from production agent failures:

- **E1 Knowledge Injection** — before dispatching a review sub-agent, the orchestrator MUST inject the relevant skill's full content. A sub-agent with only a role name produces shallow output.
- **E2 Structured Review Output** — every review gate must emit a findings table (severity, category, finding, location, recommendation) + verdict + evidence. A bare "PASS" or "LGTM" is INVALID and triggers a rerun.
- **E3 Conditional Skill Activation** — conditional skills (`browser-qa`, `e2e-testing`, `database-migrations`, `security-review`, etc.) have concrete trigger rules. If the trigger fires, activation is mandatory — not a judgment call.

## Skill Map

**Local (`woos-*`):**
`woos-development-workflow` (entry), `woos-feature-plan`, `woos-plan-review-gate`, `woos-code-review-gate`, `woos-pr-readiness`, `woos-workflow-memory`, `woos-run-orchestrator`, `woos-failure-state-machine`, `woos-human-handoff`, `woos-review-context`, `woos-systematic-debugging`, `woos-architect`, `woos-product-planner`, `woos-code-reviewer`, `woos-security-reviewer`, `woos-production-audit`.

**Imported (`skills/ecc/`):**
`git-workflow`, `tdd-workflow`, `coding-standards`, `verification-loop`, `api-design`, `browser-qa`, `e2e-testing`, `security-review`, `architecture-decision-records`, `database-migrations`, `deployment-patterns`, `codebase-onboarding`.

## DCR (Design Change Request)

When engineering hits a design issue it cannot resolve inside scope:

1. Write `docs/feedback/<version>/<feature-id>-dcr-<NNN>.md` (issue, impact, proposed fix, priority). `NNN` is zero-padded from `001`; never overwrite — always allocate the next free number.
2. Stop affected stories. Continue unaffected ones.
3. Product pipeline updates the PRD and re-issues. Engineering resumes from the affected gate.

## File Layout

```
<project-root>/
├── hep/
│   ├── runs/<run_id>/run-manifest.yaml      ← gate progress + runtime story state
│   └── review-context/<run_id>.yaml         ← cumulative cross-gate findings
└── docs/
    ├── product/<project>-roadmap.md         ← input
    ├── product/<project>-architecture.md    ← input
    ├── prd/<version>/<feature-id>.md        ← input
    ├── prd/<version>/<feature-id>-interface.md     ← optional (Strict)
    ├── design/<version>/<feature-id>-ui-brief.md   ← optional (when UI)
    ├── engineering/<version>/<feature-id>-plan.md  ← Gate 1 (incl. Story Table)
    ├── adr/                                  ← ADR captures
    ├── feedback/<version>/<feature-id>-dcr-<NNN>.md  ← DCR
    └── traceability/<version>/<feature-id>-traceability.md  ← Gate 4 (auto-generated)
```
