---
name: feature-design
description: Stage 2 orchestration skill. Takes a version from the product roadmap and produces PRD + technical design, packaged as a Handoff file for the coding agent. Supports Standard (gated) and Lite (4-field) modes. Includes Review Gate rules, Handoff Readiness self-check, Delta annotations, and DCR Protocol.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [stage-2, feature-design, orchestration, prd, design, handoff, review-gate, dcr, delta]
    related_skills:
      - woos-requirement-contract
      - woos-prd-authoring
      - woos-prd-review-gate
      - woos-feature-design
      - woos-design-review-gate
      - woos-build-handoff
      - woos-review-context
      - woos-agent-decision
      - woos-human-handoff
---

# Feature Design (Stage 2 Orchestration)

## Purpose

Orchestrate Stage 2 of the woos-idea-to-delivery pipeline: take a version from the product roadmap, produce a PRD + technical design, and package everything into a Handoff file that a fresh coding agent can work from independently.

This skill is the **orchestrator** — it calls sub-skills in sequence, enforces review gates, and ensures the Handoff output is complete.

## Agent

**research** — this skill runs entirely within the research agent's scope.

## When to Use

Use when:

- User says "开始做 V1" / "设计这个功能" / "start working on version N"
- A product roadmap exists at `docs/product/<project>-roadmap.md`
- Need to produce a Handoff for the coding agent

Skip when:

- No roadmap exists → run Stage 1 (`woos-product-discovery`) first
- Already have a Handoff file → go straight to Stage 3 (`engineering-workflow`)
- Pure bugfix with clear scope → use `engineering-workflow` Lite directly

## Input Artifacts

| Artifact | Required | Location |
|----------|----------|----------|
| Product Roadmap | Yes | `docs/product/<project>-roadmap.md` |
| Constitution | If exists | `.hep/constitution.md` |
| Prior Handoff | For iterations | `docs/handoff/<feature>-v(N-1).md` |
| Run Manifest | If exists | `.hep/runs/<run_id>/run-manifest.yaml` |

## Modes

### Standard — Default

Full gated flow: Requirement Contract → PRD → PRD Review → Design → Design Review → Handoff → Readiness Self-Check → Delta Annotation.

For: normal features, multi-file changes, anything needing design review.

### Lite — Quick Path

4-field Handoff only: Mission / Build Tasks / AC / Verification. No review gates.

For: scope-clear small changes, bugfixes with design questions, low-risk work.

## Mode Selection

```text
Scope clear, single-purpose, low risk?       → Lite
Normal feature, multi-file, needs design?    → Standard
```

If unsure, default to Standard.

## Standard Flow

### Step 2.1 — Read Version Scope

**Action**: Read `docs/product/<project>-roadmap.md`, identify target version (V1/V2/...).

- Extract: core features, non-goals, success metrics, constraints
- Confirm version scope with user if ambiguous
- Load `.hep/constitution.md` if exists
- Load prior handoff (`docs/handoff/<feature>-v(N-1).md`) if this is an iteration
- Determine feature slug from version name

**Output**: version scope confirmed, feature slug defined.

### Step 2.2 — Requirement Contract

**Skill**: `woos-requirement-contract`

Build structured requirement contract:
1. `objective`: user/business outcome
2. `constraints`: technical and policy constraints (from roadmap + constitution)
3. `acceptance_criteria`: testable, machine-checkable
4. `non_goals`: explicitly out of scope (from roadmap Non-goals)
5. `risks_assumptions`: known risks and assumptions
6. `priority`: must/should/could

**Gate**: If any required field missing or AC not measurable → `REQUEST_CHANGES` → fix before proceeding.

**Output**: `status: PASS`, `ready_for_prd: true`.

### Step 2.3 — PRD Authoring

**Skill**: `woos-prd-authoring`

Write a complete PRD:
- Follow the 14-section PRD structure
- Ensure all acceptance criteria use Given/When/Then format
- Reference roadmap vision and user personas from Stage 1
- Include edge cases, security notes, rollout considerations

**Output**: `docs/prd/<feature>.md`

### Step 2.4 — PRD Review Gate

**Skill**: `woos-prd-review-gate`

**Reviewers** (must be fresh context, no self-review):
- `product-planner`: structure, completeness, testability
- `architect`: feasibility, boundaries, non-functional risk

**Protocol**:
1. Load prior findings via `woos-review-context`
2. Dispatch each reviewer in fresh context (via `delegate_task`)
3. If reviewers disagree → `woos-agent-decision` resolves by authority matrix
4. Update `woos-review-context` with resolved/carry-forward findings
5. Persist to `.hep/review-context/<run_id>.yaml`

**Escalation**:
- Max 2 review rounds per gate
- Max 1 reconciliation attempt per round
- 3 rounds total without convergence → `woos-human-handoff` escalates to human

**Gate**: PASS → Step 2.5 / REQUEST_CHANGES → return to Step 2.3

### Step 2.5 — Feature Technical Design

**Skill**: `woos-feature-design`

Produce implementation-ready technical design:
- Architecture overview (only deviations from constitution)
- Interface / API contracts
- Data model implications
- Security considerations
- Test strategy
- Rollout / rollback plan
- Baseline compliance; deviations need ADR at `docs/adr/ADR-*.md`

**Output**: `docs/design/<feature>.md`

**Hard rules**:
- Constitution deviation without ADR + `approval_ref` → `REQUEST_CHANGES`
- Unconfirmed constraints frozen → `REQUEST_CHANGES`

### Step 2.6 — Design Review Gate

**Skill**: `woos-design-review-gate`

**Reviewer** (must be fresh context):
- `architect`: design quality, baseline compliance, deviation review

**Protocol**: same as Step 2.4 (load review context, fresh dispatch, conflict resolution).

**Escalation**: same limits as PRD Review (2 rounds, 1 reconciliation, then human).

**Gate**: PASS → Step 2.7 / REQUEST_CHANGES → return to Step 2.5

### Step 2.7 — Handoff Packaging

**Skill**: `woos-build-handoff`

Synthesize PRD + Design into a single self-contained Handoff file.

**Standard Handoff** contains:
1. Spec Versioning (YAML frontmatter: `spec-version`, `based-on`, `constitution-ref`)
2. Mission Statement
3. Context (from Stage 1 roadmap)
4. Requirements (AC, non-goals)
5. Architecture (only deviations from constitution)
6. Data Model (if applicable)
7. API Contracts (if applicable)
8. Build Tasks (with Delta annotations: `[ADDED]`/`[MODIFIED]`/`[REMOVED]`)
9. Verification Plan
10. Security Considerations
11. Constitution Reference
12. DCR Protocol section

**Output**: `docs/handoff/<feature>-vN.md`

**Delta annotation rules**:
- First full delivery: all tasks `[ADDED]`
- Iteration: mark each task by actual change type
- One prefix per task, no mixing

### Step 2.8 — Handoff Readiness Self-Check

**Action**: Built-in checklist verification (no independent dispatch for Standard).

Verify:
1. [ ] Mission clear, one sentence understandable
2. [ ] AC all testable (Given/When/Then)
3. [ ] Build Tasks each have clear Files/Steps/Verification
4. [ ] Delta annotations correct
5. [ ] No blocking Open Questions (or flagged as user decision)
6. [ ] Constitution reference correct (if exists)
7. [ ] Spec versioning header present
8. [ ] Coding agent can work independently without research agent's session

**Gate**: All pass → Handoff ready / Any fail → return to Step 2.7

### Step 2.9 — Delta Annotation Final Pass

**Action**: Ensure all Build Tasks have correct Delta prefix.

- Cross-reference with prior handoff (if iteration) to verify change type accuracy
- Ensure no task is missing `[ADDED]`/`[MODIFIED]`/`[REMOVED]` prefix
- For greenfield: confirm all tasks are `[ADDED]`

## Lite Flow

### Step 2L.1 — Quick Mission

**Action**: One-sentence Mission statement capturing what to build.

### Step 2L.2 — Build Tasks

**Action**: List of concrete tasks with steps and verification.

### Step 2L.3 — Acceptance Criteria

**Action**: Testable AC using Given/When/Then.

### Step 2L.4 — Package Lite Handoff

**Skill**: `woos-build-handoff` (Lite mode)

4 fields only:
1. Mission
2. Build Tasks (with Delta annotations)
3. Acceptance Criteria
4. Verification Commands

**Output**: `docs/handoff/<feature>-vN.md`

**Lite skips**: Requirement Contract, PRD Authoring, all Review Gates, Design, Design Review, Readiness Self-Check.

## Review Gate Rules (Cross-Cutting)

| Rule | Enforcement |
|------|-------------|
| Fresh context required | `dispatch_mode: "fresh_context"` via `delegate_task`; same-session self-review is invalid |
| Review context accumulation | `woos-review-context` loads before and saves after every gate |
| Conflict resolution | `woos-agent-decision` applies authority matrix when reviewers disagree |
| Escalation ceiling | 3 rounds total without convergence → `woos-human-handoff` |
| Constitution deviation | Must have ADR at `docs/adr/ADR-*.md` with explicit `approval_ref` |
| Gate binary | PASS / REQUEST_CHANGES only (no PASS_WITH_NOTES) |

## DCR Protocol (included in Handoff)

The Handoff file MUST include a DCR Protocol section so the coding agent knows how to feed design issues back:

```markdown
## DCR Protocol

When the coding agent discovers a design issue during implementation:

1. Write `docs/feedback/<feature>-dcr.md` with:
   - Issue: description of the design problem
   - Impact: affected scope (which Tasks/Phases), risk level
   - Proposed Resolution: suggested fix
   - Priority: Blocking / Important / Nice-to-have

2. Research agent reads and assesses:
   - Small change → update Handoff directly, notify coding agent
   - Large change → roll back to Step 2.3 (PRD) or Step 2.5 (Design) for re-review

3. Resolution recorded in DCR file; review context updated.
```

## Conflict Resolution Authority Matrix

When reviewers disagree, resolve via `woos-agent-decision`:

| Domain | Authority |
|--------|-----------|
| Security issues | `security-reviewer` |
| Architecture | `architect` |
| Product / planning | `product-planner` |
| Cross-domain | Lowest-risk path; evidence over opinion |

## User Override

User may say `GREENLIGHT NEXT STAGE` to skip interview questions and optional exploration.
- Recorded in run manifest
- Does NOT skip review gates — only skips confirmatory questions
- Override does not waive gate PASS requirements

## File Layout

```text
<project-root>/
├── .hep/
│   ├── constitution.md
│   ├── runs/<run_id>/run-manifest.yaml
│   └── review-context/<run_id>.yaml
├── docs/
│   ├── product/<project>-roadmap.md          # Stage 1 output (input here)
│   ├── prd/<feature>.md                      # Step 2.3 output
│   ├── design/<feature>.md                   # Step 2.5 output
│   ├── handoff/<feature>-vN.md              # Step 2.7 output (final deliverable)
│   ├── feedback/<feature>-dcr.md            # DCR feedback (from Stage 3)
│   └── adr/ADR-*.md                         # Architecture Decision Records
```

## Output

The final output of this skill is the Handoff file at `docs/handoff/<feature>-vN.md`.

This file is the **contract** between research agent and coding agent. It must be self-contained — a fresh coding agent with no prior context can implement from it.

## Skill Dependency Map

```text
feature-design (this skill)
├── Step 2.2: woos-requirement-contract
├── Step 2.3: woos-prd-authoring
├── Step 2.4: woos-prd-review-gate
├── Step 2.5: woos-feature-design
├── Step 2.6: woos-design-review-gate
├── Step 2.7: woos-build-handoff
└── Cross-cutting:
    ├── woos-review-context (accumulates findings across gates)
    ├── woos-agent-decision (resolves reviewer conflicts)
    └── woos-human-handoff (escalation to human)
```
