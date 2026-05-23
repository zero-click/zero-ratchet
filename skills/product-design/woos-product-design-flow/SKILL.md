---
name: woos-product-design-flow
description: "Stage 2 of woos-idea-to-delivery: take a version from the product roadmap and produce PRD + UI direction + build handoff for the coding agent. Focuses on WHAT to build and WHY — technical HOW is deferred to the engineering stage. Runs once per roadmap version."
version: 3.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, design, prd, handoff, review-gate, ui, analyze]
    stage: 2
    flow: woos-idea-to-delivery-v2
---

# Product Design Flow

## Purpose

Transform one version from the product roadmap into a build-ready product handoff. This is **Stage 2** of the woos-idea-to-delivery flow.

Focus: define WHAT to build and WHY. Technical architecture (HOW) is the engineering stage's responsibility.

**Agent:** research

## Project Root Requirement

**CRITICAL:** All file paths (`docs/`) are relative to a **project root directory**. The project root MUST be a real git repository (e.g. `~/code/my-project/`).

**DO NOT** write files to the kanban scratch workspace. The scratch workspace is temporary and will be garbage-collected after task completion.

If running via kanban:
1. If the task has a `workspace_path` pointing to a git repo, use that.
2. If the task is in scratch mode, **clone or create the target repo first**, then write all files there.
3. The project root must contain `docs/` — create it if it doesn't exist.
4. Ask the user for the project directory if not specified.

## When to Use

- User says "start V1" / "design this feature" / "ready to build X"
- Product roadmap exists and a version has been selected

## Prerequisites

- `docs/product/<project>-roadmap.md` exists (from `woos-product-discovery` or user-provided)

## Modes

| Mode | When | Gate Reviews | Handoff Contents |
|------|------|-------------|-----------------|
| **Standard** | Default. Multi-feature version, UX decisions matter | PRD Review + Analyze Gate | Full (requirements, user flows, UI brief, AC) |
| **Lite** | Small scope, obvious UX, low risk | None (self-check only) | 4 fields: Mission, Tasks, AC, Verification |

## Persona Switching

Standard mode uses two personas:

```
[PM Mode] Steps 1–4
  Mindset: user value, acceptance criteria, priorities, non-goals
  ↓ PRD Review PASS
[Design Mode] Step 5 (optional)
  Mindset: user experience, interface clarity, interaction flows
  ↓
[QA Mode] Steps 6–8
  Mindset: consistency, coverage, completeness
```

**When switching persona:**
- Clear the previous persona's biases
- Adopt the new persona's evaluation criteria

## Steps — Standard Mode

### Step 1: Select Version Scope

**[PM Mode]**

Read `docs/product/<project>-roadmap.md`, extract the target version. Confirm with user:
- Feature list and boundaries
- Non-goals (what we're NOT building)
- Success metrics (how we'll know it worked)

### Step 2: Requirement Contract

**[PM Mode]**

Produce structured requirement contract:
- Goals and constraints
- Acceptance criteria (machine-checkable where possible)
- Non-goals
- Risk assumptions and unknowns

**Output:** `docs/prd/<feature>-requirements.md`

### Step 3: PRD Authoring

**[PM Mode]**

Write full PRD:
- User stories with acceptance criteria
- Functional and non-functional requirements
- Edge cases and error handling
- User flows (text-based flow descriptions)

**Output:** `docs/prd/<feature>.md`

### Step 4: PRD Review Gate

**[PM Mode → Checkpoint]**

**Reviewer:** Independent sub-agent dispatched in fresh context (product-planner persona).

**Checklist:**

| # | Criterion | What to check |
|---|-----------|---------------|
| P1 | Value-traced | Every requirement traces back to user value (no "nice to have" as must-have) |
| P2 | AC testable | Acceptance criteria verifiable without knowing implementation |
| P3 | Non-goals effective | Clearly prevent scope creep (specific enough to say "no" to requests) |
| P4 | Edge cases covered | Not hand-waved — specific scenarios with expected behavior |
| P5 | Real user behavior | User stories reflect actual usage, not developer convenience |
| P6 | No contradictions | Requirements don't conflict with each other or non-goals |

**Dispatch:** `delegate_task` → fresh context, product-planner role, read PRD + requirements + roadmap.

**Review Findings Output:** `docs/reviews/<feature>-prd-review-rN.md`

```markdown
# PRD Review — Round N

| # | Criterion | Status | Finding | Fixed? |
|---|-----------|--------|---------|--------|
| P1 | Value-traced | ✅ PASS | — | — |
| P2 | AC testable | ❌ FAIL | "AC #3 says 'fast enough' — needs specific latency target" | ☐ |
| P3 | Non-goals effective | ✅ PASS | — | — |
| P4 | Edge cases covered | ❌ FAIL | "No mention of offline/network-error behavior" | ☐ |
| P5 | Real user behavior | ✅ PASS | — | — |
| P6 | No contradictions | ✅ PASS | — | — |

## Summary
PASS: 4/6 | FAIL: 2/6 → REQUEST_CHANGES
```

**Flow:**
1. Reviewer outputs findings with ❌/✅ per criterion
2. Author agent fixes each ❌ item, marks `Fixed? ☑` in findings file
3. Re-review: reviewer checks only `Fixed? ☑` rows — verifies fix is adequate
4. New issues found during re-review → append as new rows

**Results:**
- **PASS** → all criteria ✅ → proceed to Step 5
- **REQUEST_CHANGES** → return to Step 3, fix per findings checklist
- 3 rounds without convergence → ask user for direction

**Checkpoint:** If configured, pause here and present PRD summary to user for confirmation.

### Step 5: UI Design Brief (Optional)

**[Design Mode]**

**Skill:** `woos-ui-design-brief`

When the feature has user-facing interface:
- Define screens, layouts, key components
- Define user states (empty, loading, error, success, first-run)
- Establish visual direction
- Optionally generate image concepts for taste alignment

**Output:** `docs/design/<feature>-ui-brief.md`

**Skip when:**
- Pure API/backend/CLI work
- Lite mode
- User explicitly declines

### Step 5R: UI Brief Review Gate (when Step 5 runs)

**Reviewer:** Independent sub-agent dispatched in fresh context (ux-reviewer persona).

**Checklist:**

| # | Criterion | What to check |
|---|-----------|---------------|
| U1 | Screen coverage | Every screen maps to ≥1 user story from PRD |
| U2 | States complete | All important states defined (empty, loading, error, success, first-run) |
| U3 | Flows connected | User flows have clear entry/exit matching PRD flows, no dead ends |
| U4 | Visual consistency | Design principles don't contradict each other |
| U5 | Accessibility realistic | A11y targets achievable for the platform and timeline |
| U6 | Components sufficient | Component inventory covers all screens (no orphans) |
| U7 | Principles actionable | Design principles guide real decisions (not generic platitudes) |

**Dispatch:** `delegate_task` → fresh context, ux-reviewer role, read UI brief + PRD.

**Review Findings Output:** `docs/reviews/<feature>-ui-review-rN.md`

```markdown
# UI Brief Review — Round N

| # | Criterion | Status | Finding | Fixed? |
|---|-----------|--------|---------|--------|
| U1 | Screen coverage | ✅ PASS | — | — |
| U2 | States complete | ❌ FAIL | "Settings screen missing error state" | ☐ |
| U3 | Flows connected | ✅ PASS | — | — |
| U4 | Visual consistency | ✅ PASS | — | — |
| U5 | Accessibility realistic | ❌ FAIL | "AAA target unrealistic for V1 timeline — suggest AA" | ☐ |
| U6 | Components sufficient | ✅ PASS | — | — |
| U7 | Principles actionable | ✅ PASS | — | — |

## Summary
PASS: 5/7 | FAIL: 2/7 → REQUEST_CHANGES
```

**Flow:**
1. Reviewer outputs findings with ❌/✅ per criterion
2. Author agent fixes each ❌ item, marks `Fixed? ☑` in findings file
3. Re-review: reviewer checks only `Fixed? ☑` rows — verifies fix is adequate
4. New issues found during re-review → append as new rows

**Results:**
- **PASS** → all criteria ✅ → proceed to Step 6
- **REQUEST_CHANGES** → return to Step 5, fix per findings checklist

Max 2 rounds. If no convergence → ask user for direction.

### Step 6: Analyze Gate

**[QA Mode]**

Cross-artifact product consistency check. Run BEFORE packaging the handoff.

| Check | What | Pass Condition |
|-------|------|----------------|
| A1: Requirement Coverage | Every user story has acceptance criteria | 100% coverage |
| A2: AC Testability | Every AC is verifiable without knowing implementation | 100% testable |
| A3: Flow Completeness | All user flows from PRD have defined start/end states | No dead-end flows |
| A4: Non-goal Alignment | No requirement contradicts stated non-goals | Zero conflicts |
| A5: UI Coverage | If UI brief exists, every screen maps to ≥1 user story | No orphan screens |

**Output:** `docs/handoff/<feature>-vN-analyze-report.md`

**Results:**
- **PASS** → all checks green → proceed to Step 7
- **GAPS_FOUND** → return to relevant step (Step 3 for requirement gaps, Step 5 for UI gaps)

### Step 7: Build Handoff Packaging

**[QA Mode]**

**Skill:** `woos-build-handoff`

Package all product artifacts into a single handoff file that a fresh coding agent can work from independently.

**Output:** `docs/handoff/<feature>-vN.md`

Handoff contains:
1. Spec versioning (YAML frontmatter: `spec-version`, `based-on`)
2. Mission Statement (one paragraph: what and why)
3. Context (from roadmap — target users, market position)
4. Requirements (user stories + AC + non-goals)
5. User Flows (step-by-step flow descriptions)
6. UI Direction (summary from UI brief, if exists)
7. Build Tasks (product-level task breakdown)
8. Verification Plan (how to confirm each AC is met)
9. Open Questions (anything the engineering stage should resolve)
10. DCR Protocol (how coding agent reports product issues back)

**Note:** Technical architecture, data model, API design are NOT in this handoff. Those are the engineering stage's job. The handoff defines WHAT to build; engineering decides HOW.

### Step 8: Handoff Readiness Check

**[QA Mode]**

Checklist:
- [ ] All AC are testable
- [ ] Build Tasks map to user stories
- [ ] No unresolved product decisions remain
- [ ] User flows have no dead ends
- [ ] UI brief covers all interactive features (if applicable)
- [ ] Non-goals are clear enough to prevent scope creep
- [ ] DCR protocol is specified

**PASS** → handoff ready for engineering stage
**FAIL** → return to Step 7 with gaps

## Steps — Lite Mode

| Step | What |
|------|------|
| L1 | One-sentence Mission: what we're building and why |
| L2 | Build Tasks: numbered list of product objectives |
| L3 | Acceptance Criteria: how to verify each task |
| L4 | Verification: how to confirm completion |
| L5 | Package into Lite handoff (4 fields) using `woos-build-handoff` |

No review gates, no UI brief, no analyze gate. Self-check only.

## DCR Reception

When coding agent sends a Design Change Request (`docs/feedback/<feature>-dcr.md`):

1. Read DCR — what product assumption is being challenged?
2. Assess impact:
   - **Small change**: Update handoff directly, notify coding agent to continue
   - **Large change**: Return to Step 3 (PRD) or Step 5 (UI brief) to revise
3. Update handoff version number

## Checkpoint Control

Standard mode supports optional checkpoints:

```yaml
checkpoints:
  - prd-passed      # Pause after PRD Review PASS
  - handoff-ready   # Pause after Handoff Readiness PASS
```

If `checkpoints: []` or field absent → fully autonomous (no pauses).

At each checkpoint:
1. Present summary to user
2. Wait for confirmation
3. If user requests changes → return to relevant step
4. If user confirms → proceed

## Handoff to Next Stage

On completion:
- Handoff file at `docs/handoff/<feature>-vN.md`
- Analyze report at `docs/handoff/<feature>-vN-analyze-report.md`
- Tell user: "Product handoff ready. Engineering stage can begin."
- If using kanban: create task assigned to `coding` with handoff file path

## File Layout

```text
<project-root>/
├── docs/
│   ├── product/<project>-roadmap.md          ← input (from Stage 1)
│   ├── prd/
│   │   ├── <feature>-requirements.md         ← Step 2 output
│   │   └── <feature>.md                      ← Step 3 output
│   ├── design/
│   │   └── <feature>-ui-brief.md             ← Step 5 output (optional)
│   ├── handoff/
│   │   ├── <feature>-vN.md                   ← main output
│   │   └── <feature>-vN-analyze-report.md    ← Step 6 output
│   └── feedback/<feature>-dcr.md             ← DCR input (from engineering)
```

## Failure Handling

| Situation | Action |
|-----------|--------|
| Roadmap missing | Redirect to `woos-product-discovery` first |
| Review loops 3x | Ask user for direction |
| Scope too large for one handoff | Split into multiple handoffs; one per sub-feature |
| UI brief requested but no interface | Skip Step 5, note in handoff |

## Skills Used

| Skill | Purpose |
|-------|---------|
| `woos-ui-design-brief` | Step 5 (optional) |
| `woos-build-handoff` | Step 7 |
