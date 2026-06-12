---
name: woos-product-design-flow
description: "Stage 3 orchestrator: route dedicated product-design skills to turn an approved roadmap version into reviewed PRDs and interface summaries ready for coding agents."
version: 7.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, design, prd, orchestrator]
    stage: 3
    flow: woos-idea-to-design
    related_skills:
      - woos-requirement-contract
      - woos-prd-authoring
      - woos-product-prd-review-gate
      - woos-ui-design-brief
      - woos-ui-brief-review
      - woos-prd-consistency-audit
      - woos-version-integration-audit
---

# Product Design Flow (Orchestrator)

> You are an ORCHESTRATOR.
>
> You do not write requirements, PRDs, UI briefs, reviews, or audits yourself.
> You route dedicated skills, validate outputs, and control transitions.

## Design Principles

1. **PRD is the source of truth.** Coding agents receive the full PRD directly. No intermediate "handoff" layer.
2. **Per-feature checkpoint.** After each feature completes its design pipeline, the orchestrator pauses and asks the user whether to deliver it to engineering now or continue designing the next feature.
3. **Sequential execution.** Features are designed one at a time, in dependency order.
4. **Product defines WHAT/WHY, Engineering decides HOW.** Including task decomposition and ordering.

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
- Step 6.5: interface summary extraction (bookkeeping, not creative)

All other outputs must come from their declared skills.

### P2: No Step Merging or Silent Skipping

- Each step has its own output
- Steps run in order
- Failures are fixed and retried, not skipped
- Optional UI steps may be skipped only when the user confirms there is no user-facing UI
- Step 7 may be skipped only when the version has a single feature

### P3: Validate Output Before Advancing

After each step, verify the declared output exists and is substantive.

| Step | Required result |
|------|-----------------|
| Step 1.5 | execution order + feature IDs + interface pass-through plan stated (Strict only) |
| Step 2 | `docs/prd/<version>/<feature-id>-requirements.md` exists with required sections and `## Priority Ranking` |
| Step 3 | `docs/prd/<version>/<feature-id>.md` exists with required sections |
| Step 4 | PRD review file exists with explicit `PASS` or `REQUEST_CHANGES` |
| Step 5 | UI brief exists when UI is in scope |
| Step 5R | UI review file exists with explicit `PASS` or `REQUEST_CHANGES` |
| Step 6 | Analyze report exists with explicit `PASS` or `GAPS_FOUND` |
| Step 6.5 | `docs/prd/<version>/<feature-id>-interface.md` exists (Strict only) |
| Step 7 | Integration report exists with explicit `PASS` or `CONFLICTS_FOUND` **and** a `## Verdict` section authored by the semantic phase (raw `SIGNALS_CLEAR` / `HOTSPOTS_FOUND` script output is not a completed gate output) |
| Step 7-Final | `docs/reviews/<version>/integration-report.md` exists with verdict `PASS` after a `--final-run` invocation that loads full requirements/PRD/UI for every audited feature (Strict, 2+ features only) |

After all steps pass: **feature design is complete → CHECKPOINT.**

### P4: No Self-Review

Review and audit steps must always use their dedicated skills in fresh context.

### P5: Mandatory Subagent Isolation

The following steps MUST run in isolated subagent contexts so their skill loads, review logic, and audit evidence do not pollute the orchestrator context:

- Step 4: `woos-product-prd-review-gate`
- Step 5R: `woos-ui-brief-review`
- Step 6: `woos-prd-consistency-audit`
- Step 7: `woos-version-integration-audit`

### P6: Fix Propagation (Global Sync)

When any review gate returns `REQUEST_CHANGES` and a fix is applied:

1. Identify all terms, enums, field names, or concepts that were modified
2. Grep ALL existing version documents (`docs/prd/<version>/`, `docs/design/<version>/`, `docs/product/`) for those terms
3. Update every occurrence to maintain consistency
4. If an upstream interface summary exists for a completed feature and the fix contradicts it, update the interface summary too

This rule applies regardless of which step triggered the fix. A single-file fix is never sufficient when the modified concept appears in other documents.

### P7: Upstream Interface Awareness

When Step 1.5 identifies `feeds` or `mutual` relationships, downstream features MUST receive upstream interface summaries as additional input in Steps 2, 3, 4, and 6. The orchestrator determines which summaries to pass based on the dependency graph — only direct dependencies, not transitive.

---

## Purpose

Transform one approved roadmap version into reviewed PRDs and interface summaries, with a user-controlled delivery checkpoint after each feature. This is **Stage 3** of the `woos-idea-to-design` flow.

Product defines **WHAT** and **WHY**. Engineering decides **HOW**.

## Feature ID Convention

Every designed feature gets a stable ordered feature ID:

```text
<feature-id> = <two-digit-order>-<feature-slug>
Example: 01-user-auth, 02-project-dashboard
```

Use `<feature-id>` in **all feature-specific document filenames** so the delivery order is visible from filenames. In Strict mode, assign order from the dependency-aware execution order in Step 1.5. In Standard/Lite mode, use `01-<feature-slug>`. Do not renumber after files are created.

## Project Root Requirement

All file paths (`docs/`) are relative to a project root directory which must be a git repository.

## Prerequisites

**Standard / Strict:**

- `docs/product/<project>-roadmap.md` exists
- Discovery human approval has passed
- The target version has been selected from the roadmap

**Lite:**

- An idea capture file exists from `woos-idea-capture` (`ideas/<slug>.md` for Quick Note, or `ideas/<slug>/00-idea-capture.md` for Guided Interview)
- Discovery and roadmap are **not** required for Lite — the idea capture file is the source of truth for scope
- Default `<version>` is `lite`; default `<feature-id>` is `01-<slug>` derived from the idea capture filename

## Modes

| Mode | When | Blocking Steps | Checkpoint |
|------|------|----------------|------------|
| **Lite** | Small scope, obvious, 1-2 days work | Requirements → PRD | After PRD |
| **Standard** | Single feature, moderate complexity | Requirements → PRD → PRD Review | After PRD Review |
| **Strict** | Multi-feature version, higher uncertainty, UX-heavy | Select Scope → Dependency Analysis → [per feature: Requirements → PRD → Review → UI → UI Review → Analyze → Interface Summary → Integration] | After each feature completes all gates |

---

## Steps — Strict Mode

The orchestrator runs per feature:

```text
Step 1:   Select Version Scope
Step 1.5: Feature Dependency Analysis (auto, Strict only)
  → For each feature (in dependency order):
      Steps 2–6.5 (Requirements → Interface Summary)
      Step 7 (incremental Integration, after 2nd+ feature)
      → ⭐ CHECKPOINT: "Should this feature be delivered to engineering now?"
          Yes → deliver to engineering, continue to next feature
          No  → continue to next feature, deliver later
  → After ALL features have completed their per-feature loop:
      Step 7-Final (full-doc integration audit across every feature)
      → ⭐ FINAL CHECKPOINT: any features not yet delivered → deliver now
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
| **Output** | ordered execution plan with feature IDs (inline, not a separate file) |

The orchestrator scans the roadmap features for shared entities:

1. **Extract shared signals** — identify mentions of shared data models, shared state, common APIs/endpoints, or explicit "depends on <feature-id>" references across features
2. **Classify relationships:**
   - `independent` — no shared entities, can run in any order
   - `feeds` — Feature A produces a concept that Feature B consumes (A before B)
   - `mutual` — features share a concept but neither strictly depends on the other
3. **Determine execution order:**
   - `independent` features: process in roadmap-listed order (arbitrary but deterministic)
   - `feeds` relationships: process upstream feature first
   - `mutual` relationships: process in roadmap-listed order, but flag for Step 7 integration focus

**Output format (stated before proceeding):**

```text
Execution order:
  1. 01-<feature-A> (independent)
  2. 02-<feature-B> (feeds: depends on 01-<feature-A>'s <shared-entity>)
  3. 03-<feature-C> (mutual with 02-<feature-B> — flagged for integration audit)

Interface pass-through:
  - 02-<feature-B> receives: 01-<feature-A> interface summary
  - 03-<feature-C> receives: 02-<feature-B> interface summary
```

**Advance when:** execution order, feature IDs, and interface pass-through plan are determined. No blocking — this step always produces a result.

**Skip when:** Standard or Lite mode (single feature, no dependency to analyze).

---

### Step 2: Requirement Contract

| | |
|---|---|
| **Skill** | `woos-requirement-contract` |
| **Input** | `docs/product/<project>-roadmap.md` § selected version |
| **Conditional input** | `docs/prd/<version>/<upstream-feature-id>-interface.md` for each upstream dependency (per Step 1.5 graph) |
| **Output** | `docs/prd/<version>/<feature-id>-requirements.md` |

**Advance when:** the requirements file exists, passes structural validation, and includes an explicit `P0/P1/P2` ranking with cut-line.

---

### Step 3: PRD Authoring

| | |
|---|---|
| **Skill** | `woos-prd-authoring` |
| **Input** | `docs/prd/<version>/<feature-id>-requirements.md` |
| **Conditional input** | `docs/prd/<version>/<upstream-feature-id>-interface.md` for each upstream dependency |
| **Output** | `docs/prd/<version>/<feature-id>.md` |

**Advance when:** the PRD file exists and proceeds to Step 4.

---

### Step 4: PRD Review Gate

| | |
|---|---|
| **Skill** | `woos-product-prd-review-gate` |
| **Execution** | isolated subagent |
| **Input** | `docs/prd/<version>/<feature-id>.md` + `docs/prd/<version>/<feature-id>-requirements.md` + `docs/product/<project>-architecture.md` |
| **Conditional input** | `docs/prd/<version>/<upstream-feature-id>-interface.md` for each upstream dependency |
| **Output** | `docs/reviews/<version>/<feature-id>-prd-review-rN.md` |

**Review loop:** `REQUEST_CHANGES` → fix PRD (apply P6: grep + sync all affected docs) → re-run review. Max 2 rounds before asking the user for direction.

---

### Step 5: UI Design Brief

| | |
|---|---|
| **Skill** | `woos-ui-design-brief` |
| **Input** | `docs/prd/<version>/<feature-id>.md` |
| **Output** | `docs/design/<version>/<feature-id>-ui-brief.md` |

**Trigger:** ask whether the feature has user-facing UI.

- `Yes` → run Step 5, then Step 5R
- `No` → skip Step 5 and Step 5R, continue to Step 6

---

### Step 5R: UI Brief Review Gate

| | |
|---|---|
| **Skill** | `woos-ui-brief-review` |
| **Execution** | isolated subagent |
| **Input** | `docs/design/<version>/<feature-id>-ui-brief.md` + `docs/prd/<version>/<feature-id>.md` |
| **Output** | `docs/reviews/<version>/<feature-id>-ui-review-rN.md` |

**Review loop:** `REQUEST_CHANGES` → fix UI brief → re-run review. Max 2 rounds before asking the user for direction.

---

### Step 6: Analyze Gate

| | |
|---|---|
| **Skill** | `woos-prd-consistency-audit` |
| **Execution** | isolated subagent |
| **Input** | `docs/prd/<version>/<feature-id>.md` + `docs/design/<version>/<feature-id>-ui-brief.md` (if exists) |
| **Conditional input** | `docs/prd/<version>/<upstream-feature-id>-interface.md` for each upstream dependency |
| **Output** | `docs/reviews/<version>/<feature-id>-analyze-report.md` |

**Advance when:** semantic review verdict is `PASS`.

Script extraction output alone does NOT complete Step 6. The final report must include the semantic-review sections required by `woos-prd-consistency-audit`, including `## Semantic Audit Verdict`.

**If `GAPS_FOUND`:**

- requirements gap (broken priority cut-line, missing/untestable story originating in the contract, missing ranking) → return to Step 2 (apply P6: global sync). Re-run Step 3 and Step 4 afterward.
- PRD gap → return to Step 3 (apply P6: global sync)
- UI gap → return to Step 5 (apply P6: global sync)

---

### Step 6.5: Interface Summary Extraction

| | |
|---|---|
| **Skill** | direct orchestrator step |
| **Trigger** | Strict mode, after Step 6 PASS |
| **Input** | `docs/prd/<version>/<feature-id>-requirements.md` + `docs/prd/<version>/<feature-id>.md` |
| **Output** | `docs/prd/<version>/<feature-id>-interface.md` |

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

### Step 7: Version Integration Gate

| | |
|---|---|
| **Skill** | `woos-version-integration-audit` |
| **Execution** | isolated subagent |
| **Input** | roadmap + architecture + all completed feature interface summaries, plus newest-feature full requirements/PRD/UI inputs on incremental runs (`--newest-feature`), or all full feature docs on the final run (`--final-run` + one `--feature` per audited feature) |
| **Output** | `docs/reviews/<version>/integration-report.md` (or `integration-report-after-<feature-id>.md` for incremental runs) |

**Trigger:** Strict mode with 2+ features. Runs **incrementally**:

- After the **2nd feature** completes Step 6.5 → first integration check (F1 + F2)
- After each subsequent feature completes Step 6.5 → incremental integration check
- After the **last feature's per-feature loop and checkpoint** complete → **Step 7-Final** (mandatory, see below)

**Results:**

- `PASS` → continue
- `CONFLICTS_FOUND` → fix before proceeding (apply P6: global sync)

**Skip when:** the version has only one feature.

---

### Step 7-Final: Full-Doc Integration Gate (Strict, 2+ features)

| | |
|---|---|
| **Skill** | `woos-version-integration-audit` |
| **Execution** | isolated subagent, MUST invoke `integration_gate.py` with `--final-run` plus one `--feature <feature-id>` for every audited feature |
| **Input** | roadmap + architecture + full requirements/PRD/UI for EVERY audited feature + all interface summaries |
| **Output** | `docs/reviews/<version>/integration-report.md` |

**Purpose:** The incremental Step 7 runs only compare the newest feature's full PRD against prior interface summaries. C1 (AC conflicts) and C2 (flow connectivity) can only be verified across **all full PRDs** of the version. This final pass is the only place that comparison happens.

**Trigger (mandatory):** After the last feature's per-feature CHECKPOINT, before any final delivery. The orchestrator MUST schedule this run; it is not optional and is not satisfied by the last incremental run.

**Results:**

- `PASS` → version design is closed; honor the final checkpoint for any undelivered features
- `CONFLICTS_FOUND` → fix the offending feature(s) and re-run Step 7-Final (apply P6: global sync). Per-feature loops do not re-open unless a fix requires PRD/UI changes in a specific feature.

**Skip when:** the version has only one feature (already skipped Step 7 too).

---

### ⭐ Checkpoint: Deliver to Engineering

After a feature passes all gates required for its mode, the orchestrator **pauses and asks the user:**

> "Feature <feature-id> design is complete. Deliver it to engineering now, or continue designing the next feature?"

- **Standard:** checkpoint happens after Step 4 (PRD Review).
- **Strict, first feature:** checkpoint happens after Step 6.5 (there is no cross-feature integration context yet).
- **Strict, second and later features:** checkpoint happens after Step 7.

- **Yes** → deliver PRD + supporting docs to engineering, continue to next feature
- **No** → continue to next feature, batch deliver later

This checkpoint allows the user to decide the cadence of delivery without the orchestrator making assumptions about parallelism.

---

## Steps — Standard Mode

Single feature, no UI/analyze/integration path.

| Step | Skill | Output |
|------|-------|--------|
| S1 | `woos-requirement-contract` | `docs/prd/<version>/<feature-id>-requirements.md` |
| S2 | `woos-prd-authoring` | `docs/prd/<version>/<feature-id>.md` |
| S3 | `woos-product-prd-review-gate` | `docs/reviews/<version>/<feature-id>-prd-review-rN.md` |

PRD Review PASS → ⭐ checkpoint: deliver to engineering.

---

## Steps — Lite Mode

Lite skips review gates and does not require a roadmap. The idea capture file is the input source.

**Input resolution:**

- Idea capture file: `ideas/<slug>.md` (Quick Note) or `ideas/<slug>/00-idea-capture.md` (Guided Interview)
- `<version>` = `lite`
- `<feature-id>` = `01-<slug>` (slug from idea capture filename)

**Steps:**

1. **Requirements (brief)** — run `woos-requirement-contract` in **Lite mode**: load the idea capture file in place of the roadmap; produce a brief `## Priority Ranking` (P0/P1 only is fine for Lite). Output: `docs/prd/lite/01-<slug>-requirements.md`.
2. **PRD (focused)** — run `woos-prd-authoring`: FRs + ACs, no extensive edge cases. Output: `docs/prd/lite/01-<slug>.md`.

PRD written → ⭐ deliver to engineering (no checkpoint needed, single trivial feature).

## DCR — Design Change Request

DCRs are a feedback mechanism from engineering back to product.

When engineering sends `docs/feedback/<version>/<feature-id>-dcr-<NNN>.md` (one file per DCR; multiple DCRs may exist for the same feature, numbered in order of creation):

1. Read the DCR
2. Assess impact
3. Small change → update PRD directly, notify engineering
4. Large change → return to Step 3 or Step 5, re-run affected gates

## Deliverable to Engineering

When the checkpoint delivers a feature, the coding agent receives:

**Required:**
- PRD: `docs/prd/<version>/<feature-id>.md`
- Architecture: `docs/product/<project>-architecture.md`
- Roadmap: `docs/product/<project>-roadmap.md`

**Additional when produced by product flow (expected in Strict mode, optional otherwise):**
- Interface summary: `docs/prd/<version>/<feature-id>-interface.md`
- UI brief: `docs/design/<version>/<feature-id>-ui-brief.md` (if feature has UI)
- Upstream interfaces: `docs/prd/<version>/<upstream-feature-id>-interface.md` (if applicable)

The coding agent is responsible for task decomposition, ordering, and implementation decisions.

---

## Failure Handling

| Situation | Action |
|-----------|--------|
| Roadmap missing | Return to `woos-product-discovery` |
| Review loop hits max rounds | Ask the user for direction |
| Scope too large | Split into multiple features |
| Output file missing or stub | Re-run the same declared step |
| Script-based audit fails | Fix the inputs or parser bug, then re-run |
