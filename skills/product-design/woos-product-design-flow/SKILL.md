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

## Purpose

Transform one version from the product roadmap into a build-ready product handoff. This is **Stage 2** of the woos-idea-to-delivery flow. Run once per version.

Focus: define WHAT to build and WHY. Technical architecture (HOW) is engineering's job.

## Role

This file defines an **orchestrator** — a thin state machine that:
1. Tracks which step we're on (via `run-manifest.yaml`)
2. Dispatches sub-agents with the right persona + knowledge
3. Collects outputs, decides next step
4. Handles review fix loops

## Project Root Requirement

All file paths (`docs/`) are relative to a **project root directory** which MUST be a git repository.

## When to Use

- User says "start V1" / "design this feature" / "ready to build X"
- Product roadmap exists and a version has been selected

## Prerequisites

- `docs/product/<project>-roadmap.md` exists (from Stage 1)

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

---

### Step 5: PRD Review Gate

| | |
|---|---|
| **Sub-agent** | ✅ (independent reviewer) |
| **Persona** | `references/bmad/personas/prd-validator.toml` |
| **Knowledge** | `references/bmad/frameworks/validate-prd.md` + `references/bmad/templates/prd-validation-checklist.md` |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/prd/<version>/<feature>-requirements.md` |
| **Output** | `docs/reviews/<version>/<feature>-prd-review-rN.md` |

**Checklist:**

| # | Criterion | Fix Hint |
|---|-----------|----------|
| P1 | Value-traced | Add "User value: …" line linking each requirement to a user outcome |
| P2 | AC testable | Rewrite as "Given X, When Y, Then Z" or add measurable threshold |
| P3 | Non-goals effective | Make specific enough to reject a concrete feature request |
| P4 | Edge cases covered | Add "What if…" for: empty state, error, timeout, concurrent access |
| P5 | Real user behavior | Replace developer-centric language with user-observable actions |
| P6 | No contradictions | Identify conflicts; pick one, move the other to non-goals |

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

### Step 10: Version Integration Gate

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/implementation-readiness.md` |
| **Input** | All `docs/handoff/<version>/<feature>.md` for this version |
| **Output** | `docs/reviews/<version>/integration-report.md` |

**Trigger:** Runs once after ALL features in this version pass Step 9.
**Skip when:** Version has only 1 feature.

**Checklist:**

| # | Criterion | Fix Hint |
|---|-----------|----------|
| I1 | No AC conflicts | Identify conflicting AC between features; resolve or make one non-goal |
| I2 | Shared components consistent | If features reference same component, verify specs don't contradict |
| I3 | User flows connectable | Cross-feature flows (e.g., auth → dashboard) have matching entry/exit |
| I4 | No duplicate effort | If two features define similar functionality, merge or explicitly split |
| I5 | Dependency order clear | If feature B depends on feature A, note build order in report |

**Results:**
- **PASS** → all handoffs ready for engineering
- **CONFLICTS** → return to conflicting feature's Step 4 (PRD) to resolve, then re-run Steps 5–9 for that feature

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
| S5 | Readiness Check | ❌ orchestrator | _(pass/fail)_ |

**No:** Priority Ranking, UI Brief, UI Review, Analyze Gate, Integration Gate.
**Fix flow:** Same as Strict — max 2 review rounds on S3.

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
| UI brief but no interface | Skip Step 6, note in handoff |
| Crash mid-step | Recovery protocol from run-manifest |

## Skills Used

| Skill | Step |
|-------|------|
| `woos-ui-design-brief` | 6 |
| `woos-build-handoff` | 8 |
