---
name: feature-design-flow
description: "Stage 2 of idea-to-delivery: take a version from the product roadmap and produce PRD + technical design + build handoff (with sharding) for the coding agent. Includes persona switching (PM/Architect/QA), analyze gate, and decision log. Runs once per version."
version: 2.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [feature, design, prd, handoff, review-gate, persona, analyze, sharding]
    stage: 2
    flow: idea-to-delivery-v2
---

# Feature Design Flow

## Purpose

Transform one version from the product roadmap into a build-ready handoff file. This is **Stage 2** of the idea-to-delivery flow. Run once per roadmap version (V1, V2, ...).

**Agent:** research (with internal persona switching)

## Project Root Requirement

**CRITICAL:** All file paths in this skill (`.hep/`, `docs/`, `ideas/`) are relative to a **project root directory**. The project root MUST be a real git repository (e.g. `~/code/my-project/`).

**DO NOT** write files to the kanban scratch workspace. The scratch workspace is temporary and will be garbage-collected after task completion.

If running via kanban:
1. If the task has a `workspace_path` pointing to a git repo, use that.
2. If the task is in scratch mode, **clone or create the target repo first**, then write all files there.
3. The project root must contain `.hep/` and `docs/` — create them if they don't exist.
4. Ask the user for the project directory if not specified.

## When to Use

- User says "start V1" / "design this feature" / "ready to build X"
- Product roadmap exists and a version has been selected

## Prerequisites

- `docs/product/<project>-roadmap.md` exists (from `product-discovery` or user-provided)
- `.hep/constitution.md` exists

## Modes

| Mode | When | Gate Reviews | Handoff Fields |
|------|------|-------------|----------------|
| **Standard** | Default. Multi-file, cross-component, design choices matter | PRD Review + Design Review + Analyze Gate | Full (13 sections + shards) |
| **Lite** | Small scope, no architecture changes, low risk | None (self-check only) | 4 fields: Mission, Build Tasks, AC, Verification |

## 🆕 Persona Switching

Standard mode uses explicit persona switching to ensure clean separation of concerns:

```
[PM Mode] Steps 1–4
  Mindset: user value, acceptance criteria, priorities, non-goals
  ↓ PRD Review PASS
[Architect Mode] Steps 5–6
  Mindset: performance, scalability, security, technical tradeoffs
  ↓ Design Review PASS
[QA Mode] Steps 7–10
  Mindset: consistency, coverage, testability, completeness
```

**When switching persona:**
- Clear the previous persona's value judgments
- Adopt the new persona's priority framework
- Do NOT carry PM's "user-first" bias into Architect mode
- Do NOT carry Architect's "elegance-first" bias into QA mode

## Steps — Standard Mode

### Step 1: Select Version Scope

**[PM Mode]**

Read `docs/product/<project>-roadmap.md`, extract the target version. Confirm with user:
- Feature list and boundaries
- Non-goals
- Success metrics

### Step 2: Requirement Contract

**[PM Mode]**

**Skill:** `woos-requirement-contract`

Produce structured requirement contract:
- Goals and constraints
- Acceptance criteria (machine-checkable)
- Non-goals
- Risk assumptions and unknowns

### Step 3: PRD Authoring

**[PM Mode]**

**Skill:** `woos-prd-authoring`

Write full PRD:
- User stories with acceptance criteria
- Functional and non-functional requirements
- Edge cases and error handling
- Migration/rollback considerations

**Output:** `docs/prd/<feature>.md`

### Step 4: PRD Review Gate

**[PM Mode → Checkpoint]**

**Skill:** `woos-prd-review-gate`

Independent review using product-planner + architect:
- Uses `woos-review-context` to track cumulative findings
- Uses `woos-agent-decision` for reviewer conflicts
- **PASS** → 🆕 checkpoint (optional), then Step 5
- **REQUEST_CHANGES** → return to Step 3 with feedback
- 3 rounds without convergence → `woos-human-handoff`

🆕 **Checkpoint:** If handoff frontmatter has `checkpoints: [prd-passed]`, pause here and present PRD summary to user for confirmation before entering Architect mode.

### Step 5: Feature Design

**[Architect Mode]** — 🆕 Clear PM mindset before starting.

**Skill:** `woos-feature-design`

Write technical design:
- Architecture and component interaction
- Data model and storage
- API contracts (if applicable)
- Security considerations
- Rollout/rollback plan
- Constitution deviations documented with ADR

**Output:** `docs/design/<feature>.md`

**If API endpoints defined:** invoke API design review patterns for REST/GraphQL conventions.

### Step 6: Design Review Gate

**[Architect Mode]**

**Skill:** `woos-design-review-gate`

Independent review using architect:
- Uses `woos-review-context` to track cumulative findings
- **PASS** → Step 7
- **REQUEST_CHANGES** → return to Step 5 with feedback
- 3 rounds without convergence → `woos-human-handoff`

### Step 7: 🆕 Analyze Gate

**[QA Mode]** — 🆕 Clear Architect mindset before starting.

Cross-artifact consistency pre-check. Run BEFORE packaging the handoff.

| Check | What | Pass Condition |
|-------|------|----------------|
| A1: Requirement Coverage | Every Requirement maps to ≥1 Build Task | 100% coverage |
| A2: AC Verifiability | Every AC maps to Verification Plan step | 100% mappable |
| A3: Architecture Consistency | Architecture components cover Data Model + API | No orphan components |
| A4: Data Flow Completeness | Data Model entities covered by API CRUD | No unused entities |
| A5: Non-goal Alignment | Build Tasks don't include Non-goals | Zero conflicts |
| A6: Constitution Compliance | Design respects Constitution constraints | No violations |

**Output:** `docs/handoff/<feature>-vN-analyze-report.md`

**Results:**
- **PASS** → all checks green → proceed to Step 8
- **GAPS_FOUND** → report includes specific gaps with references → return to relevant step (Step 3 for requirement gaps, Step 5 for design gaps)

### Step 8: Build Handoff Packaging

**[QA Mode]**

**Skill:** `build-handoff`

Synthesize PRD + Design into a single handoff file that a fresh coding agent can work from independently.

**Output:** `docs/handoff/<feature>-vN.md`

Handoff contains:
1. Spec versioning (YAML frontmatter: `spec-version`, `based-on`, `constitution-ref`, 🆕 `checkpoints`, 🆕 `decision-log-ref`)
2. Mission Statement
3. Context (from roadmap)
4. Requirements (AC, non-goals)
5. Architecture (technical design summary)
6. Data Model (if applicable)
7. API Contracts (if applicable)
8. Build Tasks (with `[ADDED]`/`[MODIFIED]`/`[REMOVED]` delta annotations)
9. Verification Plan
10. Security Considerations
11. Constitution Reference
12. DCR Protocol (how to report design issues back)
13. 🆕 Decision Log (key decisions + rationale + alternatives)

### Step 9: 🆕 Handoff Sharding

**[QA Mode]**

Split the handoff into focused shard files for Stage 3's story-level execution:

```text
docs/handoff/<feature>-vN-shards/
├── 01-context.md          # Project background + constraints + Constitution summary
├── 02-requirements.md     # Requirements + AC + non-goals
├── 03-architecture.md     # Technical design + component diagram
├── 04-data-model.md       # Data model + schema
├── 05-api-contracts.md    # API definitions + request/response
├── 06-build-tasks.md      # Task list + delta annotations
└── 07-verification.md     # Verification plan + security considerations
```

Each shard is self-contained (can be read without the full handoff).
Shards reference each other when cross-cutting (e.g., 03-architecture references 04-data-model).

**Skip sharding in Lite mode.**

### Step 10: Handoff Readiness Check

**[QA Mode]**

8-item checklist:
- [ ] All AC are machine-checkable
- [ ] Build Tasks map 1:1 to AC
- [ ] No unresolved design decisions remain
- [ ] Constitution reference is correct (if exists)
- [ ] Data model changes have migration plan
- [ ] API contracts have error handling
- [ ] Security considerations addressed
- [ ] DCR protocol is specified
- [ ] 🆕 Decision Log is populated (at least 1 entry)
- [ ] 🆕 Shards are generated and internally consistent

**PASS** → handoff ready for `engineering-workflow`
**FAIL** → return to Step 8 with gaps

### Step 11: 🆕 Decision Log Append

Append Stage 2 decisions to the project Decision Log (in roadmap):

| # | Decision | Rationale | Alternatives |
|---|----------|-----------|-------------|
| D+1 | (e.g. REST over gRPC) | (e.g. team familiarity) | (e.g. gRPC — better perf, higher learning cost) |
| D+2 | ... | ... | ... |

Source from: PRD tradeoffs, architecture choices, scope decisions, Constitution deviations.

## Steps — Lite Mode

| Step | What |
|------|------|
| L1 | Quick description: one-sentence Mission |
| L2 | Build Tasks: numbered list of small objectives |
| L3 | Acceptance Criteria: how to verify each task |
| L4 | Verification: how to confirm completion |
| L5 | Package into Lite handoff (4 fields) using `build-handoff` |

No review gates, no persona switching, no analyze gate, no sharding, no checkpoints. Self-check only.

## DCR Reception

When coding agent sends a Design Change Request (`docs/feedback/<feature>-dcr.md`):

1. Read DCR file (🆕 includes Decision Log reference — which decision led to the issue)
2. Assess impact:
   - **Small change**: Update handoff + affected shards directly, notify coding agent to continue
   - **Large change**: Return to appropriate step (Step 3 for PRD issues, Step 5 for design issues)
3. Update `woos-review-context` with DCR findings
4. 🆕 If DCR challenges a logged decision, update Decision Log with new entry (append, never delete)

## 🆕 Checkpoint Control

Standard mode supports optional checkpoints. Controlled by handoff frontmatter:

```yaml
checkpoints:
  - prd-passed      # Pause after PRD Review PASS
  - handoff-ready   # Pause after Handoff Readiness PASS
```

If `checkpoints: []` or field absent → fully autonomous (no pauses).

At each checkpoint:
1. Present summary of current state to user
2. Wait for confirmation
3. If user requests changes → return to relevant step
4. If user confirms → proceed

## Handoff to Next Stage

On completion:
- Handoff file at `docs/handoff/<feature>-vN.md`
- 🆕 Shards at `docs/handoff/<feature>-vN-shards/`
- 🆕 Analyze report at `docs/handoff/<feature>-vN-analyze-report.md`
- Tell user: "Handoff ready. Coding agent can pick up via `engineering-workflow`."
- If using kanban: create task assigned to `coding` with handoff file path

## File Layout

```text
<project-root>/
├── .hep/
│   ├── constitution.md
│   ├── runs/<run_id>/run-manifest.yaml
│   └── review-context/<run_id>.yaml
├── docs/
│   ├── product/<project>-roadmap.md          ← input (from Stage 1, with Decision Log)
│   ├── prd/<feature>.md                       ← Step 3 output
│   ├── design/<feature>.md                    ← Step 5 output
│   ├── handoff/
│   │   ├── <feature>-vN.md                   ← main output
│   │   ├── <feature>-vN-analyze-report.md    ← 🆕 Step 7 output
│   │   └── <feature>-vN-shards/              ← 🆕 Step 9 output
│   │       ├── 01-context.md
│   │       ├── 02-requirements.md
│   │       ├── 03-architecture.md
│   │       ├── 04-data-model.md
│   │       ├── 05-api-contracts.md
│   │       ├── 06-build-tasks.md
│   │       └── 07-verification.md
│   └── feedback/<feature>-dcr.md             ← DCR input (from Stage 3)
```

## Failure Handling

| Situation | Action |
|-----------|--------|
| Roadmap missing | Redirect to `product-discovery` first |
| Constitution missing | Create from codebase or ask user |
| Review loops 3x | Escalate to human via `woos-human-handoff` |
| Scope too large for one handoff | Split into multiple handoffs; one per sub-feature |
| Reviewer conflict | `woos-agent-decision` resolves |
| 🆕 Analyze Gate finds gaps | Return to relevant step with specific gap references |
| 🆕 Persona bleed detected | Explicit reset: re-read persona definition, clear prior biases |

## Cross-Stage Skills Used

| Skill | Purpose |
|-------|---------|
| `woos-requirement-contract` | Step 2 |
| `woos-prd-authoring` | Step 3 |
| `woos-prd-review-gate` | Step 4 |
| `woos-feature-design` | Step 5 |
| `woos-design-review-gate` | Step 6 |
| `build-handoff` | Step 8 |
| `woos-review-context` | Cross-gate findings |
| `woos-agent-decision` | Reviewer conflict resolution |
| `woos-human-handoff` | Escalation |
