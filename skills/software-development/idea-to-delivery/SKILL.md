---
name: idea-to-delivery
description: End-to-end delivery flow from idea capture through PR. Bridges research agent (idea → PRD → design → handoff) and coding agent (implement → verify → PR). Supports Lite / Standard / Strict tiers. Includes DCR feedback loop, Constitution support, Handoff Readiness Gate, and Delta annotations.
version: 2.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [delivery, idea, prd, design, handoff, tdd, review, workflow, end-to-end, dcr, constitution, delta]
    related_skills:
      - idea-capture
      - build-handoff
      - woos-development-workflow
      - woos-prd-authoring
      - woos-feature-design
      - woos-pr-readiness
---

# Idea-to-Delivery

## Purpose

End-to-end flow from raw idea to merged PR, with a **bidirectional feedback loop** between research and coding agents.

Two agents collaborate through a file-based handoff:

- **Research agent** (product side): idea capture → research → PRD → design → handoff
- **Coding agent** (engineering side): implement → verify → PR
- **Feedback loop**: coding agent can issue Design Change Requests (DCR) back to research agent

This skill is the umbrella — it selects the execution tier, routes phases, and delegates to sub-skills.

## When to Use

Use when:

- User presents a new feature idea, product initiative, or behavior-changing request
- Work spans both product thinking and engineering implementation
- You need a structured flow from ideation to delivery

Skip when:

- Pure bugfix with clear scope → use `woos-development-workflow` Lite directly
- Typos, docs-only changes → no workflow needed
- Already have a PRD + design → jump to `woos-development-workflow` Standard/Strict

## Agent Boundary

| Agent | Owns | Does NOT do |
|-------|------|-------------|
| Research | Idea capture, research, PRD, design, handoff packaging, DCR assessment | Coding, testing, git, PRs |
| Coding | Implementation, testing, code review, PR, DCR authoring | Requirement definition, product decisions, architecture changes (unless via DCR) |

Deviations from the handoff spec must go back through the research agent via the DCR mechanism.

## Core Design Principles

| Dimension | Decision |
|-----------|----------|
| Agent boundary | research = idea→handoff; coding = implement→PR |
| Handoff mechanism | File-based (Markdown artifacts), not kanban |
| Execution modes | Lite / Standard / Strict, default Standard |
| Gate model | PASS / REQUEST_CHANGES (binary — no PASS_WITH_NOTES) |
| Review isolation | Fresh context dispatch, no self-review |
| Baseline governance | Default to mainstream; deviations need ADR + approval |
| Override phrase | `GREENLIGHT NEXT STAGE` — user can force-skip questions |
| Feedback loop | DCR: coding → research (bidirectional, not one-way) |
| Constitution | `.hep/constitution.md` project-level conventions; handoff references, only deviations written |
| Delta annotation | Build Tasks: `[ADDED]`/`[MODIFIED]`/`[REMOVED]` (from OpenSpec) |
| Spec versioning | Handoff header: `spec-version` + `based-on`, supports incremental evolution |

## Execution Tiers

Default: **Standard**.

### Lite — Quick Validation

For: small tools, bugfix with design questions, scope-clear small changes, low risk.

```text
Capture → PRD (merged with design) → Build Handoff (4-field) → Implement → Verify → PR
```

- Skips: research pass, independent review gates, Handoff Readiness Gate
- PRD + design merged into one document
- Coding agent self-reviews (no independent dispatch)
- Handoff only 4 fields: Mission + Build Tasks + AC + Verification Commands
- No DCR (handle small deviations inline)
- Constitution reference optional (skip if no project conventions exist)

### Standard — Default

For: normal features, cross-file changes, needs design review.

```text
Capture → Research → PRD → [PRD Review] → Design → [Design Review]
→ Handoff → [Handoff Readiness (self-check)] → Implement → Verify
→ [Code Review] → PR
```

- PRD Review: dispatch `product-planner` (fresh context)
- Design Review: dispatch `architect` (fresh context)
- Handoff Readiness: self-check checklist (no independent dispatch)
- Code Review: dispatch `code-reviewer` (fresh context)
- DCR: available for design issues found during implementation
- Constitution reference required (if `.hep/constitution.md` exists)
- Full handoff template (12 sections)

### Strict — Full Hard-Gate Flow

For: security-sensitive, compliance, high-risk architecture changes.

```text
Capture → Research → Requirement Contract → PRD → [PRD Review]
→ Capability Contract → Design → [API Design Review] → [Design Review]
→ Handoff → [Handoff Readiness (independent reviewer)]
→ TDD → Implement → Verify → [Browser QA] → [Executable Acceptance]
→ [Deviation Control] → [Code/Security Review] → PR → [Workflow Memory]
```

- All gates active, including `security-reviewer`
- Handoff Readiness: dispatch `architect` to independently review
- Requirement Contract enforced
- Deviation Control: implementation vs design
- Workflow Memory: failure pattern capture
- DCR: mandatory for any design deviation
- Constitution MUST exist and be referenced in handoff

## Tier Selection Guide

```text
Is it security/compliance sensitive?              → Strict
Is it a major architecture change?                → Strict
Is it a normal feature (multi-file, cross-component)? → Standard
Is scope clear, single-purpose, low risk?         → Lite
Is it a typo/docs fix?                            → No workflow needed
```

If unsure, start with Standard. User can override with `GREENLIGHT NEXT STAGE` to skip questions (NOT gates).

## Phase Definitions

### Phase 0 — Product Planning (conditional)

**When:** Input is a product initiative / roadmap (multiple features bundled).

**Skill:** `woos-product-planning-workflow`

Produces feature map + delivery phases. Then each feature enters this flow individually.

### Phase 1 — Capture & Interview

**Skill:** `idea-capture`

- Lite: quick idea note → `ideas/<slug>.md`
- Full: guided interview → `ideas/<slug>/00-idea-capture.md`
- **Constitution detection**: check if `.hep/constitution.md` exists
  - If NOT exists: offer to create one (extract from project context or interview)
  - If exists: note for handoff reference
- **User override:** `GREENLIGHT NEXT STAGE` skips remaining questions

### Phase 2 — Research Pass

**Skill:** `search-first` (default) or `deep-research` (Strict)

- Bounded exploration: what exists, gaps, what to avoid
- Output: `docs/research/<topic>.md`

**Lite: skip.**

### Phase 3 — PRD Draft

**Skill:** `woos-prd-authoring`

- Structured PRD with testable acceptance criteria
- Output: `docs/prd/<feature>.md`

### Phase 3R — PRD Review Gate

**Skill:** `woos-prd-review-gate`

- Dispatch `product-planner` in fresh context
- Strict: also dispatch `architect`
- Gate: PASS → Phase 4 / REQUEST_CHANGES → return to Phase 3
- Conflict resolution: `woos-agent-decision` with authority matrix

**Lite: skip.**

### Phase 4 — Feature Design

**Skill:** `woos-feature-design`

- Architecture, data model, API contracts, interfaces, security, test strategy
- Baseline compliance check; deviations need ADR + approval
- Output: `docs/design/<feature>.md`

### Phase 4R — Design Review Gate

**Skill:** `woos-design-review-gate`

- Dispatch `architect` in fresh context
- Gate: PASS → Phase 5 / REQUEST_CHANGES → return to Phase 4

**Lite: skip.**

### Phase 5 — Build Handoff

**Skill:** `build-handoff`

- Synthesize PRD + Design into single handoff file
- Must contain everything a fresh coding agent needs to work independently
- Spec versioning: handoff header includes `spec-version: 1.0` and `based-on: (previous version path or empty)`
- Constitution reference: `constitution-ref: .hep/constitution.md` (if exists); Technical Architecture section only documents deviations
- Delta annotation: Build Task titles use `[ADDED]`/`[MODIFIED]`/`[REMOVED]` prefixes. First delivery = all `[ADDED]`; iterations mark actual changes
- **Lite handoff**: only 4 required fields (Mission, Build Tasks, Acceptance Criteria, Verification Commands)
- **Standard/Strict handoff**: full 12-section template
- Output: `docs/handoff/<feature>.md`

### Phase 5R — Handoff Readiness Gate

**Trigger:** Build Handoff complete

**Flow:**
1. **Lite: skip entirely**
2. **Standard**: execute self-check checklist (no independent dispatch)
3. **Strict**: dispatch `architect` to independently review handoff quality

**Checks: completeness, consistency, executability**

**Standard Self-Check Checklist:**
- [ ] Mission clear, one sentence understandable
- [ ] AC all testable (Given/When/Then)
- [ ] Build Tasks each have clear Files/Steps/Verification
- [ ] Delta annotations correct (`[ADDED]`/`[MODIFIED]`/`[REMOVED]`)
- [ ] No blocking Open Questions (or flagged as user decision)
- [ ] Constitution reference correct (if `.hep/constitution.md` exists)
- [ ] Spec versioning header present (`spec-version`, `based-on`)
- [ ] Coding agent can work independently without accessing research agent's session

**Strict Independent Review** (dispatch `architect`):
- Completeness: all required fields present and filled
- Consistency: PRD/Design/Handoff aligned (no contradictions)
- Executability: coding agent can implement without additional context
- Constitution: deviations from constitution are documented with rationale

**Result:** PASS → handoff ready, deliver to coding agent / REQUEST_CHANGES → return to Phase 5

### Phase 6 — Implementation Planning (coding agent)

**Trigger:** Coding agent receives handoff file.

- Parse handoff → task breakdown → implementation plan
- Skill: project conventions (`coding-standards`, `writing-plans`)

### Phase 7 — Implement

**Skill:** `coding-standards` (Standard/Lite) or `tdd-workflow` (Strict)

- Standard/Strict: TDD (write tests first)
- Lite: direct implementation
- **If design issue discovered**: initiate DCR (Phase 11)

### Phase 8 — Verify

**Skill:** `verification-loop`

- Run all tests, verify acceptance criteria
- Strict: also run `woos-executable-acceptance-gate`

### Phase 9 — Code Review Gate

**Skill:** `woos-code-review-gate`

- Standard: dispatch `code-reviewer` (fresh context)
- Strict: dispatch `code-reviewer` + `security-reviewer`
- Spec alignment + deviation detection
- Gate: PASS → Phase 10 / REQUEST_CHANGES → return to Phase 7

**Lite: self-review (no independent dispatch).**

### Phase 10 — PR Readiness

**Skill:** `woos-pr-readiness`

- Diff review, traceability matrix, commit/PR discipline
- Output: PR ready to merge

### Phase 11 — Design Change Request (DCR)

**Trigger:** Coding agent discovers a design issue at any implementation phase.

**Applicable modes:** Standard + Strict (Lite handles small deviations inline).

**Flow:**
1. Coding agent writes `docs/feedback/<feature>-dcr.md`
2. DCR contains: issue description, impact scope, proposed resolution, priority
3. Research agent reads DCR and assesses
4. **Small change**: research agent updates handoff directly, notifies coding agent
5. **Large change**: research agent rolls back to Phase 3 (PRD) or Phase 4 (Design) for full re-review

**DCR File Template:**

```markdown
# Design Change Request: <Feature Name>

## Issue
Description of the design problem discovered during implementation.

## Impact
- Affected scope (which Tasks/Phases)
- Risk level (Low / Medium / High)

## Proposed Resolution
Suggested fix or approach change.

## Priority
- [ ] Blocking — cannot continue implementation
- [ ] Important — affects quality but not blocking
- [ ] Nice to have — improvement suggestion

## Research Agent Decision
(filled by research agent)
- [ ] Approved — update handoff
- [ ] Needs re-design — roll back to Phase 4
- [ ] Needs re-PRD — roll back to Phase 3
- [ ] Deferred — record but don't address this round
```

**DCR lifecycle:**
- Written by coding agent during Phase 7/8/9
- Assessed by research agent
- Resolution recorded in DCR file
- Handoff updated if approved
- Review context updated with DCR findings

## Constitution File

### What is Constitution

`.hep/constitution.md` is a project-level conventions file (inspired by Spec-Kit), containing:

- Tech stack choices (language, framework, database, deployment)
- Architecture conventions (monorepo vs multi-repo, API style, state management)
- Coding standards references
- Baseline decisions (what's default; deviations require ADR)
- Team conventions (naming, directory structure, testing requirements)

### When Created

- First time entering idea-to-delivery flow, if `.hep/constitution.md` doesn't exist
- Phase 1 (Capture) detects and offers to create
- Existing projects: extract from current codebase and conventions

### How Handoff References

```yaml
# handoff file header
spec-version: 1.0
constitution-ref: .hep/constitution.md
```

The Technical Architecture section in the handoff only documents **deviations** from constitution, not the full stack.

### Constitution Template

```markdown
# Project Constitution

## Tech Stack
- Language: [e.g., TypeScript]
- Runtime: [e.g., Node.js 20+]
- Framework: [e.g., Hono]
- Database: [e.g., Cloudflare D1]
- Deployment: [e.g., Cloudflare Workers]

## Architecture
- API style: [e.g., REST]
- Auth: [e.g., JWT + Cloudflare Access]
- State: [e.g., Stateless (Workers)]

## Coding Standards
- Linter: [e.g., ESLint + Prettier]
- Testing: [e.g., Vitest]
- Commit: [e.g., Conventional Commits]

## Baseline Decisions
- Default ecosystem: [e.g., Cloudflare — deviations need ADR]
- API versioning: [e.g., URL path (/v1/)]
- Error format: [e.g., { error: { code, message, details } }]
```

## Cross-Phase Skills

| Skill | Purpose |
|-------|---------|
| `woos-run-orchestrator` | Run manifest, queue policy, concurrency |
| `woos-review-context` | Cumulative findings across review gates |
| `woos-agent-decision` | Reviewer conflict resolution |
| `woos-human-handoff` | Escalation to human |
| `woos-workflow-memory` | Failure pattern capture |
| `woos-failure-state-machine` | Deterministic failure transitions |
| `woos-deviation-control-gate` | Implementation vs spec drift (Strict) |
| `woos-executable-acceptance-gate` | Executable done criteria (Strict) |

## Gate Status Model

```text
NOT_RUN / BLOCKED / REQUEST_CHANGES  →  PASS  →  next phase
```

Only two gate outcomes:

- **PASS** — proceed
- **REQUEST_CHANGES** — return to prior phase with concrete feedback

Notes and observations are recorded in findings but do not affect gate state.

## Review Isolation (Hard Rule)

Reviews MUST execute in fresh context:

- Use `delegate_task` or `kanban_create` to dispatch independent agent
- Reviewer MUST NOT inherit implementer's session
- `invocation_evidence` MUST include `dispatch_mode: "fresh_context"`

Self-review in the same session is invalid.

## Conflict Resolution (Authority Matrix)

When reviewers disagree:

| Domain | Authority |
|--------|-----------|
| Security issues | `security-reviewer` |
| Architecture | `architect` |
| Product/planning | `product-planner` |
| Code quality | `code-reviewer` |
| Cross-domain | Lowest-risk path; evidence over opinion |

Apply via `woos-agent-decision`. Full matrix in `references/review-authority-matrix.md`.

## Override Mechanism

User may say `GREENLIGHT NEXT STAGE` at any point to force progression past unresolved questions.

- Records the override in the run manifest
- Does not skip review gates — only skips interview questions and optional exploration
- Override does not waive gate PASS requirements

## Escalation

- Review rounds: max 2 per gate
- Reconciliation attempts: max 1 per round
- Exceeded → BLOCKED → escalate to human via `woos-human-handoff`

## File Layout

```text
<project-root>/
├── docs/
│   ├── prd/<feature>.md
│   ├── design/<feature>.md
│   ├── research/<topic>.md
│   ├── handoff/<feature>.md
│   ├── feedback/<feature>-dcr.md       # Design Change Requests
│   ├── adr/ADR-001-*.md
│   └── product/<initiative>-plan.md    # Product planning output (Phase 0)
├── .hep/
│   ├── constitution.md                 # Project-level conventions
│   ├── runs/<run_id>/run-manifest.yaml
│   └── review-context/<run_id>.yaml
└── ideas/
    ├── index.md
    └── <idea-slug>.md
```

## Skill Dependency Map

```text
idea-to-delivery (this skill)
├── Phase 0:  woos-product-planning-workflow
├── Phase 1:  idea-capture
├── Phase 2:  search-first / deep-research
├── Phase 3:  woos-prd-authoring
├── Phase 3R: woos-prd-review-gate
├── Phase 4:  woos-feature-design
├── Phase 4R: woos-design-review-gate
├── Phase 5:  build-handoff
├── Phase 5R: Handoff Readiness (built-in self-check / architect review)
├── Phase 6:  coding-standards / writing-plans
├── Phase 7:  coding-standards / tdd-workflow
├── Phase 8:  verification-loop
├── Phase 9:  woos-code-review-gate
├── Phase 10: woos-pr-readiness
├── Phase 11: DCR feedback loop (built-in)
└── Cross-cutting:
    ├── woos-run-orchestrator
    ├── woos-review-context
    ├── woos-agent-decision
    ├── woos-human-handoff
    ├── woos-workflow-memory
    ├── woos-failure-state-machine
    ├── woos-deviation-control-gate
    └── woos-executable-acceptance-gate
```

## Key Design Decisions

### D1: Binary gate (PASS / REQUEST_CHANGES)

Original woos design had `PASS_WITH_NOTES`. Unified to binary:
- **PASS** = can proceed
- **REQUEST_CHANGES** = must change before proceeding

Notes go in findings but don't affect gate state. Reduces agent decision complexity.

### D2: Review must be fresh context

Same LLM session reviewing itself = no real independent review. Fresh context dispatch is the only way to ensure review has actual value.

### D3: File-based handoff (not kanban)

- Files are human-readable, version-controllable, diffable
- Kanban is for task scheduling, not for complex PRD/Design content
- File handoff allows cross-system (different profiles, different agents) seamless transfer

### D4: Lite skips review gates

Lite = "low-risk small changes". Independent dispatch review cost > self-review risk. Use Standard if quality matters more.

### D5: Research agent does not code

Separation of concerns. Research agent value = product thinking + requirement quality. Coding + product thinking in same agent leads to skipping requirement clarification.

### D6: When to use product-planning-workflow

When input is product/plan/roadmap level (multiple features mixed), first do feature map + delivery phase decomposition, then enter idea-to-delivery per feature.

### D7: Why DCR (feedback loop)

Original was one-way: research → handoff → coding. But coding often discovers:
- Design assumptions don't hold (library behavior differs)
- Missing requirements (edge cases)
- Technical constraints (performance/security/compatibility)

Without DCR, coding agent either silently drifts from spec or blocks on human. DCR enables bidirectional communication: small fixes are immediate, large changes roll back orderly.

### D8: Why Constitution

Every handoff repeating Technical Stack is redundant and inconsistent. Constitution centralizes project conventions:
- Created once upfront
- Subsequent handoffs only document deviations
- Inspired by: OpenSpec's project.md / Spec-Kit's constitution

### D9: Why Handoff Readiness Gate

Handoff is coding agent's **only input**. Defective handoff (missing fields, untestable AC, PRD-Design contradictions) causes repeated implementation errors. Phase 5R quality-checks before handoff — cost is far lower than post-implementation rework.

### D10: Why Delta annotations

Most features aren't greenfield — they iterate on existing code. Without delta markers, coding agent can't distinguish new code from modifications. OpenSpec's ADDED/MODIFIED/REMOVED is simple and effective.

### D11: Why Lite has streamlined handoff

Lite targets bugfix, small tools, low-risk scenarios. 12-section handoff for Lite means process overhead exceeds task complexity. Streamlined to 4 fields (Mission + Tasks + AC + Verification) keeps it lightweight without losing core information.
