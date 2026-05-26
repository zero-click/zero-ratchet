---
name: woos-product-design-flow
description: "Stage 3 orchestrator: route dedicated product-design skills to turn an approved roadmap version into PRDs, UI direction, and build handoff."
version: 5.1.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, design, prd, handoff, orchestrator]
    stage: 3
    flow: woos-idea-to-design
    related_skills:
      - woos-requirement-contract
      - woos-prd-authoring
      - woos-product-prd-review-gate
      - woos-ui-design-brief
      - woos-ui-brief-review
      - woos-prd-consistency-audit
      - woos-build-handoff
      - woos-handoff-readiness-check
      - woos-version-integration-audit
---

# Product Design Flow (Orchestrator)

> You are an ORCHESTRATOR.
>
> You do not write requirements, PRDs, UI briefs, reviews, audits, or handoffs yourself.
> You route dedicated skills, validate outputs, and control transitions.

## ⛔ Enforcement Rules (NON-NEGOTIABLE)

### P0: Explicit Step Dispatch

Before executing any step, state the step being run and the exact:

- skill name
- input file(s)
- output file

### P1: Orchestrator Does Not Author Artifacts

The orchestrator may directly execute only:

- Step 1: version scope selection

All other outputs must come from their declared skills.

### P2: No Step Merging or Silent Skipping

- Each step has its own output
- Steps run in order
- Failures are fixed and retried, not skipped
- Optional UI steps may be skipped only when the user confirms there is no user-facing UI
- Step 9 may be skipped only when the version has a single feature

### P3: Validate Output Before Advancing

After each step, verify the declared output exists and is substantive.

| Step | Required result |
|------|-----------------|
| Step 2 | `docs/prd/<version>/<feature>-requirements.md` exists with required sections and `## Priority Ranking` |
| Step 3 | `docs/prd/<version>/<feature>.md` exists with required sections |
| Step 4 | PRD review file exists with explicit `PASS` or `REQUEST_CHANGES` |
| Step 5 | UI brief exists when UI is in scope |
| Step 5R | UI review file exists with explicit `PASS` or `REQUEST_CHANGES` |
| Step 6 | analyze report exists with explicit `PASS` or `GAPS_FOUND` |
| Step 7 | handoff file exists |
| Step 8 | readiness report exists with explicit `PASS` or `FAIL` |
| Step 9 | integration report exists with explicit `PASS` or `CONFLICTS_FOUND` |

### P4: No Self-Review

Review and audit steps must always use their dedicated skills in fresh context.

### P5: Mandatory Subagent Isolation

The following steps MUST run in isolated subagent contexts so their skill loads, review logic, and audit evidence do not pollute the orchestrator context:

- Step 4: `woos-product-prd-review-gate`
- Step 5R: `woos-ui-brief-review`
- Step 6: `woos-prd-consistency-audit`
- Step 8: `woos-handoff-readiness-check`
- Step 9: `woos-version-integration-audit`

---

## Purpose

Transform one approved roadmap version into build-ready product handoff files. This is **Stage 3** of the `woos-idea-to-design` flow.

Product defines **WHAT** and **WHY**. Engineering decides **HOW**.

## Project Root Requirement

All file paths (`docs/`) are relative to a project root directory which must be a git repository.

## Prerequisites

- `docs/product/<project>-roadmap.md` exists
- Discovery human approval has passed
- The target version has been selected from the roadmap

## Modes

| Mode | When | Steps |
|------|------|-------|
| **Lite** | Small scope, obvious, 1-2 days work | Mission → Tasks → AC → Handoff |
| **Standard** | Single feature, moderate complexity | Requirements → PRD → PRD Review → Handoff → Readiness |
| **Strict** | Multi-feature version, higher uncertainty, UX-heavy | Select Scope → Requirements → PRD → Review → UI → UI Review → Analyze → Handoff → Readiness → Integration |

---

## Steps — Strict Mode

The orchestrator runs per feature:

```text
Step 1: Select Version Scope
  → For each feature:
      Steps 2–8
  → After all features pass Step 8:
      Step 9
```

### Step 1: Select Version Scope

| | |
|---|---|
| **Skill** | direct orchestrator step |
| **Input** | `docs/product/<project>-roadmap.md` |
| **Output** | selected version + feature list for downstream steps |

**Advance when:** the version, feature boundaries, non-goals, and success metrics are confirmed.

---

### Step 2: Requirement Contract

| | |
|---|---|
| **Skill** | `woos-requirement-contract` |
| **Input** | `docs/product/<project>-roadmap.md` § selected version |
| **Output** | `docs/prd/<version>/<feature>-requirements.md` |

**Advance when:** the requirements file exists, passes structural validation, and includes an explicit `P0/P1/P2` ranking with cut-line.

---

### Step 3: PRD Authoring

| | |
|---|---|
| **Skill** | `woos-prd-authoring` |
| **Input** | `docs/prd/<version>/<feature>-requirements.md` |
| **Output** | `docs/prd/<version>/<feature>.md` |

**Advance when:** the PRD file exists and proceeds to Step 4.

---

### Step 4: PRD Review Gate

| | |
|---|---|
| **Skill** | `woos-product-prd-review-gate` |
| **Execution** | isolated subagent |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/prd/<version>/<feature>-requirements.md` + `docs/product/<project>-architecture.md` |
| **Output** | `docs/reviews/<version>/<feature>-prd-review-rN.md` |

**Review loop:** `REQUEST_CHANGES` → fix PRD → re-run review. Max 2 rounds before asking the user for direction.

---

### Step 5: UI Design Brief

| | |
|---|---|
| **Skill** | `woos-ui-design-brief` |
| **Input** | `docs/prd/<version>/<feature>.md` |
| **Output** | `docs/design/<version>/<feature>-ui-brief.md` |

**Trigger:** ask whether the feature has user-facing UI.

- `Yes` → run Step 5, then Step 5R
- `No` → skip Step 5 and Step 5R, continue to Step 6

---

### Step 5R: UI Brief Review Gate

| | |
|---|---|
| **Skill** | `woos-ui-brief-review` |
| **Execution** | isolated subagent |
| **Input** | `docs/design/<version>/<feature>-ui-brief.md` + `docs/prd/<version>/<feature>.md` |
| **Output** | `docs/reviews/<version>/<feature>-ui-review-rN.md` |

**Review loop:** `REQUEST_CHANGES` → fix UI brief → re-run review. Max 2 rounds before asking the user for direction.

---

### Step 6: Analyze Gate

| | |
|---|---|
| **Skill** | `woos-prd-consistency-audit` |
| **Execution** | isolated subagent |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/design/<version>/<feature>-ui-brief.md` (if exists) |
| **Output** | `docs/handoff/<version>/<feature>-analyze-report.md` |

**Advance when:** verdict is `PASS`.

**If `GAPS_FOUND`:**

- requirement / PRD gap → return to Step 3
- UI gap → return to Step 5

---

### Step 7: Build Handoff

| | |
|---|---|
| **Skill** | `woos-build-handoff` |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/design/<version>/<feature>-ui-brief.md` (if exists) + `docs/handoff/<version>/<feature>-analyze-report.md` (if exists) |
| **Output** | `docs/handoff/<version>/<feature>.md` |

**Advance when:** the handoff file exists and is substantive.

---

### Step 8: Handoff Readiness Check

| | |
|---|---|
| **Skill** | `woos-handoff-readiness-check` |
| **Execution** | isolated subagent |
| **Input** | `docs/handoff/<version>/<feature>.md` |
| **Output** | `docs/reviews/<version>/<feature>-readiness.md` |

**Results:**

- `PASS` → feature is ready; if all features are ready, continue to Step 9
- `FAIL` → return to Step 7

---

### Step 9: Version Integration Gate

| | |
|---|---|
| **Skill** | `woos-version-integration-audit` |
| **Execution** | isolated subagent |
| **Input** | all roadmap / architecture / requirements / PRD / handoff / UI brief files for the version |
| **Output** | `docs/reviews/<version>/integration-report.md` |

**Trigger:** runs once after all features pass Step 8.

**Skip when:** the version has only one feature.

**Results:**

- `PASS` → all handoffs are ready for engineering
- `CONFLICTS_FOUND` → return to the conflicting feature's Step 3 or fix upstream discovery artifacts first

---

## Steps — Standard Mode

Single feature, no priority/UI/analyze/integration path.

| Step | Skill | Output |
|------|-------|--------|
| S1 | `woos-requirement-contract` | `docs/prd/<version>/<feature>-requirements.md` |
| S2 | `woos-prd-authoring` | `docs/prd/<version>/<feature>.md` |
| S3 | `woos-product-prd-review-gate` | `docs/reviews/<version>/<feature>-prd-review-rN.md` |
| S4 | `woos-build-handoff` | `docs/handoff/<version>/<feature>.md` |
| S5 | `woos-handoff-readiness-check` | `docs/reviews/<version>/<feature>-readiness.md` |

---

## Steps — Lite Mode

Lite skips the review/audit pipeline and uses `woos-build-handoff` to package:

1. Mission
2. Build Tasks
3. Acceptance Criteria
4. Verification

## DCR Reception

When engineering sends `docs/feedback/<feature>-dcr.md`:

1. Read the DCR
2. Assess impact
3. Small change → update handoff directly
4. Large change → return to Step 3 or Step 5

## Handoff to Engineering

On completion:

- Handoff: `docs/handoff/<version>/<feature>.md`
- Analyze report: `docs/handoff/<version>/<feature>-analyze-report.md` (if generated)
- Integration report: `docs/reviews/<version>/integration-report.md` (Strict only)

---

## Failure Handling

| Situation | Action |
|-----------|--------|
| Roadmap missing | Return to `woos-product-discovery` |
| Review loop hits max rounds | Ask the user for direction |
| Scope too large | Split into multiple handoffs |
| Output file missing or stub | Re-run the same declared step |
| Script-based audit fails | Fix the inputs or parser bug, then re-run |
