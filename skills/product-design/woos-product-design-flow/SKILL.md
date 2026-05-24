---
name: woos-product-design-flow
description: "Stage 2 orchestrator: take a version from the product roadmap and produce PRD + UI direction + build handoff. Dispatches sub-agents per step with domain knowledge."
version: 4.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, design, prd, handoff, review-gate, ui, orchestrator]
    stage: 2
    flow: woos-idea-to-delivery
---

# Product Design Flow (Orchestrator)

> **🚨 CRITICAL: Read "Enforcement Rules" (E1–E7) before executing ANY step.**
> Every step MUST produce its declared output file. Every output MUST pass structural validation.
> Every sub-agent dispatch MUST inject full persona + knowledge + template file contents (E7).
> Skipping steps, merging outputs, or passing reviews without checking all criteria = WORKFLOW VIOLATION.

## Purpose

Transform one version from the product roadmap into a build-ready product handoff. This is **Stage 2** of the woos-idea-to-delivery flow. Run once per version.

Focus: define WHAT to build and WHY. Technical architecture (HOW) is engineering's job.

## Role

This file defines an **orchestrator** — a thin state machine that:
1. Tracks which step we're on (via `run-manifest.yaml`)
2. Dispatches sub-agents with the right persona + knowledge
3. **Validates outputs before advancing** (structural check)
4. Collects outputs, decides next step
5. Handles review fix loops

---

## ⛔ Enforcement Rules (NON-NEGOTIABLE)

These rules prevent the orchestrator from cutting corners. Violating any of them makes the entire flow invalid.

### E1: No Step Merging

Each step produces its own output file. You MUST NOT combine steps (e.g., writing requirements + PRD in one pass). Each step is a separate sub-agent dispatch with a separate output.

**Why:** Merging steps skips the quality ratchet. Each step builds on the previous step's validated output.

### E2: Output Validation Gate

After EVERY step, before advancing to the next, the orchestrator MUST verify:

```
1. Output file EXISTS at the declared path
2. Output file contains ALL required sections (structural check below)
3. If validation fails → re-dispatch the step, do NOT proceed
```

### E3: Template Compliance Check

Steps that declare a `Template` field MUST produce output matching that template's section structure. Check by verifying these H2 headings exist:

| Step | Required H2 Sections |
|------|---------------------|
| Step 2 (Requirements) | `## Problem Statement`, `## Goals`, `## User Stories`, `## Non-Goals`, `## Constraints`, `## Risks & Unknowns` |
| Step 4 (PRD) | `## Background`, `## User Personas`, `## Functional Requirements`, `## Non-Functional Requirements`, `## User Flows`, `## Edge Cases`, `## Non-Goals`, `## Success Metrics` |
| Step 9 (Readiness) | `## Checklist`, `## Verdict` |

If ANY required section is missing → the step is NOT done. Re-dispatch with: "Missing sections: [list]. Add them."

### E4: Review Prompt Must Include Full Checklist

When dispatching a review sub-agent, the orchestrator MUST include the COMPLETE checklist table in the prompt. Do NOT summarize or abbreviate it. The reviewer must check ALL criteria, not just "look for issues."

**Review dispatch template:**
```
You are reviewing: [file path]
Check EVERY row in this checklist. For EACH row, state ✅ or ❌ with a specific finding.
Do NOT skip rows. Do NOT give blanket passes.

[paste full checklist table here]

If you find ❌ on any row, the result is REQUEST_CHANGES.
```

### E5: No Silent Step Skipping

If a step fails (file not found, sub-agent error, etc.):
- **FIX the problem** (correct file path, re-dispatch, etc.)
- Do NOT skip to next step
- Do NOT mark as "skipped" unless the step is explicitly optional AND user confirms skip

The only legitimately skippable steps are:
- Step 6 (UI Brief) — only if user confirms "no UI"
- Step 10 (Integration) — only if single feature

### E6: Review Cannot Self-Validate

The same agent that authored a document MUST NOT review it. Reviews always use a fresh sub-agent dispatch with independent context.

### E7: Reference Injection Is Mandatory

Before dispatching ANY sub-agent, the orchestrator MUST:

1. **Read** the file declared in the step's `Persona` field → inject full content as the sub-agent's identity
2. **Read** the file(s) declared in the step's `Knowledge` field → inject full content as domain context
3. **Read** the file declared in the step's `Template` field → inject full content so the sub-agent can follow it exactly

**Do NOT:**
- Summarize or paraphrase reference files — inject them verbatim
- Say "you are a PM" without the persona file content — that's a hollow role
- Describe the template in your own words — the sub-agent needs the actual template to fill

**Why:** Reference files contain principles, thinking frameworks, and structural requirements that cannot be guessed. Without injection, sub-agents produce generic output that ignores the domain knowledge this workflow is built on.

**Dispatch prompt structure:**
```
## Your Identity
[full content of persona .toml file]

## Domain Knowledge
[full content of knowledge/framework .md file(s)]

## Template to Follow
[full content of template .md file]

## Task
[step-specific instructions]

## Input
[file path(s) to read]

## Output
[expected output file path]
```

---

## Project Root Requirement

All file paths (`docs/`) are relative to a **project root directory** which MUST be a git repository.

## When to Use

- User says "start V1" / "design this feature" / "ready to build X"
- Product roadmap exists and a version has been selected

## Prerequisites

- `docs/product/<project>-roadmap.md` exists (from Stage 1)
- **🚦 Human Approval Gate has passed** — user has reviewed full roadmap + architecture and explicitly said "start PRD" or equivalent. If you're invoking this skill and the user hasn't approved yet, STOP and go back to present the files.

## Modes

| Mode | When | Steps | Reviews |
|------|------|-------|---------|
| **Lite** | Small scope, obvious, 1-2 days work | Mission → Tasks → AC → Handoff | None |
| **Standard** | Single feature, moderate complexity | Requirements → PRD → PRD Review → Handoff | 1 (PRD Review) |
| **Strict** | Multi-feature version, high uncertainty, UX-heavy | Full pipeline: Priority → PRD → Review → UI → Review → Analyze → Handoff → Integration | All gates |

**How to choose:**
- Is it a one-liner change or tiny feature? → **Lite**
- Is it a single feature with clear scope? → **Standard**
- Is it a full version release with multiple features? → **Strict**

---

## Steps — Strict Mode

The orchestrator runs **per feature** in a loop:

```
Step 1: Select Version → extract feature list
  → For each feature:
      Steps 2–9 (Requirements → Readiness)
  → After ALL features pass Step 9:
      Step 10: Version Integration Gate
```

### Step 1: Select Version Scope

| | |
|---|---|
| **Sub-agent** | ❌ (orchestrator does this directly) |
| **Input** | `docs/product/<project>-roadmap.md` |
| **Output** | _(confirmed version name — stored in run-manifest)_ |

Read roadmap, extract target version. Confirm with user:
- Feature list and boundaries
- Non-goals
- Success metrics

---

### Step 2: Requirement Contract

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/prd.md` |
| **Template** | `templates/requirements-template.md` |
| **Input** | `docs/product/<project>-roadmap.md` § target version |
| **Output** | `docs/prd/<version>/<feature>-requirements.md` |

Produce structured requirements following the template. Mark uncertain items with `[NEEDS CLARIFICATION: ...]`.
- Goals and constraints
- Acceptance criteria (machine-checkable where possible)
- Non-goals
- Risk assumptions and unknowns

**⚠️ This step MUST produce a separate file.** Do NOT fold requirements into the PRD. The requirements file is the input to Step 3 (Priority Ranking) which appends to it.

---

### Step 3: Priority Ranking

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | _(persona sufficient — ranking is judgment, not methodology)_ |
| **Input** | `docs/prd/<version>/<feature>-requirements.md` |
| **Output** | `docs/prd/<version>/<feature>-requirements.md` → appends `## Priority Ranking` |

Rank requirements by priority using one framework:

| Framework | When | How |
|-----------|------|-----|
| MoSCoW | Small scope, clear stakeholders | Must / Should / Could / Won't |
| RICE | Data-available, competing features | Reach × Impact × Confidence ÷ Effort |
| Kano | UX-heavy, user delight matters | Must-have / Performance / Delighter |
| Story Mapping | Complex flows | Backbone → Walking Skeleton → Nice-to-have |

**Must produce:**
1. Ranked list with priority tier (P0 must-ship, P1 should-ship, P2 nice-to-have)
2. Trade-off rationale for P1/P2 items
3. Cut-line: what's IN vs DEFERRED

---

### Step 4: PRD Authoring

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/prd.md` + `references/bmad/templates/prd-template.md` |
| **Template** | `templates/prd-template.md` |
| **Input** | `docs/prd/<version>/<feature>-requirements.md` (including Priority Ranking) |
| **Output** | `docs/prd/<version>/<feature>.md` |

Write full PRD following the template. Mark uncertain items with `[NEEDS CLARIFICATION: ...]`.
P0 requirements get full detail, P2 gets brief mention:
- User stories with acceptance criteria
- Functional and non-functional requirements
- Edge cases and error handling
- User flows (text-based)

**⚠️ Template is mandatory, not advisory.** After authoring, the orchestrator runs E3 structural check. If ANY template section is missing, this step is re-dispatched until all sections are present.

---

### Step 5: PRD Review Gate

| | |
|---|---|
| **Sub-agent** | ✅ (independent reviewer) |
| **Persona** | `references/bmad/personas/prd-validator.toml` |
| **Knowledge** | `references/bmad/frameworks/validate-prd.md` + `references/bmad/templates/prd-validation-checklist.md` |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/prd/<version>/<feature>-requirements.md` + `docs/product/<project>-architecture.md` |
| **Output** | `docs/reviews/<version>/<feature>-prd-review-rN.md` |

**⚠️ PRD Review has TWO phases (both mandatory):**

**Phase A — Structural Completeness (E3 enforcement):**

Before content review, verify ALL required sections exist per template:
- `## Background` ✅/❌
- `## User Personas` ✅/❌
- `## Functional Requirements` (with `**User value:**` per FR) ✅/❌
- `## Non-Functional Requirements` ✅/❌
- `## User Flows` (at least 1 flow diagram) ✅/❌
- `## Edge Cases` (table format, ≥ 4 cases) ✅/❌
- `## Non-Goals` ✅/❌
- `## Success Metrics` (≥ 2 measurable metrics) ✅/❌

If ANY section is missing → **immediate REQUEST_CHANGES** without proceeding to Phase B.

**Phase B — Content Quality Checklist:**

| # | Criterion | Fix Hint |
|---|-----------|----------|
| P1 | Value-traced | Add "User value: …" line linking each requirement to a user outcome |
| P2 | AC testable | Rewrite as "Given X, When Y, Then Z" or add measurable threshold |
| P3 | Non-goals effective | Make specific enough to reject a concrete feature request |
| P4 | Edge cases covered | Add "What if…" for: empty state, error, timeout, concurrent access |
| P5 | Real user behavior | Replace developer-centric language with user-observable actions |
| P6 | No internal contradictions | Identify conflicts within this PRD; resolve or move to non-goals |
| P7 | Architecture alignment | Cross-check constants, state definitions, and API routes against `docs/product/<project>-architecture.md`. Flag any divergence. |

**Review findings format:**
```markdown
# PRD Review — Round N

| # | Criterion | Status | Finding | Fix Hint | Fixed? |
|---|-----------|--------|---------|----------|--------|
| P1 | Value-traced | ✅ | — | — | — |
| P2 | AC testable | ❌ | "AC #3 says 'fast enough'" | Add latency target | ☐ |

## Summary
PASS: X/6 | FAIL: Y/6 → [PASS | REQUEST_CHANGES]
```

**Fix flow:**
1. If `REQUEST_CHANGES` → dispatch fix agent (pm persona) with findings + PRD
2. Fix agent edits PRD in-place, marks `Fixed? ☑` in findings
3. Re-dispatch reviewer (round N+1)
4. Max 2 rounds → ask user

**Result:** `PASS` → proceed to Step 6

---

### Step 6: UI Design Brief (Optional)

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/ux-designer.toml` |
| **Knowledge** | `references/bmad/frameworks/ux-design.md` |
| **Input** | `docs/prd/<version>/<feature>.md` |
| **Output** | `docs/design/<version>/<feature>-ui-brief.md` |

**Skill:** `woos-ui-design-brief`

When the feature has user-facing interface:
- Define screens, layouts, key components
- Define user states (empty, loading, error, success, first-run)
- Establish visual direction
- Optionally generate image concepts

**Trigger:** Before entering Step 6, orchestrator asks user: "Does this feature have user-facing UI?" 
- **Yes** → proceed with Step 6
- **No** → skip Step 6 + 6R, go directly to Step 7

---

### Step 6R: UI Brief Review Gate

| | |
|---|---|
| **Sub-agent** | ✅ (independent reviewer) |
| **Persona** | `references/bmad/personas/ux-designer.toml` |
| **Knowledge** | `references/bmad/frameworks/ux-validate.md` |
| **Input** | `docs/design/<version>/<feature>-ui-brief.md` + `docs/prd/<version>/<feature>.md` |
| **Output** | `docs/reviews/<version>/<feature>-ui-review-rN.md` |

**Checklist:**

| # | Criterion | Fix Hint |
|---|-----------|----------|
| U1 | Screen coverage | List unmapped user stories; add a screen or flow for each |
| U2 | States complete | Add missing states (empty/loading/error/success) to each screen |
| U3 | Flows connected | Trace each flow end-to-end; add missing transitions or exit points |
| U4 | Visual consistency | Remove contradicting principles; pick one direction |
| U5 | Accessibility realistic | Downgrade to achievable level (AAA→AA); document upgrade timeline |
| U6 | Components sufficient | List screens with no component mapping; add or mark as reuse |
| U7 | Principles actionable | Replace generic ("clean", "modern") with decision-guiding rules |

**Fix flow:** Same protocol. Fix agent uses ux-designer persona. Max 2 rounds.

**Result:** `PASS` → proceed to Step 7

---

### Step 7: Analyze Gate

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | _(qa — no BMAD persona needed)_ |
| **Knowledge** | `references/bmad/frameworks/implementation-readiness.md` |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/design/<version>/<feature>-ui-brief.md` (if exists) |
| **Output** | `docs/handoff/<version>/<feature>-analyze-report.md` |

Cross-artifact consistency check:

| Check | Pass Condition |
|-------|----------------|
| A1: Requirement Coverage | Every user story has AC |
| A2: AC Testability | Every AC verifiable without knowing implementation |
| A3: Flow Completeness | All flows have start/end states |
| A4: Non-goal Alignment | No requirement contradicts non-goals |
| A5: UI Coverage | Every screen maps to ≥1 user story (if UI brief exists) |

**Results:**
- **PASS** → proceed to Step 8
- **GAPS_FOUND** → return to Step 4 (requirement gaps) or Step 6 (UI gaps)

---

### Step 8: Build Handoff Packaging

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/epics-and-stories.md` |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/design/<version>/<feature>-ui-brief.md` + analyze report |
| **Output** | `docs/handoff/<version>/<feature>.md` |

**Skill:** `woos-build-handoff`

Package all product artifacts into a single handoff file:
1. Spec versioning (YAML frontmatter)
2. Mission Statement
3. Context (from roadmap)
4. Requirements (user stories + AC + non-goals)
5. User Flows
6. UI Direction (from UI brief, if exists)
7. Build Tasks (product-level breakdown)
8. Verification Plan
9. Open Questions
10. DCR Protocol

**Note:** Technical architecture, data model, API design are NOT in handoff. Engineering decides HOW.

---

### Step 9: Handoff Readiness Check

| | |
|---|---|
| **Sub-agent** | ❌ (orchestrator does this directly) |
| **Input** | `docs/handoff/<version>/<feature>.md` |
| **Output** | `docs/reviews/<version>/<feature>-readiness.md` |

Checklist:
- [ ] All AC are testable
- [ ] Build Tasks map to user stories
- [ ] No unresolved product decisions
- [ ] User flows have no dead ends
- [ ] UI brief covers all interactive features (if applicable)
- [ ] Non-goals clear enough to prevent scope creep
- [ ] DCR protocol specified

**Output file format:**
```markdown
# Readiness Check — <feature>

| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | AC testable | ✅ | — |
| 2 | Tasks → stories | ✅ | — |
| ...

## Verdict: PASS / FAIL
```

**PASS** → handoff ready for engineering (if single feature) or proceed to Step 10 (if multi-feature version)
**FAIL** → return to Step 8 with gaps

---

### Step 10: Version Integration Gate (Cross-Feature Audit)

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/implementation-readiness.md` |
| **Input** | **ALL documents for this version** (see Input Scope below) |
| **Output** | `docs/reviews/<version>/integration-report.md` |

**Trigger:** Runs once after ALL features in this version pass Step 9.
**Skip when:** Version has only 1 feature.

#### Input Scope (MUST read all of these)

The reviewer MUST read the full content of every document below — not just handoffs:

```
docs/product/<project>-roadmap.md
docs/product/<project>-architecture.md
docs/prd/<version>/<feature>-requirements.md   (× all features)
docs/prd/<version>/<feature>.md                (× all features)
docs/handoff/<version>/<feature>.md            (× all features)
docs/design/<version>/<feature>-ui-brief.md    (× all features, if exists)
```

#### Audit Checklist

**Part A — Shared Concept Consistency:**

| # | Check | Method | Example Failure |
|---|-------|--------|-----------------|
| A1 | State machine unified | Extract all state definitions across features. Every feature that references the same entity MUST use identical states + transitions | Feature B: 7 states vs Feature D: 6 states |
| A2 | Constants consistent | Extract all numeric constants (timeouts, limits, intervals). Same concept MUST have same value everywhere | Heartbeat: 30s in architecture vs 90s in requirements |
| A3 | Data model aligned | Extract all entity schemas/types. Same entity MUST have identical fields across features | Task type has `accepted` in C but not in D |
| A4 | API contract consistent | Extract all endpoint definitions. Same endpoint MUST have consistent request/response schemas, status codes, auth | `POST /start` requires `accepted` state in B but `assigned` in D |
| A5 | Terminology unified | Same concept MUST use same name everywhere | "agent" vs "worker" vs "executor" referring to same entity |

**Part B — Completeness & Traceability:**

| # | Check | Method |
|---|-------|--------|
| B1 | Roadmap → Requirements coverage | Every roadmap feature has a requirements file |
| B2 | Requirements → PRD coverage | Every requirement appears in a PRD |
| B3 | PRD → Handoff coverage | Every PRD user story appears in handoff build tasks |
| B4 | Architecture → PRD alignment | Architecture's component list matches PRD's scope |
| B5 | UI → PRD traceability | Every UI screen/action maps to a PRD user story |

**Part C — Cross-Feature Integration:**

| # | Check | Method |
|---|-------|--------|
| C1 | No AC conflicts | Identify conflicting acceptance criteria between features |
| C2 | User flows connectable | Cross-feature flows have matching entry/exit states |
| C3 | No duplicate effort | Similar functionality across features is merged or explicitly split |
| C4 | Dependency order clear | Build order documented for dependent features |
| C5 | Error handling consistent | Same error scenarios handled the same way across features |

#### Output Format

```markdown
# Version Integration Audit — <version>

## Summary
- Features audited: [list]
- Documents read: [count]
- Result: PASS / CONFLICTS_FOUND

## Part A — Shared Concepts

### State Machine
[extract all state definitions, mark ✅ consistent or ❌ contradicts]

### Constants
| Constant | Doc 1 Value | Doc 2 Value | Status |
|----------|-------------|-------------|--------|
| heartbeat_timeout | 30s (architecture) | 90s (B-requirements) | ❌ |

### Data Model
[compare entity fields across features]

### API Contracts
[compare endpoint definitions]

## Part B — Traceability
[coverage matrix: roadmap → requirements → PRD → handoff]

## Part C — Cross-Feature
[C1-C5 findings]

## Verdict
- **PASS**: No contradictions found
- **CONFLICTS_FOUND**: [list each conflict with fix recommendation]

## Recommended Fix Order
1. [highest priority fix — e.g., unify state machine]
2. ...
```

#### Review Rules

- Reviewer MUST produce a finding for EVERY check (A1-A5, B1-B5, C1-C5) — no skipping
- ANY ❌ in Part A = **CONFLICTS_FOUND** (shared concepts MUST be unified before build)
- Part B gaps = **CONFLICTS_FOUND** (traceability must be complete)
- Part C issues = **CONFLICTS_FOUND** unless explicitly documented as intentional divergence

**Results:**
- **PASS** → all handoffs ready for engineering
- **CONFLICTS_FOUND** → return to conflicting feature's Step 4 (PRD) to resolve, then re-run Steps 5–9 for that feature. If conflict is in architecture/roadmap, fix upstream first.

---

## Steps — Standard Mode

Single feature, one review gate, no UI brief or integration gate.

```
Requirements → PRD → PRD Review → Handoff → Readiness
```

| Step | What | Sub-agent? | Output |
|------|------|:----------:|--------|
| S1 | Requirement Contract | ✅ (pm) | `docs/prd/<version>/<feature>-requirements.md` |
| S2 | PRD Authoring | ✅ (pm) | `docs/prd/<version>/<feature>.md` |
| S3 | PRD Review | ✅ (prd-validator) | `docs/reviews/<version>/<feature>-prd-review-rN.md` |
| S4 | Build Handoff | ✅ (pm) | `docs/handoff/<version>/<feature>.md` |
| S5 | Readiness Check | ❌ orchestrator | `docs/reviews/<version>/<feature>-readiness.md` |

**No:** Priority Ranking, UI Brief, UI Review, Analyze Gate, Integration Gate.
**Fix flow:** Same as Strict — max 2 review rounds on S3.

**⚠️ Standard mode enforcement:**
- S1 MUST produce a separate requirements file (not folded into PRD)
- S2 MUST follow `templates/prd-template.md` — E3 structural check applies
- S3 MUST run Phase A (structural) + Phase B (content) review. No "Conditional Pass."
- S5 MUST produce a readiness output file (not just a mental check)

---

## Steps — Lite Mode

| Step | What |
|------|------|
| L1 | One-sentence Mission |
| L2 | Build Tasks (numbered list) |
| L3 | Acceptance Criteria |
| L4 | Verification |
| L5 | Package into Lite handoff using `woos-build-handoff` |

No review gates, no UI brief, no analyze gate. Self-check only.

---

## State Persistence

### Run Manifest Schema (Stage 2 section)

```yaml
stages:
  product-design-flow:
    status: in_progress
    version: "v1"
    features:
      auth:
        current_step: 9
        steps:
          2-requirements: { status: done, output: "docs/prd/v1/auth-requirements.md" }
          3-priority-ranking: { status: done, output: "docs/prd/v1/auth-requirements.md#priority-ranking" }
          4-prd: { status: done, output: "docs/prd/v1/auth.md" }
          5-prd-review: { status: done, round: 1, result: PASS }
          6-ui-brief: { status: skipped }
          6r-ui-review: { status: skipped }
          7-analyze: { status: done, output: "docs/handoff/v1/auth-analyze-report.md" }
          8-handoff: { status: done, output: "docs/handoff/v1/auth.md" }
          9-readiness: { status: done, result: PASS, output: "docs/reviews/v1/auth-readiness.md" }
      dashboard:
        current_step: 4
        steps:
          2-requirements: { status: done, output: "docs/prd/v1/dashboard-requirements.md" }
          3-priority-ranking: { status: done, output: "docs/prd/v1/dashboard-requirements.md#priority-ranking" }
          4-prd: { status: in_progress, output: "docs/prd/v1/dashboard.md" }
          # ... remaining pending
    integration:
      status: pending  # runs after all features pass step 9
      output: null
```

### Recovery Protocol

Same as Stage 1:
1. Read `run-manifest.yaml`
2. Find first step where `status != done`
3. Check output file → exists/well-formed (mark done) | exists/incomplete (resume) | missing (restart step)
4. Continue

### Update Rules
- Write manifest BEFORE dispatching sub-agent (`status: in_progress`)
- Write manifest AFTER sub-agent returns (`status: done` + output)
- Reviews record: `round: N`, `result: PASS|REQUEST_CHANGES`

---

## DCR Reception

When coding agent sends a Design Change Request (`docs/feedback/<feature>-dcr.md`):

1. Read DCR — what product assumption is being challenged?
2. Assess impact:
   - **Small change**: Update handoff directly, notify coding agent
   - **Large change**: Return to Step 4 (PRD) or Step 6 (UI brief)
3. Update handoff version number

---

## Checkpoint Control

```yaml
checkpoints:
  - prd-passed      # Pause after PRD Review PASS
  - handoff-ready   # Pause after Readiness PASS
```

If `checkpoints: []` → fully autonomous.

At each checkpoint: present summary → wait for user confirmation → proceed or return.

## Handoff to Engineering

On completion:
- Handoff: `docs/handoff/<version>/<feature>.md`
- Analyze report: `docs/handoff/<version>/<feature>-analyze-report.md`
- Tell user: "Product handoff ready. Engineering stage can begin."

## Failure Handling

| Situation | Action |
|-----------|--------|
| Roadmap missing | Redirect to `woos-product-discovery` first |
| Review loops 3x | Ask user for direction |
| Scope too large | Split into multiple handoffs per sub-feature |
| UI brief but no interface | Skip Step 6 **only with explicit user confirmation**, note in handoff |
| Crash mid-step | Recovery protocol from run-manifest |
| Sub-agent file not found | Fix path (use absolute), re-dispatch. **NEVER skip.** |
| Output validation fails (E3) | Re-dispatch step with "Missing sections: ..." instruction |
| Step produces empty/stub file | Re-dispatch. Stub output = step not done |

### ❌ Explicitly Forbidden Actions

- **Do NOT merge steps** — each step = 1 sub-agent dispatch → 1 verified output
- **Do NOT skip a step because it "failed"** — fix the failure and retry
- **Do NOT pass a review without checking every row** — partial review = review not done
- **Do NOT accept "Conditional Pass"** — only PASS or REQUEST_CHANGES exist
- **Do NOT write PRD without the template** — free-form PRD = not a PRD

## Skills Used

| Skill | Step |
|-------|------|
| `woos-ui-design-brief` | 6 |
| `woos-build-handoff` | 8 |

---

## Known Anti-Patterns (from real failures)

These are things agents ACTUALLY DO when executing this workflow. Catch yourself:

| Anti-Pattern | Why It's Wrong | Correct Behavior |
|---|---|---|
| Merging Step 2+3 into PRD | Requirements file never exists; priority ranking never done independently | Each step = separate dispatch, separate output file |
| Writing PRD "free-form" | Template sections missing → review can't validate completeness | Copy template, fill each section. Empty section = `[NEEDS CLARIFICATION: reason]` |
| Giving reviewer a vague prompt | "Check for issues" → reviewer only finds 2-3 surface problems | Paste FULL checklist. Require verdict on EVERY row |
| Accepting "Conditional Pass" | Means "partially broken but too lazy to fix" | Only PASS or REQUEST_CHANGES. Conditional = REQUEST_CHANGES |
| Skipping step after file-not-found | The step's output doesn't exist → downstream steps fail silently | Fix path, retry. Never skip |
| Readiness as mental check | No output file → no audit trail, no proof of validation | Write `docs/reviews/<version>/<feature>-readiness.md` |
| Sub-agent reviewing own work | Confirmation bias — author can't see own gaps | Fresh sub-agent with no prior context of authoring |
| Dispatching sub-agent without reading reference files | Sub-agent says "I'm a PM" but has no persona principles, no framework knowledge, no template to follow → shallow generic output | Read persona .toml + knowledge .md + template .md → inject verbatim into dispatch prompt (E7) |
