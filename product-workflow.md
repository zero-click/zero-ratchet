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
| 4 | Run Initialization | ❌ orchestrator | — | `.hep/runs/<run_id>/run-manifest.yaml` | _(none)_ |
| 5 | Product Vision & Roadmap | ✅ | pm | `docs/product/<project>-roadmap.md` | `personas/pm.toml`<br>`frameworks/create-prd.md` |
| 5R | Roadmap Review | ✅ | product-strategist | `docs/reviews/<project>-roadmap-review-rN.md` | `frameworks/validate-prd.md`<br>`templates/prd-validation-checklist.md` |
| 6 | System Architecture | ✅ | architect | `docs/product/<project>-architecture.md` | `personas/architect.toml`<br>`frameworks/create-architecture.md` |
| 6R | Architecture Review | ✅ | system-architect | `docs/reviews/<project>-architecture-review-rN.md` | `frameworks/architecture-validation.md` |
| 7 | Decision Log | ❌ orchestrator | — | `docs/product/<project>-roadmap.md` → appends `## Decision Log` | _(none)_ |

**Stage 1 final deliverables:**
- `docs/product/<project>-roadmap.md` — 产品愿景 + 用户画像 + V1/V2/V3 路线图 + 决策日志
- `docs/product/<project>-architecture.md` — 系统架构概览

---

## Stage 2: `woos-product-design-flow` (per version)

```
Step 1: Select Version → extract feature list
  → For each feature:
      Steps 2–9 (Requirements → Readiness)
  → After ALL features pass Step 9:
      Step 10: Version Integration Gate
```

| Step | Name | Sub-agent? | Persona | Output | BMAD Knowledge |
|------|------|:----------:|---------|--------|----------------|
| 1 | Select Version Scope | ❌ orchestrator | — | _(version + feature list in run-manifest)_ | _(none)_ |
| 2 | Requirement Contract | ✅ | pm | `docs/prd/<project>/<version>/<feature>-requirements.md` | `personas/pm.toml`<br>`frameworks/prd.md` |
| 3 | Priority Ranking | ✅ | pm | ↑ appends `## Priority Ranking` (P0/P1/P2 + cut-line) | `personas/pm.toml` |
| 4 | PRD Authoring | ✅ | pm | `docs/prd/<project>/<version>/<feature>.md` | `frameworks/prd.md`<br>`templates/prd-template.md` |
| 5 | PRD Review | ✅ | product-planner | `docs/reviews/<project>/<version>/<feature>-prd-review-rN.md` | `frameworks/validate-prd.md`<br>`templates/prd-validation-checklist.md` |
| 6 | UI Design Brief (opt-in) | ✅ | ux-designer | `docs/design/<project>/<version>/<feature>-ui-brief.md` | `personas/ux-designer.toml`<br>`frameworks/ux-design.md` |
| 6R | UI Brief Review | ✅ | ux-reviewer | `docs/reviews/<project>/<version>/<feature>-ui-review-rN.md` | `frameworks/ux-validate.md` |
| 7 | Analyze Gate | ✅ | qa | `docs/handoff/<project>/<version>/<feature>-analyze-report.md` | `frameworks/implementation-readiness.md` |
| 8 | Build Handoff | ✅ | pm | `docs/handoff/<project>/<version>/<feature>.md` | `frameworks/epics-and-stories.md` |
| 9 | Readiness Check | ❌ orchestrator | — | _(pass/fail in run-manifest)_ | _(none)_ |
| **10** | **Version Integration Gate** | ✅ | pm | `docs/reviews/<project>/<version>/integration-report.md` | `frameworks/implementation-readiness.md` |

**Step 6 trigger:** Orchestrator asks user "Does this feature have UI?" — Yes → run, No → skip 6+6R.
**Step 10 trigger:** Runs after ALL features pass Step 9. Skipped if only 1 feature in version.

**Stage 2 final deliverables (per feature):**
- `docs/prd/<project>/<version>/<feature>-requirements.md` — 需求合约 + 优先级排序
- `docs/prd/<project>/<version>/<feature>.md` — 完整 PRD
- `docs/design/<project>/<version>/<feature>-ui-brief.md` — UI 方向（如有）
- ⭐ **`docs/handoff/<project>/<version>/<feature>.md`** — 最终交付物，coding agent 的唯一输入

**Stage 2 final deliverables (per version):**
- `docs/reviews/<project>/<version>/integration-report.md` — 跨 feature 一致性报告

---

## Legend

| Column | Meaning |
|--------|---------|
| Sub-agent? | ✅ = dispatched as independent sub-agent with fresh context. ❌ = orchestrator handles directly. |
| Persona | Role identity injected via `customize.toml`. |
| Output | File path produced by this step. ↑ = appends to previous step's file. |
| BMAD Knowledge | Files from `references/bmad/` (max 2 per step). |

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

---

## Gap 1: Step I/O Declarations

Every step must declare explicit `input` and `output` so the next agent knows exactly what to read.

### Stage 1

| Step | Input | Output |
|------|-------|--------|
| 1 Idea Capture | _(user conversation)_ | `ideas/<slug>/00-idea-capture.md` |
| 2 Problem Validation | `ideas/<slug>/00-idea-capture.md` | `ideas/<slug>/00-idea-capture.md` → appends `## Problem Validation` |
| 3 Research | `ideas/<slug>/00-idea-capture.md` (全文) | `docs/research/<topic>.md` |
| 4 Run Init | _(none)_ | `.hep/runs/<run_id>/run-manifest.yaml` |
| 5 Roadmap | `ideas/<slug>/00-idea-capture.md` + `docs/research/*.md` | `docs/product/<project>-roadmap.md` |
| 5R Roadmap Review | `docs/product/<project>-roadmap.md` + `ideas/<slug>/00-idea-capture.md` | `docs/reviews/<project>-roadmap-review-rN.md` |
| 6 Architecture | `docs/product/<project>-roadmap.md` | `docs/product/<project>-architecture.md` |
| 6R Architecture Review | `docs/product/<project>-architecture.md` + `docs/product/<project>-roadmap.md` | `docs/reviews/<project>-architecture-review-rN.md` |
| 7 Decision Log | `docs/product/<project>-roadmap.md` | `docs/product/<project>-roadmap.md` → appends to `## Decision Log` |

### Stage 2 (Steps 2–9 run per feature, Step 10 runs once for the version)

| Step | Input | Output |
|------|-------|--------|
| 1 Select Scope | `docs/product/<project>-roadmap.md` | _(confirmed version + feature list — stored in run-manifest)_ |
| 2 Requirements | `docs/product/<project>-roadmap.md` § target version § feature | `docs/prd/<project>/<version>/<feature>-requirements.md` |
| 3 Priority Ranking | `docs/prd/<project>/<version>/<feature>-requirements.md` | ↑ appends `## Priority Ranking` |
| 4 PRD Authoring | `docs/prd/<project>/<version>/<feature>-requirements.md` (含 Priority Ranking) | `docs/prd/<project>/<version>/<feature>.md` |
| 5 PRD Review | `docs/prd/<project>/<version>/<feature>.md` + requirements | `docs/reviews/<project>/<version>/<feature>-prd-review-rN.md` |
| 6 UI Brief | `docs/prd/<project>/<version>/<feature>.md` | `docs/design/<project>/<version>/<feature>-ui-brief.md` |
| 6R UI Review | UI brief + PRD | `docs/reviews/<project>/<version>/<feature>-ui-review-rN.md` |
| 7 Analyze Gate | PRD + UI brief (if exists) | `docs/handoff/<project>/<version>/<feature>-analyze-report.md` |
| 8 Handoff | PRD + UI brief + analyze report | `docs/handoff/<project>/<version>/<feature>.md` |
| 9 Readiness | `docs/handoff/<project>/<version>/<feature>.md` | _(pass/fail — updates run-manifest)_ |
| **10 Integration** | All `docs/handoff/<project>/<version>/*.md` | `docs/reviews/<project>/<version>/integration-report.md` |

---

## Gap 2: Review Fix Flow

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

## Gap 3: Review Checklist Fix Hints

Each review criterion must include a `Fix Hint` — a one-line instruction telling the fix agent HOW to resolve the issue, not just WHAT is wrong.

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

## Gap 4: State Persistence & Crash Recovery

### State File

Every run tracks progress in `.hep/runs/<run_id>/run-manifest.yaml`:

```yaml
run_id: "abc-123"
project: "my-project"
created_at: "2025-05-23T10:00:00Z"
updated_at: "2025-05-23T12:30:00Z"

stages:
  product-discovery:
    status: in_progress  # pending | in_progress | completed | blocked
    current_step: 6
    steps:
      1-idea-capture: { status: done, output: "ideas/my-project/00-idea-capture.md" }
      2-problem-validation: { status: done, output: "ideas/my-project/00-idea-capture.md#problem-validation" }
      3-research: { status: done, output: "docs/research/my-project-market.md" }
      4-run-init: { status: done }
      5-roadmap: { status: done, output: "docs/product/my-project-roadmap.md" }
      5r-roadmap-review: { status: done, round: 2, result: PASS }
      6-architecture: { status: in_progress, output: "docs/product/my-project-architecture.md" }
      6r-architecture-review: { status: pending }
      7-decision-log: { status: pending }

  product-design-flow:
    status: pending
    current_step: null
    steps: {}
```

### Recovery Protocol

When orchestrator starts (or restarts after crash):

```
1. Read `.hep/runs/<run_id>/run-manifest.yaml`
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
