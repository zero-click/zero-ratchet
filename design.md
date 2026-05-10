# Hermes Coding Workflow Design

## Overview

This profile uses a **skill-first gated workflow** for software delivery.  
Each workflow node must invoke exactly one named skill (local or imported), satisfy a minimal contract, and emit an explicit gate status.

Core objective:

- maximize reuse of imported skills
- keep local skills as thin wrappers only where no single ready-made skill exists
- enforce deterministic progression with hard stop conditions

Design emphasis:

- unattended delivery is the vision, enabled by role-specialized agents and strict gates
- design principles are first-class: role separation, traceability, deterministic progression, and explicit stop conditions

## Workflow Topology

```text
Research
  -> PRD Draft
  -> PRD Review
  -> Capability Contract
  -> Feature Design
  -> Design Review
  -> TDD
  -> Implement
  -> Verify
  -> Code/Security Review
  -> PR Readiness
```

Git mode policy:

- Always run `git-workflow` before meaningful code changes.
- Run `dmux-workflows` only for parallel lanes; when active, use worktree-per-worker.

## Gate Status Model

All gates use the same status model:

- `NOT_RUN`: required skill/agent was not invoked
- `BLOCKED`: required skill/agent unavailable
- `REQUEST_CHANGES`: gate failed, revise and rerun
- `PASS`: gate satisfied

Progression rule:

```text
NOT_RUN/BLOCKED/REQUEST_CHANGES -> PASS -> next gate
```

## Skill Mapping (Node -> Skill)

| Node | Skill | Source | Contract (minimal) |
|---|---|---|---|
| Git Workflow | `git-workflow` | imported | Define branch/commit/PR/merge-rebase mode before coding |
| Research | `search-first` | imported | Search reusable solutions before net-new work |
| Parallel Orchestration (when needed) | `dmux-workflows` | imported | Orchestrate parallel lanes with worktree isolation |
| PRD Draft | `woos-prd-authoring` | local | Produce PRD artifact with testable AC |
| PRD Review | `woos-prd-review-gate` | local | Invoke planner+architect and return gate status |
| Capability Contract | `product-capability` | imported | Convert PRD intent into implementation contract |
| Feature Design | `woos-feature-design` | local | Produce technical design artifact |
| Design Review | `woos-design-review-gate` | local | Invoke architect and return gate status |
| TDD | `tdd-workflow` | imported | RED -> GREEN discipline for behavior changes |
| Implement | `coding-standards` | imported | Enforce implementation quality baseline |
| Verify | `verification-loop` | imported | Run verification phases and report outcomes |
| Code/Security Review | `woos-code-review-gate` | local | Invoke code/security reviewers and gate |
| PR Readiness | `woos-pr-readiness` | local | Final PR readiness with verification visibility |

## Imported Modules Used

### Imported Skills (directly invoked)

- `search-first`
- `git-workflow`
- `dmux-workflows`
- `product-capability`
- `tdd-workflow`
- `coding-standards`
- `verification-loop`

### Agent-Adapter Skills (invoked via local gate skills)

- `planner` (PRD review support)
- `architect` (PRD/design review and design ownership)
- `code-reviewer` (mandatory code review)
- `security-reviewer` (required for security-sensitive scope)

## Local Skill Wrappers (Design Rationale)

Local wrappers exist only to provide hard-gate orchestration around imported capabilities:

- `woos-prd-review-gate`
- `woos-feature-design`
- `woos-design-review-gate`
- `woos-code-review-gate`
- `woos-pr-readiness`

Wrapper principles:

1. hard required invocation of named skills
2. no fallback to generic/self review
3. normalized gate status output
4. explicit blocking behavior when dependencies are missing

## Enforcement Rules

1. A gate is invalid if required skill/agent was not invoked.
2. Local wrappers must remain thin and contract-centric.
3. Any gate returning `REQUEST_CHANGES` must rerun the same gate skill after revisions.
4. No implementation starts before PRD draft/review and capability contract gates pass.
5. No PR handoff before verify + code/security review + PR readiness gates pass.

## Artifact Conventions

- PRD: `docs/prd/<feature>.md` (or project convention)
- Design: `docs/design/<feature>.md` (or project convention)
- Capability contract: repo product context artifact as defined by `product-capability`

## Future Extension Points

- Add a dedicated local `woos-research-gate` wrapper if stricter evidence output is needed on top of `search-first`.
- Add telemetry fields for each gate status transition to support workflow auditing.
- Add profile-specific risk matrix to auto-trigger `security-reviewer` scopes.
