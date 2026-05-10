---
name: woos-development-workflow
description: Skill-first development workflow for Hermes coding profile. Every gate binds to exactly one named skill with a minimal contract.
version: 1.2.1
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [development, workflow, skill-first, tdd, review, prd, design]
---

# Woos Development Workflow

## Purpose

Use this workflow for non-trivial software work.  
Rule: every gate must invoke exactly one named skill, then satisfy that skill's minimal contract.

## Git Branch/Worktree Policy

Define git mode explicitly before implementation:

- `git-workflow` is required for branch strategy, commit/PR flow, and merge/rebase conventions.
- `dmux-workflows` is required only when running parallel coding lanes.

Minimal contract:

1. Invoke `git-workflow` before meaningful code changes.
2. Invoke `dmux-workflows` only for parallel execution.
3. If `dmux-workflows` is active, use worktree-per-worker with isolated branches.

Core path:

```text
Research -> PRD Draft -> PRD Review -> Capability Contract -> Feature Design -> Design Review -> TDD -> Implement -> Verify -> Code/Security Review -> PR Readiness
```

## Skill Whitelist

Only these skills are allowed in this workflow:

| Step | Skill | Source |
|---|---|---|
| Git Workflow | `git-workflow` | imported |
| Research | `search-first` | imported |
| Parallel Orchestration (when needed) | `dmux-workflows` | imported |
| PRD Draft | `woos-prd-authoring` | local |
| PRD Review | `woos-prd-review-gate` | local |
| Capability Contract | `product-capability` | imported |
| Feature Design | `woos-feature-design` | local |
| Design Review | `woos-design-review-gate` | local |
| TDD | `tdd-workflow` | imported |
| Implement | `coding-standards` | imported |
| Verify | `verification-loop` | imported |
| Code/Security Review | `woos-code-review-gate` | local |
| PR Readiness | `woos-pr-readiness` | local |

If a required skill is unavailable, status is `BLOCKED` and the workflow stops.

Local wrapper intent:

- `woos-prd-review-gate` wraps `planner` + `architect`
- `woos-feature-design` wraps `architect` (and `planner` for complex scope)
- `woos-design-review-gate` wraps `architect`
- `woos-code-review-gate` wraps `code-reviewer` (+ `security-reviewer` when needed)
- `woos-pr-readiness` wraps `verification-loop`

## Global Gate Status

- `NOT_RUN`: required skill was not invoked
- `BLOCKED`: required skill unavailable
- `REQUEST_CHANGES`: gate failed, revise and rerun same skill
- `PASS`: gate complete

Progression rule:

```text
NOT_RUN/BLOCKED/REQUEST_CHANGES -> PASS -> next gate
```

## Gate Definitions (skill + minimal contract)

### Gate 0 — Research
**Skill:** `search-first`  
**Minimal contract:**

1. Reuse options are searched before net-new design.
2. Chosen direction is recorded with a short rationale.

### Gate 1 — PRD Draft
**Skill:** `woos-prd-authoring` (local)  
**Minimal contract:**

1. PRD artifact exists at `docs/prd/<feature>.md` (or repo convention).
2. Core sections and testable AC are present.

### Gate 1R — PRD Review
**Skill:** `woos-prd-review-gate` (local)  
**Minimal contract:**

1. Executes independent PRD review using `planner` + `architect` via the local gate skill.
2. Returns `PASS` or `REQUEST_CHANGES` with concrete gaps.

### Gate 1.5 — Capability Contract
**Skill:** `product-capability`  
**Minimal contract:**

1. Produces implementation-facing capability contract.
2. Captures constraints/invariants/interfaces/open questions.

### Gate 2 — Feature Design
**Skill:** `woos-feature-design` (local)  
**Minimal contract:**

1. Design artifact exists at `docs/design/<feature>.md` (or repo convention).
2. Covers architecture, data, interfaces, risk, rollout/rollback.

### Gate 2R — Design Review
**Skill:** `woos-design-review-gate` (local)  
**Minimal contract:**

1. Executes independent design review using `architect` via local gate skill.
2. Returns `PASS` or `REQUEST_CHANGES`.

### Gate 3 — TDD
**Skill:** `tdd-workflow`  
**Minimal contract:**

1. RED observed before implementation for behavior changes.
2. GREEN observed after implementation.

### Gate 4 — Implement
**Skill:** `coding-standards`  
**Minimal contract:**

1. Changes are minimal, scoped, and convention-aligned.
2. No silent failures or unsafe shortcuts.

### Gate 5 — Verify
**Skill:** `verification-loop`  
**Minimal contract:**

1. Relevant lint/test/type/build checks executed.
2. Verification status reported explicitly.

### Gate 6 — Code/Security Review
**Skill:** `woos-code-review-gate` (local)  
**Minimal contract:**

1. Runs `code-reviewer`.
2. Runs `security-reviewer` when scope is security-sensitive.
3. Enforces implementation-vs-spec alignment (`spec_alignment_status`).
4. Returns `PASS` or `REQUEST_CHANGES`.

### Gate 7 — PR Readiness
**Skill:** `woos-pr-readiness` (local)  
**Minimal contract:**

1. Diff/status/review/verification readiness is checked.
2. Traceability matrix is provided (requirement -> test -> code).
3. Artifact sync status is `PASS` when deviations exist.
4. Conventional commit + PR test plan readiness confirmed.

## Stop Conditions

Stop and surface blocker when:

- Required skill was not invoked (`NOT_RUN`)
- Required skill unavailable (`BLOCKED`)
- Gate returns `REQUEST_CHANGES`
- Ambiguity blocks acceptance criteria definition
