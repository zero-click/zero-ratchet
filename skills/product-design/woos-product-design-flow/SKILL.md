---
name: woos-product-design-flow
description: "Stage 3 orchestrator: route dedicated product-design skills to turn an approved roadmap version into PRDs, UI direction, and build handoff."
version: 6.0.0
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
- Step 1.5: feature dependency analysis
- Step 8.5: interface summary extraction (bookkeeping, not creative)

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
| Step 1.5 | execution order + interface pass-through plan stated (Strict only) |
| Step 2 | `docs/prd/<version>/<feature>-requirements.md` exists with required sections and `## Priority Ranking` |
| Step 3 | `docs/prd/<version>/<feature>.md` exists with required sections |
| Step 4 | PRD review file exists with explicit `PASS` or `REQUEST_CHANGES` |
| Step 5 | UI brief exists when UI is in scope |
| Step 5R | UI review file exists with explicit `PASS` or `REQUEST_CHANGES` |
| Step 6 | analyze report exists with explicit `PASS` or `GAPS_FOUND` |
| Step 7 | handoff file exists |
| Step 8 | readiness report exists with explicit `PASS` or `FAIL` |
| Step 8.5 | `docs/prd/<version>/<feature>-interface.md` exists (Strict only) |
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

### P6: Fix Propagation (Global Sync)

When any review gate returns `REQUEST_CHANGES` and a fix is applied:

1. Identify all terms, enums, field names, or concepts that were modified
2. Grep ALL existing version documents (`docs/prd/<version>/`, `docs/design/<version>/`, `docs/handoff/<version>/`, `docs/product/`) for those terms
3. Update every occurrence to maintain consistency
4. If an upstream interface summary exists for a completed feature and the fix contradicts it, update the interface summary too

This rule applies regardless of which step triggered the fix. A single-file fix is never sufficient when the modified concept appears in other documents.

### P7: Upstream Interface Awareness

When Step 1.5 identifies `feeds` or `mutual` relationships, downstream features MUST receive upstream interface summaries as additional input in Steps 2, 3, 4, and 6. The orchestrator determines which summaries to pass based on the dependency graph — only direct dependencies, not transitive.

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
| **Strict** | Multi-feature version, higher uncertainty, UX-heavy | Select Scope → Dependency Analysis → [per feature: Requirements → PRD → Review → UI → UI Review → Analyze → Handoff → Readiness → Interface Summary → Integration (incremental)] |

---

## Steps — Strict Mode

The orchestrator runs per feature:

```text
Step 1:   Select Version Scope
Step 1.5: Feature Dependency Analysis (auto, Strict only)
  → For each feature (in dependency order):
      Steps 2–8.5
      Step 9 (incremental, after 2nd+ feature)
  → After last feature passes Step 9:
      Done — all handoffs ready
```

### Step 1: Select Version Scope

| | |
|---|---|
| **Skill** | direct orchestrator step |
| **Input** | `docs/product/<project>-roadmap.md` |
| **Output** | selected version + feature list for downstream steps |

**Advance when:** the version, feature boundaries, non-goals, and success metrics are confirmed.

---

### Step 1.5: Feature Dependency Analysis

| | |
|---|---|
| **Skill** | direct orchestrator step |
| **Trigger** | Strict mode with 2+ features |
| **Input** | `docs/product/<project>-roadmap.md` § selected version features |
| **Output** | ordered execution plan (inline, not a separate file) |

The orchestrator scans the roadmap features for shared entities:

1. **Extract shared signals** — identify mentions of shared data models, shared state, common APIs/endpoints, or explicit "depends on Feature X" references across features
2. **Classify relationships:**
   - `independent` — no shared entities, can run in any order
   - `feeds` — Feature A produces a concept that Feature B consumes (A before B)
   - `mutual` — features share a concept but neither strictly depends on the other
3. **Determine execution order:**
   - `independent` features: process in roadmap-listed order (arbitrary but deterministic)
   - `feeds` relationships: process upstream feature first
   - `mutual` relationships: process in roadmap-listed order, but flag for Step 9 integration focus

**Output format (stated before proceeding):**

```text
Execution order:
  1. <feature-A> (independent)
  2. <feature-B> (feeds: depends on A's <shared-entity>)
  3. <feature-C> (mutual with B — flagged for integration audit)

Interface pass-through:
  - F-B receives: F-A interface summary
  - F-C receives: F-B interface summary
```

**Advance when:** execution order AND interface pass-through plan are determined. No blocking — this step always produces a result.

**Skip when:** Standard or Lite mode (single feature, no dependency to analyze).

---

### Step 2: Requirement Contract

| | |
|---|---|
| **Skill** | `woos-requirement-contract` |
| **Input** | `docs/product/<project>-roadmap.md` § selected version |
| **Conditional input** | `docs/prd/<version>/<upstream-feature>-interface.md` for each upstream dependency (per Step 1.5 graph) |
| **Output** | `docs/prd/<version>/<feature>-requirements.md` |

**Advance when:** the requirements file exists, passes structural validation, and includes an explicit `P0/P1/P2` ranking with cut-line.

---

### Step 3: PRD Authoring

| | |
|---|---|
| **Skill** | `woos-prd-authoring` |
| **Input** | `docs/prd/<version>/<feature>-requirements.md` |
| **Conditional input** | `docs/prd/<version>/<upstream-feature>-interface.md` for each upstream dependency |
| **Output** | `docs/prd/<version>/<feature>.md` |

**Advance when:** the PRD file exists and proceeds to Step 4.

---

### Step 4: PRD Review Gate

| | |
|---|---|
| **Skill** | `woos-product-prd-review-gate` |
| **Execution** | isolated subagent |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/prd/<version>/<feature>-requirements.md` + `docs/product/<project>-architecture.md` |
| **Conditional input** | `docs/prd/<version>/<upstream-feature>-interface.md` for each upstream dependency |
| **Output** | `docs/reviews/<version>/<feature>-prd-review-rN.md` |

**Review loop:** `REQUEST_CHANGES` → fix PRD (apply P6: grep + sync all affected docs) → re-run review. Max 2 rounds before asking the user for direction.

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
| **Conditional input** | `docs/prd/<version>/<upstream-feature>-interface.md` for each upstream dependency |
| **Output** | `docs/handoff/<version>/<feature>-analyze-report.md` |

**Advance when:** verdict is `PASS`.

**If `GAPS_FOUND`:**

- requirement / PRD gap → return to Step 3 (apply P6: global sync)
- UI gap → return to Step 5 (apply P6: global sync)

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

- `PASS` → continue to Step 8.5
- `FAIL` → return to Step 7

---

### Step 8.5: Interface Summary Extraction

| | |
|---|---|
| **Skill** | direct orchestrator step |
| **Trigger** | Strict mode, after Step 8 PASS |
| **Input** | `docs/prd/<version>/<feature>-requirements.md` + `docs/prd/<version>/<feature>.md` + `docs/handoff/<version>/<feature>.md` |
| **Output** | `docs/prd/<version>/<feature>-interface.md` |

The orchestrator extracts the feature's **shared interface contract** — a lightweight summary (~500 bytes–1KB) of concepts that other features may depend on:

```markdown
# <Feature> — Interface Summary

## Status Enums
- <enum_name>: value1 | value2 | value3

## Data Models (shared fields only)
- <model_name>: field1 (type), field2 (type), ...

## Event Types / Messages
- <event_name>: { payload fields }

## API Endpoints (if defined)
- METHOD /path → response shape

## Key Terminology
- <term>: definition as used in this feature
```

**Rules:**
- Extract ONLY what is defined/introduced by THIS feature, not what it consumes from upstream
- Include only concepts that have cross-feature relevance (appear in dependency graph)
- This is bookkeeping extraction, not creative work — no new analysis
- If the feature introduces no shared concepts (independent), write a minimal file noting "No shared interface"

**Advance when:** interface summary file exists.

**Skip when:** Standard or Lite mode (single feature, no downstream consumers).

---

### Step 9: Version Integration Gate

| | |
|---|---|
| **Skill** | `woos-version-integration-audit` |
| **Execution** | isolated subagent |
| **Input** | all interface summaries + roadmap + architecture + script extraction output |
| **Output** | `docs/reviews/<version>/integration-report.md` (or `integration-report-after-<feature>.md` for incremental runs) |

**Trigger:** Strict mode with 2+ features. Runs **incrementally**:

- After the **2nd feature** completes Step 8.5 → first integration check (F1 + F2)
- After each subsequent feature completes Step 8.5 → incremental integration check (all completed features)
- Final run after the last feature → full integration report

**Incremental strategy:**

The integration audit script receives ALL completed interface summaries plus the full docs of only the NEWLY completed feature. This keeps context bounded:

```text
Full docs loaded:     newest feature only
Interface summaries:  all previously completed features
Script pre-filter:    extract conflict candidates before semantic review
```

**Skip when:** the version has only one feature.

**Results:**

- `PASS` → continue to next feature (or done if last)
- `CONFLICTS_FOUND` → fix before proceeding to next feature (apply P6: global sync)

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
