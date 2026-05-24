---
name: woos-development-workflow
description: Skill-first gated workflow for near-unattended Hermes delivery. Every gate binds to one wrapper skill with a minimal contract and enforced sub-invocations.
version: 1.12.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [development, workflow, skill-first, tdd, review, prd, design]
---

# Woos Development Workflow

## Purpose

Use this workflow for non-trivial software work.  
Rule: every gate must invoke exactly one **gate wrapper skill**, then satisfy that wrapper's minimal contract.  
Wrapper-internal mandatory sub-invocations are allowed and required.

## Baseline-First Governance

1. Default all affected domains (UI/backend/database/infra) to mainstream, maintainable, evolvable baselines.
2. Any below-baseline or outlier decision requires ADR + explicit approval.
3. Freeze constraints only when user-provided or ADR-approved.
4. Design/code review gates must fail when deviation lacks ADR+approval evidence.

## Git Branch/Worktree Policy

Define git mode explicitly before implementation:

- `git-workflow` is required for branch strategy, commit/PR flow, and merge/rebase conventions.
- `dmux-workflows` is required only when running parallel coding lanes.

Minimal contract:

1. Invoke `git-workflow` before meaningful code changes.
2. Invoke `dmux-workflows` only for parallel execution.
3. If `dmux-workflows` is active, use worktree-per-worker with isolated branches.

Mandatory bootstrap:

1. Invoke `woos-run-orchestrator` first to initialize run state and produce `run_id`.
2. Review gates MUST NOT run without orchestrator-issued `run_id`.

## Execution Profiles (tiered activation)

Default profile is **Standard**.  
Use **Lite** for low-risk small changes.  
Use **Strict** for high-risk, ambiguous, or security-critical scope.

### Lite (small/low-risk)

```text
Run Orchestrator -> Git Workflow -> Handoff Intake -> Implement -> Verify -> Code/Security Review -> PR Readiness
```

Minimal use criteria:

- Limited scope and low coupling
- No architecture/API contract changes
- No high-risk security/compliance impact

### Standard (default)

```text
Run Orchestrator -> Git Workflow -> Handoff Intake -> Feature Design -> Design Review -> Implement -> Verify -> Code/Security Review -> PR Readiness -> Workflow Memory Update
```

Use when:

- Multi-file or cross-component change
- Design choices need review
- Normal feature delivery with moderate risk

### Strict (full hard-gate flow)

```text
Run Orchestrator -> Git Workflow -> Handoff Intake -> Capability Contract -> Feature Design -> [API Design Review] -> Design Review -> TDD -> Implement -> Verify -> [Browser QA] -> Executable Acceptance -> Deviation Control -> Code/Security Review -> PR Readiness -> Workflow Memory Update
```

Use when:

- Security-sensitive or compliance-sensitive scope
- High uncertainty/ambiguity
- Significant architecture/data model/API changes
- Release risk is high and full traceability is required

## Skill Whitelist

Only these skills are allowed in this workflow:

| Step | Skill | Source |
|---|---|---|
| Run Orchestrator | `woos-run-orchestrator` | local |
| Git Workflow | `git-workflow` | imported |
| Handoff Intake | _(reads product handoff)_ | from `woos-product-design-flow` |
| Parallel Orchestration (when needed) | `dmux-workflows` | imported |
| Capability Contract | `product-capability` | imported |
| Feature Design | `woos-feature-design` | local |
| API Design Review (if REST/GraphQL) | `api-design` | imported |
| Design Review | `woos-design-review-gate` | local |
| TDD | `tdd-workflow` | imported |
| Implement | `coding-standards` | imported |
| Verify | `verification-loop` | imported |
| Browser QA (if frontend) | `browser-qa` | imported |
| Executable Acceptance | `woos-executable-acceptance-gate` | local |
| Deviation Control | `woos-deviation-control-gate` | local |
| Review Context (cross-gate) | `woos-review-context` | local |
| Agent Decision (on reviewer conflict) | `woos-agent-decision` | local |
| Code/Security Review | `woos-code-review-gate` | local |
| PR Readiness | `woos-pr-readiness` | local |
| Workflow Memory Update | `woos-workflow-memory` | local |

If a required skill is unavailable, status is `BLOCKED` and the workflow stops.

Local wrapper intent:

- `woos-feature-design` wraps `architect` (and `product-planner` for complex scope)
- `woos-design-review-gate` wraps `architect`
- `woos-executable-acceptance-gate` wraps measurable acceptance checks
- `woos-deviation-control-gate` wraps spec drift blocking policy
- `woos-failure-state-machine` defines retry/degrade/escalate transitions
- `woos-systematic-debugging` activates during Gate 3/4/5 on repeated failures (cross-cutting protocol)
- `woos-run-orchestrator` defines queue/concurrency/timeout/retry controls
- `woos-human-handoff` defines escalation and recovery protocol
- `woos-workflow-memory` captures failure and rework patterns
- `woos-review-context` carries cumulative findings across review gates
- `woos-agent-decision` resolves reviewer conflicts deterministically
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

### Gate 0 — Handoff Intake

**Input:** `docs/handoff/<version>/<feature>.md` (produced by `woos-product-design-flow`)

**Minimal contract:**

1. Handoff file exists and contains: Mission, Requirements, AC, User Flows, Build Tasks, Verification Plan.
2. All AC are testable (already validated by product stage).
3. Record handoff version in run-manifest for traceability.

**If handoff does NOT exist:** Redirect to `woos-product-design-flow` first. Do not proceed without product handoff.

### Gate 1.5 — Capability Contract
**Skill:** `product-capability`  
**Minimal contract:**

1. Produces implementation-facing capability contract derived from the handoff.
2. Captures constraints/invariants/interfaces/open questions.

### Gate 2 — Feature Design
**Skill:** `woos-feature-design` (local)  
**Minimal contract:**

1. Design artifact exists at `docs/design/<feature>.md` (or repo convention).
2. Covers architecture, data, interfaces, risk, rollout/rollback.
3. If API endpoints are defined: API design reviewed against `api-design` patterns.
4. Baseline/deviation decision fields are complete; deviations include ADR + approval refs.
5. `unconfirmed_constraints_frozen` must be `false`.

### Gate 2.1 — API Design Review (conditional)
**Skill:** `api-design` (imported, optional)  
**When to invoke:**
- Feature includes new REST/GraphQL API endpoints
- Existing API is being modified
- Public or partner-facing API involved

**Minimal contract:**
1. Endpoints follow resource naming conventions (plural, kebab-case, no verbs)
2. HTTP methods and status codes are semantically correct
3. Pagination/filtering strategy defined (cursor vs offset)
4. Authentication and authorization strategy documented
5. Error response format is standard
6. Rate limiting policy defined (if applicable)

### Gate 2R — Design Review
**Skill:** `woos-design-review-gate` (local)  
**Minimal contract:**

1. Executes independent design review using `architect` via local gate skill.
2. Uses `woos-review-context` to load/update cumulative findings.
3. Returns `PASS` or `REQUEST_CHANGES`.
4. Escalates to `woos-human-handoff` when review loop threshold is exceeded.

### Gate 3 — TDD
**Skill:** `tdd-workflow`  
**Minimal contract:**

1. RED observed before implementation for behavior changes.
2. GREEN observed after implementation.
3. If RED-GREEN cycle stalls (2+ consecutive failed fix attempts), activate `woos-systematic-debugging` before further attempts.

### Gate 4 — Implement
**Skill:** `coding-standards`  
**Minimal contract:**

1. Changes are minimal, scoped, and convention-aligned.
2. No silent failures or unsafe shortcuts.
3. If implementation causes cascading failures, activate `woos-systematic-debugging`.

### Gate 5 — Verify
**Skill:** `verification-loop`  
**Minimal contract:**

1. Relevant lint/test/type/build checks executed.
2. Verification status reported explicitly.
3. If verification fails and fix is non-obvious (2+ attempts), activate `woos-systematic-debugging` before further retry.

### Gate 5.3 — Browser QA (conditional)
**Skill:** `browser-qa` (imported, optional)  
**When to invoke:**
- Feature includes frontend/UI changes
- UI interactions need verification
- Cross-browser or responsive testing required
- Pre-launch visual regression check

**Minimal contract:**
1. Smoke test: page loads, no critical console errors, network requests succeed
2. Interaction test: key user flows work (forms, navigation, state changes)
3. Visual regression: screenshots at 3 breakpoints (375px, 768px, 1440px)
4. Accessibility: WCAG AA violations checked, keyboard navigation verified
5. Core Web Vitals: LCP/CLS/INP within acceptable ranges
6. Report: screenshot evidence, issue log, verdict (ship/needs-fixes)

### Gate 5.5 — Executable Acceptance
**Skill:** `woos-executable-acceptance-gate` (local)  
**Minimal contract:**

1. Done criteria are mapped to executable checks (tests, schema checks, thresholds, policies).
2. Missing automation is explicitly tracked as a blocker.
3. Gate returns `REQUEST_CHANGES` when required checks are missing or failing.

### Gate 5.8 — Deviation Control
**Skill:** `woos-deviation-control-gate` (local)  
**Minimal contract:**

1. Implementation is compared against PRD/design/capability artifacts.
2. Unresolved deviations block progression.
3. Intentional deviations require updated artifacts and explicit rationale.

### Gate 6 — Code/Security Review
**Skill:** `woos-code-review-gate` (local)  
**Minimal contract:**

1. Runs `code-reviewer`.
2. Runs `security-reviewer` when scope is security-sensitive.
3. Uses `woos-review-context` to load/update cumulative findings.
4. Uses `woos-agent-decision` when reviewer verdicts conflict.
5. Enforces implementation-vs-spec alignment (`spec_alignment_status`).
6. Returns `PASS` or `REQUEST_CHANGES`.
7. Escalates to `woos-human-handoff` when review loop threshold is exceeded.
8. Rejects unapproved baseline deviations or frozen unconfirmed constraints.

### Gate 7 — PR Readiness
**Skill:** `woos-pr-readiness` (local)  
**Minimal contract:**

1. Diff/status/review/verification readiness is checked.
2. Traceability matrix is provided (requirement -> test -> code).
3. Artifact sync status is `PASS` when deviations exist.
4. Conventional commit + PR test plan readiness confirmed.

### Gate 8 — Workflow Memory Update
**Skill:** `woos-workflow-memory` (local)  
**Minimal contract:**

1. Capture failures, rework causes, and mitigation patterns from this run.
2. Persist reusable guidance for next run.
3. Record whether human handoff occurred and why.

## Stop Conditions

Stop and surface blocker when:

- Required skill was not invoked (`NOT_RUN`)
- Required skill unavailable (`BLOCKED`)
- Gate returns `REQUEST_CHANGES`
- Ambiguity blocks acceptance criteria definition
- Review loop threshold exceeded without convergence

## Runtime Control for Near-Unattended Execution

Use these control skills across all gates:

- `woos-run-orchestrator`: queue policy, concurrency limits, timeout and retry envelope
- `woos-failure-state-machine`: deterministic transition after failure (`retry` -> `degrade` -> `human_handoff`)
- `woos-human-handoff`: escalation trigger, handoff payload, resume conditions
- `woos-review-context`: cumulative findings and resolution tracking across review gates
- `woos-agent-decision`: conflict resolution when reviewer outputs disagree

Review context persistence file:

- `<workspace_root>/hep/review-context/<run_id>.yaml`
- For gated runs, `run_id` is mandatory; if missing, return `BLOCKED`.

Review gates MUST emit machine-readable `enforcement` output that lists required and actually-invoked skills with invocation evidence.

Run orchestration MUST persist and verify:

- `<workspace_root>/hep/runs/<run_id>/run-manifest.yaml`
- `runs/` and `review-context/` are created by orchestrator at run start when missing.
- Missing required sections is a `BLOCKED` condition.
