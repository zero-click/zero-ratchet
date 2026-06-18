# Product Design Workflow — Step × Knowledge Map

## Architecture

```
orchestrator (thin state machine)
  │
  ├── dispatch sub-agent (persona + 1 methodology/template)
  │     └── produces artifact
  │
  ├── dispatch review sub-agent (rubric)
  │     └── produces findings
  │
  └── next step...
```

Each work step runs as an independent sub-agent with focused knowledge injected (max 2 files).
The orchestrator only tracks: current step, output file paths, pass/fail status.

---

## Stage 1: `woos-product-discovery` (per project)

| Step | Name | Sub-agent? | Persona | Output | BMAD Knowledge |
|------|------|:----------:|---------|--------|----------------|
| 1 | Idea Capture | ✅ | analyst | `ideas/<slug>/00-idea-capture.md` | `personas/analyst.toml`<br>`templates/brief-template.md` |
| 2 | Problem Validation | ✅ | analyst | ↑ appends `## Problem Validation` (PROCEED/PIVOT/PARK) | `personas/analyst.toml`<br>`frameworks/customer-pain-points.md` |
| 3 | Research & Validation | ✅ | analyst | `docs/research/<topic>.md` | `frameworks/market-research.md`<br>`frameworks/competitive-analysis.md` |
| 4 | Run Initialization | ❌ orchestrator | — | `.ratchet/runs/<run_id>/run-manifest.yaml` | _(none)_ |
| 5 | Product Vision & Roadmap | ✅ | pm | `docs/product/<project>-roadmap.md` | `personas/pm.toml`<br>`frameworks/create-prd.md` |
| 5R | Roadmap Review | ✅ | product-strategist | `docs/reviews/<project>-roadmap-review-rN.md` | `frameworks/validate-prd.md`<br>`templates/prd-validation-checklist.md` |
| 6 | System Architecture | ✅ | architect | `docs/product/<project>-architecture.md` | `personas/architect.toml`<br>`frameworks/create-architecture.md` |
| 6R | Architecture Review | ✅ | system-architect | `docs/reviews/<project>-architecture-review-rN.md` | `frameworks/architecture-validation.md` |
| 7 | Decision Log | ❌ orchestrator | — | `docs/product/<project>-roadmap.md` → appends `## Decision Log` | _(none)_ |

**Stage 1 final deliverables:**
- `docs/product/<project>-roadmap.md` — product vision + user personas + V1/V2/V3 roadmap + decision log
- `docs/product/<project>-architecture.md` — system architecture overview

---

## Stage 2: `woos-product-design-flow`

### Design Principles

1. **PRD is the source of truth.** Coding agents receive PRD + interface summaries directly. No intermediate "handoff" translation layer.
2. **Per-feature completion.** Each feature completes its full design pipeline independently. After each feature finishes, the orchestrator pauses to ask whether engineering should start on it.
3. **Sequential execution.** Features are designed and built one at a time (no parallel development).

### Feature ID Convention

Every designed feature gets a stable ordered feature ID:

```text
<feature-id> = <two-digit-order>-<feature-slug>
Example: 01-user-auth, 02-project-dashboard
```

Use the feature ID in **all feature-specific document filenames** so the delivery order is visible from filenames. In Strict mode, assign order from the dependency-aware execution order in Step 1.5. In Standard/Lite mode, use `01-<feature-slug>`. Do not renumber after files are created.

### Three Modes

| Mode | When | Steps | Reviews |
|------|------|-------|---------|
| **Lite** | Small scope, obvious, 1-2 days | PRD | None |
| **Standard** | Single feature, moderate complexity | PRD → PRD Review | 1 (PRD) |
| **Strict** | Multi-feature version, high uncertainty | Full: PRD → Review → UI → Review → Analyze → Integration | All |

### Strict Mode (full pipeline, per version)

```
Step 1: Select Version → extract feature list
  → For each feature (in dependency order):
      Steps 2–5 (PRD → Analyze Gate)
      → Interface Summary extraction
      → Integration Gate (after 2nd+ feature)
      → ⭐ Feature design complete
      → CHECKPOINT: "Should this feature be delivered to engineering now?"
          Yes → engineering starts, product continues next feature
          No  → continue to next feature, batch deliver later
```

| Step | Name | Sub-agent? | Persona | Output |
|------|------|:----------:|---------|--------|
| 1 | Select Version Scope | ❌ orchestrator | — | _(version + feature list)_ |
| 1.5 | Feature Dependency Analysis | ❌ orchestrator | — | _(execution order + feature IDs)_ |
| 2 | PRD Authoring | ✅ | pm | `docs/prd/<version>/<feature-id>.md` |
| 3 | PRD Review | ✅ | prd-reviewer (`woos-product-prd-review-gate`) | `docs/reviews/<version>/<feature-id>-prd-review-rN.md` |
| 4 | UI Design Brief (opt-in) | ✅ | ux-designer | `docs/design/<version>/<feature-id>-ui-brief.md` |
| 4R | UI Brief Review | ✅ | ux-reviewer | `docs/reviews/<version>/<feature-id>-ui-review-rN.md` |
| 5 | Analyze Gate | ✅ | qa | `docs/reviews/<version>/<feature-id>-analyze-report.md` |
| 5.5 | Interface Summary | ❌ orchestrator | — | `docs/prd/<version>/<feature-id>-interface.md` |
| 6 | Integration Gate | ✅ | pm | `docs/reviews/<version>/integration-report.md` |
| | **⭐ CHECKPOINT: deliver to engineering?** | | | |

**Step 4 trigger:** Orchestrator asks user "Does this feature have UI?" — Yes → run, No → skip 4+4R.
**Step 6 trigger:** Runs incrementally after 2nd+ feature completes. Skipped if only 1 feature in version.
**Checkpoint:** After each feature passes all gates, orchestrator asks user whether to deliver to engineering now.

### Standard Mode (single feature)

```
PRD → PRD Review → ⭐ Deliver to engineering
```

| Step | Name | Sub-agent? | Output |
|------|------|:----------:|--------|
| S1 | PRD Authoring | ✅ (pm) | `docs/prd/<version>/<feature-id>.md` |
| S2 | PRD Review | ✅ (prd-reviewer / `woos-product-prd-review-gate`) | `docs/reviews/<version>/<feature-id>-prd-review-rN.md` |

PRD Review PASS → deliver to engineering.

### Lite Mode (trivial)

| Step | What | Output |
|------|------|--------|
| L1 | PRD (lightweight) | `docs/prd/<version>/<feature-id>.md` |

No review gates. PRD written → deliver to engineering.

### Deliverable to Engineering (all modes)

⭐ **Deliver to the coding agent after feature design completes:**

```
Required:
  - docs/prd/<version>/<feature-id>.md           ← PRD (full context: why + what + edge cases)
  - docs/product/<project>-architecture.md       ← system architecture constraints
  - docs/product/<project>-roadmap.md            ← product direction and version context

Additional in Strict mode:
  - docs/prd/<version>/<feature-id>-interface.md ← cross-feature shared contract
  - docs/design/<version>/<feature-id>-ui-brief.md ← UI implementation direction (if any)
  - docs/prd/<version>/<upstream-feature-id>-interface.md ← upstream dependency interfaces
```

The coding agent owns task decomposition, ordering, and implementation decisions. Product does not split engineering work.

---

## Legend

| Column | Meaning |
|--------|---------|
| Sub-agent? | ✅ = dispatched as independent sub-agent with fresh context. ❌ = orchestrator handles directly. |
| Persona | Role identity injected via `customize.toml`. |
| Output | File path produced by this step. |

## File Types

| Suffix | Role |
|--------|------|
| `customize.toml` | Agent persona: identity, principles, constraints |
| `SKILL.md` | Methodology: workflow procedure |
| `steps/*.md` | Sub-step detailed method |
| `assets/*.md` | Output template / example |
| `references/*.md` | Quality criteria / spec |

## Context Budget

Every step ≤ 2 files → typically 2–5K tokens of injected knowledge.
Well within sub-agent limits. No context explosion.

## Output Templates

Templates in `skills/product-design/templates/` define the structure each step must produce:

| Template | Used By |
|----------|---------|
| `prd-template.md` | Step 2 (PRD Authoring) |

**Convention:** When a sub-agent encounters an unknown or unresolved decision, it MUST mark it as `[NEEDS CLARIFICATION: <what is needed>]` rather than inventing an answer. The orchestrator collects these markers and asks the user before proceeding to the next step.

---

## Step I/O Declarations

Every step declares explicit `input` and `output` so the next agent knows exactly what to read.

### Stage 1

| Step | Input | Output |
|------|-------|--------|
| 1 Idea Capture | _(user conversation)_ | `ideas/<slug>/00-idea-capture.md` + `.ratchet/runs/<run_id>/run-manifest.yaml` |
| 2 Problem Validation | `ideas/<slug>/00-idea-capture.md` | `ideas/<slug>/00-idea-capture.md` → appends `## Problem Validation` |
| 3 Research | `ideas/<slug>/00-idea-capture.md` (full text) | `docs/research/<topic>.md` |
| 4 Roadmap | `ideas/<slug>/00-idea-capture.md` + `docs/research/*.md` | `docs/product/<project>-roadmap.md` |
| 4R Roadmap Review | `docs/product/<project>-roadmap.md` + `ideas/<slug>/00-idea-capture.md` | `docs/reviews/<project>-roadmap-review-rN.md` |
| 5 Architecture | `docs/product/<project>-roadmap.md` | `docs/product/<project>-architecture.md` |
| 5R Architecture Review | `docs/product/<project>-architecture.md` + `docs/product/<project>-roadmap.md` | `docs/reviews/<project>-architecture-review-rN.md` |
| 6 Decision Log | `docs/product/<project>-roadmap.md` | `docs/product/<project>-roadmap.md` → appends to `## Decision Log` |

### Stage 2 (per feature, with checkpoint after each)

| Step | Input | Output |
|------|-------|--------|
| 1 Select Scope | `docs/product/<project>-roadmap.md` | _(confirmed version + feature list)_ |
| 1.5 Dependency Analysis | `docs/product/<project>-roadmap.md` § selected version | _(execution order + feature IDs + interface pass-through plan)_ |
| 2 PRD Authoring | `docs/product/<project>-roadmap.md` § target version § feature + `docs/product/<project>-architecture.md` | `docs/prd/<version>/<feature-id>.md` |
| 3 PRD Review | `docs/prd/<version>/<feature-id>.md` + roadmap + architecture | `docs/reviews/<version>/<feature-id>-prd-review-rN.md` |
| 4 UI Brief (opt-in) | `docs/prd/<version>/<feature-id>.md` | `docs/design/<version>/<feature-id>-ui-brief.md` |
| 4R UI Review | UI brief + PRD | `docs/reviews/<version>/<feature-id>-ui-review-rN.md` |
| 5 Analyze Gate | PRD + UI brief (if exists) | `docs/reviews/<version>/<feature-id>-analyze-report.md` |
| 5.5 Interface Summary | PRD | `docs/prd/<version>/<feature-id>-interface.md` |
| 6 Integration | All `*-interface.md` + architecture + newest/full PRD set per mode | `docs/reviews/<version>/integration-report.md` |
| | **⭐ CHECKPOINT: deliver to engineering?** | |

---

## Review Fix Flow

When a review gate returns `REQUEST_CHANGES`:

```
┌─────────────┐      findings file       ┌─────────────┐
│  Reviewer   │ ───────────────────────▶ │  Findings   │
│ (sub-agent) │                           │  .md file   │
└─────────────┘                           └──────┬──────┘
                                                  │
                                                  ▼
                                          ┌─────────────┐
                                          │ Fix Agent   │  ← same persona as original author
                                          │ (sub-agent) │
                                          └──────┬──────┘
                                                  │ reads findings, fixes source artifact
                                                  │ marks Fixed? ☑ in findings file
                                                  ▼
                                          ┌─────────────┐
                                          │  Reviewer   │  ← re-dispatched, round N+1
                                          │ (sub-agent) │
                                          └─────────────┘
```

### Rules

1. **Who fixes:** A new sub-agent with the same persona as the original step (e.g., Step 5 author = pm persona)
2. **What it reads:** The findings file + the original artifact
3. **How it fixes:** Edits the original artifact **in-place** (same file path, no versioning of drafts)
4. **How it signals done:** Marks each `Fixed?` cell as `☑` in the findings file
5. **What triggers re-review:** Orchestrator sees all ❌ rows now have `Fixed? ☑` → dispatches reviewer again
6. **Max rounds:** 2 fix-review cycles. If still failing → orchestrator asks user.
7. **Round tracking:** Findings file name includes round number: `*-review-r1.md`, `*-review-r2.md`

---

## Review Checklist Fix Hints

Each review criterion includes a `Fix Hint` — a one-line instruction telling the fix agent HOW to resolve the issue, not just WHAT is wrong.

### Stage 1 — Roadmap Review (5R)

| # | Criterion | Fix Hint |
|---|-----------|----------|
| R1 | Vision differentiated | Add a "Unlike X, we…" statement that names the unique angle |
| R2 | Versioning logical | Move items that have no V1 dependency into V2+; ensure V1 is shippable alone |
| R3 | Metrics measurable | Replace vague words ("fast", "many") with specific numbers or observable events |
| R4 | Non-goals effective | Rewrite as concrete "we will NOT do X even if Y" statements |
| R5 | Decision Log sound | Add real alternative that was considered; explain why it lost |
| R6 | Personas grounded | Cite observed behavior or data; remove hypothetical "ideal user" language |

### Stage 1 — Architecture Review (6R)

| # | Criterion | Fix Hint |
|---|-----------|----------|
| A1 | Component boundaries | Split component into two if it has >1 responsibility; name each clearly |
| A2 | Communication consistency | Pick one primary pattern; justify exceptions explicitly |
| A3 | Data decoupling | Introduce API boundary between components sharing raw data |
| A4 | Infrastructure proportional | Remove infra not needed until V2; document when it becomes necessary |
| A5 | Dependencies manageable | Add "can be built independently" note; if not, mark as sequential |
| A6 | Risks realistic | Add concrete mitigation action (not just "monitor") |
| A7 | Version-aligned | Move components only needed by V2+ features out of V1 architecture |

### Stage 2 — PRD Review (5)

| # | Criterion | Fix Hint |
|---|-----------|----------|
| P1 | Value-traced | Add "User value: …" line to each requirement linking it to a user outcome |
| P2 | AC testable | Rewrite as "Given X, When Y, Then Z" or add specific measurable threshold |
| P3 | Non-goals effective | Make non-goal specific enough to reject a concrete feature request |
| P4 | Edge cases covered | Add "What if…" section for: empty state, error, timeout, concurrent access |
| P5 | Real user behavior | Replace developer-centric language with user-observable actions |
| P6 | No contradictions | Identify conflicting requirements; pick one and move the other to non-goals |

### Stage 2 — UI Brief Review (6R)

| # | Criterion | Fix Hint |
|---|-----------|----------|
| U1 | Screen coverage | List unmapped user stories; add a screen or flow for each |
| U2 | States complete | Add missing states (empty/loading/error/success) to each screen |
| U3 | Flows connected | Trace each flow end-to-end; add missing transitions or exit points |
| U4 | Visual consistency | Remove contradicting principles; pick one direction |
| U5 | Accessibility realistic | Downgrade to achievable level (e.g., AAA → AA); document timeline for upgrade |
| U6 | Components sufficient | List screens with no component mapping; add components or mark as reusing existing |
| U7 | Principles actionable | Replace generic principles ("clean", "modern") with decision-guiding rules |

---

## State Persistence & Crash Recovery

### State File

Every run tracks progress in `.ratchet/runs/<run_id>/run-manifest.yaml`.
The manifest is created at **Step 1** (Idea Capture) so that even early crashes can recover.

```yaml
run_id: "abc-123"
project: "my-project"
created_at: "2025-05-23T10:00:00Z"
updated_at: "2025-05-23T12:30:00Z"

stages:
  product-discovery:
    status: in_progress  # pending | in_progress | done | blocked
    current_step: 6
    steps:
      1-idea-capture: { status: done, output: "ideas/my-project/00-idea-capture.md" }
      2-problem-validation: { status: done, output: "ideas/my-project/00-idea-capture.md#problem-validation" }
      3-research: { status: done, output: "docs/research/my-project-market.md" }
      4-roadmap: { status: done, output: "docs/product/my-project-roadmap.md" }
      4r-roadmap-review: { status: done, round: 2, result: PASS }
      5-architecture: { status: in_progress, output: "docs/product/my-project-architecture.md" }
      5r-architecture-review: { status: pending }
      6-decision-log: { status: pending }

  product-design-flow:
    status: pending
    version: null
    features: {}
```

### Recovery Protocol

When orchestrator starts (or restarts after crash):

```
1. Read `.ratchet/runs/<run_id>/run-manifest.yaml`
2. Find first step where status != done
3. Check if output file for that step exists:
   a. EXISTS + well-formed → mark step done, advance
   b. EXISTS + incomplete  → resume step (re-dispatch sub-agent with existing content)
   c. NOT EXISTS           → start step from scratch
4. Continue from that point
```

### Update Rules

- Orchestrator writes `run-manifest.yaml` **before** dispatching each sub-agent (status: `in_progress`)
- Orchestrator writes `run-manifest.yaml` **after** sub-agent returns (status: `done` + output path)
- Review results include: `round: N`, `result: PASS|REQUEST_CHANGES`
- If step is `in_progress` on restart → check output file existence to decide resume vs restart
