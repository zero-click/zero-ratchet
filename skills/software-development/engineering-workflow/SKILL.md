---
name: engineering-workflow
description: "Stage 3 of idea-to-delivery: receive a build handoff (with shards), decompose into stories, execute story-by-story with TDD, verify architecture conformance, and submit PR. Replaces woos-development-workflow."
version: 2.1.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [engineering, implementation, tdd, review, pr, stories, sharding]
    stage: 3
    flow: woos-idea-to-delivery-v2
---

# Engineering Workflow

## Purpose

Receive a build handoff from `woos-product-design-flow` (Stage 2), decompose it into independent stories, and execute each story with TDD, verification, and review. This is **Stage 3** of the woos-idea-to-delivery flow.

**Agent:** coding

## Project Root Requirement

**CRITICAL:** All file paths in this skill (`.hep/`, `docs/`, `src/`) are relative to a **project root directory**. The project root MUST be a real git repository (e.g. `~/code/my-project/`).

**DO NOT** write files to the kanban scratch workspace. The scratch workspace is temporary and will be garbage-collected after task completion.

If running via kanban:
1. If the task has a `workspace_path` pointing to a git repo, use that.
2. If the task is in scratch mode, **clone or create the target repo first**, then write all files there.
3. All code changes, tests, and commits happen inside the project repo.
4. The handoff file MUST be read from the project repo's `docs/handoff/` directory.

## When to Use

- A handoff file exists at `docs/handoff/<feature>-vN.md`
- Task assigned to coding agent via kanban or direct instruction

## Modes

| Mode | Determined by | Gate Reviews | Story Execution |
|------|--------------|-------------|-----------------|
| **Standard** | Handoff has 13 sections (full handoff) | All gates | Story-by-story |
| **Lite** | Handoff has 4 sections (Lite handoff) | Minimal | Flat execution |

Mode is **read from the handoff file**, not chosen here.

## Steps — Standard Mode

### Step 1: Run Initialization

**Skill:** `woos-run-orchestrator`

- Initialize or resume run: `.hep/runs/<run_id>/run-manifest.yaml`
- If handoff references a run_id from Stage 2, continue that run
- If no run_id, create new and note in handoff

**Gate:** Run MUST have a valid run_id before proceeding. BLOCKED without it.

### Step 2: Git Preparation

- Read branch strategy from handoff or constitution
- Create feature branch: `feature/<feature-slug>` or as specified
- If constitution specifies worktree policy, follow it

### Step 3: 🆕 Story Generation

**Skill:** `writing-plans`

Parse handoff and decompose into independent stories. Each story is a self-contained unit of work.

Read handoff from `docs/handoff/<feature>-vN.md`. If shards exist at `docs/handoff/<feature>-vN-shards/`, use them for focused context.

**Story file format:**

```markdown
# Story <NNN>: <task name>

## Context Shards
- 03-architecture.md#component-auth
- 04-data-model.md#user-table
- 05-api-contracts.md#POST-/auth/login

## Build Tasks
- [ ] Implement user model
- [ ] Implement login endpoint

## Acceptance Criteria
- AC-01: ...
- AC-02: ...

## Verification
- Unit test: ...
- Integration test: ...

## Dependencies
- None (or: depends on story-NNN)

## Status: pending
```

**Output:** `.hep/runs/<run_id>/stories/story-001.md`, `story-002.md`, ...

**Rules:**
- Each story references specific shard sections (not entire shards)
- Stories have clear dependencies (DAG order)
- Each story covers 1-3 related Build Tasks
- Stories are independently verifiable

### Step 4: 🆕 Context Loading

Before executing each story, load ONLY the referenced shard sections:
- Read `docs/handoff/<feature>-vN-shards/<shard-name>.md`
- Extract the referenced section (e.g., `#component-auth`)
- Do NOT load the entire handoff or all shards

This keeps context lean and focused.

### Step 5: 🆕 Story-by-Story Execution Loop

Execute stories in dependency order. For **each story**:

#### 5.1 TDD

**Skill:** `test-driven-development`

1. **RED**: Write failing test for the story's behavior
2. **GREEN**: Implement minimum code to pass
3. **REFACTOR**: Clean up while keeping tests green

If RED-GREEN cycle stalls (2+ consecutive failed attempts):
→ Activate `woos-systematic-debugging` before further attempts

#### 5.2 Implement

- Follow Build Tasks within the story
- Respect delta annotations: `[ADDED]` new, `[MODIFIED]` change, `[REMOVED]` delete
- Constitution deviations → require ADR (flag immediately)
- If design issue discovered → write DCR (see DCR section), do NOT improvise

#### 5.3 Verify

- Run tests for the current story
- Run lint / type check
- Verify story-level AC

#### 5.4 🆕 Story Verification Gate

**Per-story AC check:**
- Map story's AC to executable checks
- **PASS** → mark story `status: completed`, continue to next story
- **FAIL (1st)** → fix and retry
- **FAIL (2nd)** → activate `woos-systematic-debugging`
- **FAIL (3rd)** → 🆕 mark story `status: blocked`, continue with other stories

#### 5.5 🆕 Failure Isolation

- A blocked story does NOT block independent stories
- Blocked stories are retried after all other stories complete
- If still blocked → write DCR with context

#### 5.6 🆕 Checkpoint (Optional)

If handoff frontmatter has `checkpoints: [per-story]`:
- Pause after each story completion
- Present story summary to user
- Wait for confirmation before next story

If `checkpoints: [all-stories-done]` or absent → no per-story pauses.

### Step 6: Executable Acceptance Gate

**Skill:** `woos-executable-acceptance-gate`

After ALL stories complete (or remaining are blocked):
- Map ALL handoff AC to executable checks
- **PASS** → Step 7
- **REQUEST_CHANGES** → identify which story needs rework, return to Step 5

### Step 7: Deviation Control

**Skill:** `woos-deviation-control-gate`

Compare implementation against handoff:
- Unresolved deviations block progression
- Intentional deviations require updated handoff + rationale
- 🆕 Cross-reference with Decision Log: if deviation contradicts a logged decision, flag for DCR
- **PASS** → Step 8
- **REQUEST_CHANGES** → return to Step 5 (specific story)

### Step 8: 🆕 Requirement Traceability Gate

**Skill:** built-in (no separate skill needed)

Compare implementation against **PRD** (not just handoff). This is the only step that traces from original requirements all the way to code and tests.

**Procedure:**

1. Read PRD from `docs/prd/<feature>.md`
2. Read design from `docs/design/<feature>.md`
3. For **each PRD User Story and AC**, trace the full chain:

| PRD AC | Design Spec | Code | Test | Status |
|--------|-------------|------|------|--------|
| AC-4.5.1 | §API assign endpoint | routes/tasks.py:assign_task() | test_story003:test_assign_task | ✅ |
| AC-6.2 | §Data model completed_at | N/A (uses updated_at) | N/A | ⚠️ Deviated |

4. Classify each AC:
   - **✅ Aligned** — PRD, design, code, test all match
   - **⚠️ Deviated** — implemented differently (record rationale)
   - **❌ Missing** — AC not implemented or not tested
   - **🆕 Added** — implemented but not in PRD (extra scope)

5. Write output to `docs/handoff/<feature>-traceability.md`:
   - Per-AC traceability table
   - Data model deviations (field name changes, type changes, missing fields)
   - API contract deviations (endpoint path, request/response shape, error codes)
   - State machine deviations (added/removed states, changed transitions)
   - Summary: total ACs, aligned count, deviated count, missing count

**Gate rules:**
- **PASS** — all ACs are ✅ or ⚠️ with documented rationale, zero ❌
- **REQUEST_CHANGES** — any ❌ (missing AC), or ⚠️ without rationale
- Return to Step 5 with specific AC gaps

**Why this step exists:**
- Step 6 (Executable Acceptance) checks handoff ACs are testable
- Step 7 (Deviation Control) checks implementation vs handoff (design layer)
- **Step 8 traces from PRD (requirements layer) through design to code and tests**
- Catches "meets design but not requirements" and "PRD says X, code does Y" issues
- Without this step, design deviations from PRD are invisible

### Step 9: 🆕 Architecture Conformance Gate

**Skill:** `woos-design-review-gate`

Verify that implementation conforms to the architecture design:
- Component boundaries respected
- Data model matches design
- API contracts implemented as specified
- Security considerations addressed
- No ad-hoc architectural decisions (or logged as Decision Log entry)

**PASS** → Step 10
**REQUEST_CHANGES** → return to Step 5 with specific violations

This catches "works but doesn't match the design" issues that code review alone misses.

### Step 10: Code Review

**Skill:** `woos-code-review-gate`

Independent review:
- Dispatch `code-reviewer` in fresh context (no self-review)
- If scope is security-sensitive: also dispatch `security-reviewer`
- Uses `woos-review-context` to load cumulative findings
- Uses `woos-agent-decision` for reviewer conflicts
- Enforces spec alignment
- **PASS** → Step 11
- **REQUEST_CHANGES** → return to Step 5 with feedback (specific stories)
- 3 rounds without convergence → `woos-human-handoff`

### Step 11: 🆕 Verification Before Completion

Mandatory pre-PR gate. ALL of the following must pass:

- [ ] All tests pass (unit + integration + e2e as applicable)
- [ ] Lint is clean (zero warnings)
- [ ] Type check passes (if applicable)
- [ ] All stories are `completed` (none `blocked` without DCR)
- [ ] Documentation updated (README, API docs, if applicable)
- [ ] No TODO/FIXME/HACK comments without linked issues
- [ ] Constitution compliance verified

**PASS** → Step 12
**FAIL** → return to Step 5 with specific issues

### Step 12: PR Readiness

**Skill:** `woos-pr-readiness`

- Diff review and traceability matrix
- Conventional commit messages
- PR description with:
  - Summary of stories completed
  - Test plan
  - 🆕 Decision Log changes (if any)
  - 🆕 Blocked stories (if any, with DCR references)
- Create PR via `gh pr create`

### Step 13: Workflow Memory Update

**Skill:** `woos-workflow-memory`

Record for future runs:
- Failures encountered and how they were resolved
- Rework causes
- Whether DCR was triggered and outcome
- Patterns worth reusing
- 🆕 Story decomposition quality (too granular? too broad?)
- 🆕 Shard usefulness (which shards were actually referenced)

## Steps — Lite Mode

| Step | What | Skill |
|------|------|-------|
| L1 | Parse handoff (4 fields) | built-in |
| L2 | Implement tasks directly | built-in |
| L3 | Verify (basic test + lint) | built-in |
| L4 | Self-review | built-in (no independent dispatch) |
| L5 | Create PR | `woos-pr-readiness` |

No story decomposition, no deviation control, no executable acceptance gate, no architecture conformance, no verification before completion.

## DCR (Design Change Request)

**Trigger:** At any step, if a design issue is discovered that cannot be resolved within scope.

**Action:**
1. Write `docs/feedback/<feature>-dcr.md`:
   ```markdown
   # DCR: <Issue Title>

   ## Issue Description
   (What's wrong with the current design)

   ## Impact Scope
   (Which Build Tasks / AC / Stories are affected)

   ## 🆕 Decision Log Reference
   (Which logged decision led to this issue, e.g. "D3: chose SQLite — but concurrent writes exceed limits")

   ## Proposed Resolution
   (Suggested fix)

   ## Priority
   (blocking / non-blocking)
   ```
2. Stop work on affected stories
3. Notify research agent (via kanban comment or direct message)
4. Continue with unaffected stories if possible

**Research agent handles the DCR** and either:
- Updates handoff + affected shards directly (small change) → coding agent re-reads and continues
- Returns to Stage 2 for full re-design (large change)

## Failure Handling

| Situation | Action |
|-----------|--------|
| Handoff file missing or invalid | BLOCKED — report to research agent |
| Run_id unavailable | Create new run, note in handoff |
| Single story fails 3x | Mark BLOCKED, continue others |
| Build/test fails 2x (within story) | `woos-systematic-debugging` |
| Review fails 3x | `woos-human-handoff` escalation |
| Design issue found | DCR → back to research (Stage 2) |
| Overall timeout | `woos-failure-state-machine` (retry → degrade → escalate) |
| Required skill unavailable | BLOCKED — report which skill is missing |
| 🆕 All stories blocked | `woos-human-handoff` — fundamental design issue likely |

## Gate Status Model

All gates use binary outcomes:
- **PASS** — proceed to next step
- **REQUEST_CHANGES** — return to prior step with concrete feedback
- **BLOCKED** — external dependency missing, cannot proceed

Notes and observations are recorded in `woos-review-context` but do not affect gate state.

## 🆕 Checkpoint Control

Checkpoints are read from handoff YAML frontmatter:

```yaml
checkpoints:
  - per-story          # Pause after each story (high-risk features)
  # - all-stories-done  # Pause after all stories (default)
```

- `per-story`: pause after every story completion, present summary to user
- `all-stories-done` or absent: no per-story pauses
- Checkpoints are **advisory** — coding agent pauses and signals, human responds to continue

## File Layout

```text
<project-root>/
├── .hep/
│   ├── constitution.md
│   ├── runs/<run_id>/
│   │   ├── run-manifest.yaml
│   │   └── stories/                        ← 🆕 Story files
│   │       ├── story-001.md
│   │       ├── story-002.md
│   │       └── ...
│   └── review-context/<run_id>.yaml
├── docs/
│   ├── handoff/
│   │   ├── <feature>-vN.md                 ← input (from Stage 2)
│   │   └── <feature>-vN-shards/            ← 🆕 input (from Stage 2)
│   │       ├── 01-context.md
│   │       ├── 02-requirements.md
│   │       ├── 03-architecture.md
│   │       ├── 04-data-model.md
│   │       ├── 05-api-contracts.md
│   │       ├── 06-build-tasks.md
│   │       └── 07-verification.md
│   └── feedback/<feature>-dcr.md           ← output (DCR to Stage 2)
└── (implementation files)
```

## 🆕 Step Completion Rule (MANDATORY)

**After completing ANY step (1-11), you MUST:**

1. Update `run-manifest.yaml` — mark the step as `completed` in a `steps` section
2. State: **"Step N: <name> — DONE ✅. Next: Step N+1: <name>"**
3. **Do NOT proceed to the next step** until the current step's work is confirmed complete
4. Run-manifest serves as the authoritative record of which steps are done

**Purpose:** Prevent premature termination. The workflow has 13 steps — completing Stories (Step 5) is NOT the end. Steps 6-13 are gates that MUST run before PR.

**Run-manifest `steps` format:**

```yaml
steps:
  step-1-init: completed
  step-2-git: completed
  step-3-stories: completed
  step-4-context: completed
  step-5-execution: completed
  step-6-acceptance: pending
  step-7-deviation: pending
  step-8-traceability: pending
  step-9-architecture: pending
  step-10-codereview: pending
  step-11-verification: pending
  step-12-pr: pending
  step-13-memory: pending
```

This rule applies regardless of execution mode (kanban, direct, manual). Human-in-the-loop or agent — no step skipping.

## Cross-Stage Skills Used

| Skill | Step |
|-------|------|
| `woos-run-orchestrator` | Step 1 |
| `writing-plans` | 🆕 Step 3 (Story Generation) |
| `test-driven-development` | Step 5.1 |
| `woos-executable-acceptance-gate` | Step 6 |
| `woos-deviation-control-gate` | Step 7 |
| built-in (traceability procedure) | 🆕 Step 8 (Requirement Traceability) |
| `woos-design-review-gate` | Step 9 (Architecture Conformance) |
| `woos-code-review-gate` | Step 10 |
| `woos-pr-readiness` | Step 12 |
| `woos-workflow-memory` | Step 13 |
| `woos-review-context` | Cross-gate |
| `woos-agent-decision` | Reviewer conflicts |
| `woos-human-handoff` | Escalation |
| `woos-failure-state-machine` | Timeout/cascade |
| `woos-systematic-debugging` | Repeated failures |
