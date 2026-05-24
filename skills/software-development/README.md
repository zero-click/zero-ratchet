# Software Development Workflow

A gated engineering pipeline for AI coding agents. Receives a build handoff from the product design stage, decomposes into stories, and delivers a production-ready PR through TDD, review gates, and end-to-end requirement traceability.

## Purpose

This is **Stage 3** of the idea-to-delivery pipeline. It ensures:

- Engineering receives a fully-defined handoff — no product-phase work happens here
- Work is decomposed into independent, verifiable stories with clear DAG ordering
- Every story is implemented via TDD (RED → GREEN → REFACTOR)
- Requirements are traced end-to-end: PRD → design → code → test
- Design issues flow back to product via DCR (Design Change Request)

## Quick Start

1. Ensure a build handoff exists at `docs/handoff/<version>/<feature>.md`
2. The agent activates `woos-development-workflow` (entry point skill)
3. The workflow auto-selects Lite/Standard/Strict based on handoff content
4. Follow the gated flow — each gate must PASS before the next begins

**Prerequisite:** Product design pipeline must have completed. No handoff = BLOCKED.

## Workflow Flowchart

```
                     ┌───────────────────────┐
                     │  Build Handoff        │
                     │  (from product stage) │
                     └───────────┬───────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Bootstrap                   │
                  │  Run Orchestrator + Git      │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 0: Handoff Intake      │
                  │  Validate handoff, record    │
                  │  version in run-manifest     │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 1: Feature Design      │
                  │  Technical design artifact   │
                  │  (architecture, data, API)   │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 1R: Design Review      │
                  │  Independent architect       │
                  │  review (PASS/REQUEST_CHANGES)│
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 2: Story Decomposition │
                  │  Break handoff into 3–8      │
                  │  independent stories (DAG)   │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 3: Story Execution     │
                  │  Loop (per story):           │
                  │                              │
                  │  ┌────────────────────────┐  │
                  │  │ 3.1 TDD (RED→GREEN)   │  │
                  │  │ 3.2 Implement          │  │
                  │  │ 3.3 Verify (test+lint) │  │
                  │  │ 3.4 Story AC Gate      │  │
                  │  └─────────┬──────────────┘  │
                  │            │                  │
                  │    PASS → next story          │
                  │    FAIL 3× → mark blocked     │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 4: Executable          │
                  │  Acceptance                  │
                  │  All AC → executable checks  │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 5: Deviation Control   │
                  │  Implementation vs handoff   │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 6: Requirement         │
                  │  Traceability                │
                  │  PRD → design → code → test │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 7: Code/Security       │
                  │  Review                      │
                  │  Fresh context, no self-review│
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 8: PR Readiness        │
                  │  Traceability matrix + PR    │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Post: Workflow Memory       │
                  │  Capture patterns for reuse  │
                  └──────────────┬──────────────┘
                                 │
                      ┌──────────▼──────────┐
                      │    PR Created ✅    │
                      └─────────────────────┘

  On design issue at any gate:
  ┌─────────────────────────────────────────┐
  │  DCR → docs/feedback/<feature>-dcr.md   │
  │  → back to product pipeline for fix     │
  └─────────────────────────────────────────┘
```

## Gate Breakdown

### Gate 0 — Handoff Intake

**What:** Validate the build handoff from product pipeline.

- Confirm file at `docs/handoff/<version>/<feature>.md`
- Verify required sections: Mission, Requirements, AC, User Flows, Build Tasks, Verification Plan
- Record handoff version in run-manifest for traceability
- If first time on this codebase: invoke `codebase-onboarding` for analysis
- Output: validated handoff reference in run-manifest

### Gate 1 — Feature Design

**What:** Produce the technical design artifact based on handoff.

- **Skill:** `woos-feature-design`
- Covers: architecture, data model, interfaces, risk, rollout/rollback
- If API endpoints: reference `api-design` patterns
- If database changes: reference `database-migrations` strategy
- If deployment needed: reference `deployment-patterns` for rollout/rollback
- Deviations from baseline captured via `architecture-decision-records`
- Output: `docs/design/<feature>.md`

### Gate 1R — Design Review

**What:** Independent review of the design by a fresh architect agent.

- **Skill:** `woos-design-review-gate`
- Uses `woos-review-context` for cumulative findings
- Escalates to `woos-human-handoff` after 3 failed rounds
- Output: PASS or REQUEST_CHANGES with specific feedback

### Gate 2 — Story Decomposition

**What:** Break the handoff into independent, verifiable stories.

- Built-in orchestrator procedure
- Each story covers 1–3 related Build Tasks
- Stories form a DAG (dependency order)
- Each story is independently verifiable
- Target: 3–8 stories per feature
- Output: `docs/stories/<feature>/story-NNN.md`

### Gate 3 — Story Execution Loop

**What:** Execute each story with TDD, implementation, and verification.

Per story (in dependency order):

| Sub-step | Skill | What |
|----------|-------|------|
| 3.1 TDD | `tdd-workflow` | RED → GREEN → REFACTOR |
| 3.2 Implement | `coding-standards` | Minimal, scoped, convention-aligned |
| 3.3 Verify | `verification-loop` | Tests + lint + type check |
| 3.4 Story AC | built-in | Per-story acceptance check |

**Conditional skills activated within Gate 3:**
- `database-migrations` — when story touches schema
- `e2e-testing` — when story needs Playwright integration tests
- `browser-qa` — when story includes UI changes

**Failure isolation:** A blocked story does NOT block independent stories. Blocked stories retry after others complete; if still stuck → DCR.

### Gate 4 — Executable Acceptance

**What:** Full-feature acceptance check after all stories complete.

- **Skill:** `woos-executable-acceptance-gate`
- Maps ALL handoff AC to executable checks
- Missing automation = blocker
- Output: PASS → proceed. REQUEST_CHANGES → back to Gate 3.

### Gate 5 — Deviation Control

**What:** Compare implementation against handoff and design.

- **Skill:** `woos-deviation-control-gate`
- Unresolved deviations block progression
- Intentional deviations require updated artifacts + rationale

### Gate 6 — Requirement Traceability

**What:** Trace from PRD through design to code and tests.

- Built-in procedure (reads PRD + design + implementation)
- Produces traceability table: `PRD AC → Design Spec → Code → Test → Status`
- Classifications: ✅ Aligned, ⚠️ Deviated (rationale required), ❌ Missing, 🆕 Added
- Zero ❌ required for PASS
- Output: `docs/handoff/<feature>-traceability.md`

### Gate 7 — Code/Security Review

**What:** Independent code review in fresh context.

- **Skill:** `woos-code-review-gate`
- Dispatches `code-reviewer` (+ `security-reviewer` with `security-review` knowledge if sensitive)
- If Strict: also checks architecture conformance
- If applicable: invokes `production-audit` for pre-merge readiness
- Uses `woos-agent-decision` for reviewer conflicts
- 3 rounds without convergence → `woos-human-handoff`

### Gate 8 — PR Readiness

**What:** Final verification and PR creation.

- **Skill:** `woos-pr-readiness`
- All tests pass, lint clean, no unlinked TODOs
- Traceability matrix (requirement → test → code)
- Conventional commit messages
- PR description includes: story summary, test plan, blocked stories
- Creates PR via `gh pr create`

### Post — Workflow Memory

**What:** Capture learnings for future runs.

- **Skill:** `woos-workflow-memory`
- Records: failures, rework causes, story decomposition quality, DCR outcomes
- Persists reusable guidance for next run

## Three Execution Modes

| Mode | When | Gates | Story Loop |
|------|------|-------|------------|
| **Lite** | Low-risk, limited scope, no arch changes | Handoff → Implement → Verify → Review → PR | No decomposition |
| **Standard** | Multi-file, moderate risk (default) | All 9 gates | Full story loop |
| **Strict** | Security-sensitive, high uncertainty | All + API Review + Browser QA + Arch Conformance | Full story loop |

**Mode is determined by handoff content**, not chosen manually:
- Lite handoff (4 sections) → Lite mode
- Full handoff (13 sections) → Standard mode
- Full handoff + security/compliance flags → Strict mode

## Enforcement Rules

The workflow includes 3 non-negotiable enforcement rules (E1–E3) learned from production agent failures:

- **E1: Knowledge Injection Protocol** — before dispatching any review sub-agent, the orchestrator MUST read and inject the relevant imported skill content. A sub-agent with only a role name ("you are a code reviewer") produces shallow output. Inject full methodology.
- **E2: Structured Review Output** — all review gates must produce a findings table (severity, category, finding, location, recommendation) + verdict + evidence. A bare "PASS" or "LGTM" is INVALID and triggers rerun.
- **E3: Conditional Skill Activation** — conditional skills (browser-qa, e2e-testing, database-migrations, security-review, etc.) have concrete trigger rules. If the trigger is met, activation is MANDATORY. Agent cannot skip based on "judgment".

## Skill Map

### Local Skills (workflow gates)

| Skill | Role |
|-------|------|
| `woos-development-workflow` | **Entry point** — orchestrator, gate progression |
| `woos-feature-design` | Gate 1 — technical design artifact |
| `woos-design-review-gate` | Gate 1R — independent design review |
| `woos-executable-acceptance-gate` | Gate 4 — machine-checkable done criteria |
| `woos-deviation-control-gate` | Gate 5 — implementation-vs-spec drift blocking |
| `woos-code-review-gate` | Gate 7 — independent code/security review |
| `woos-pr-readiness` | Gate 8 — PR creation and verification |
| `woos-workflow-memory` | Post — persistent pattern capture |
| `woos-run-orchestrator` | Infrastructure — run queue, concurrency, timeout |
| `woos-failure-state-machine` | Infrastructure — retry/degrade/escalation |
| `woos-human-handoff` | Infrastructure — escalation and recovery |
| `woos-review-context` | Infrastructure — cumulative cross-gate findings |
| `woos-agent-decision` | Infrastructure — reviewer conflict resolution |
| `woos-systematic-debugging` | Infrastructure — structured debugging on failures |
| `woos-setup-rules` | Utility — project rule routing setup |

### Imported Skills (from ECC)

| Skill | Gate | Role |
|-------|------|------|
| `git-workflow` | Bootstrap | Branch strategy, commit/PR flow |
| `tdd-workflow` | Gate 3.1 | RED → GREEN → REFACTOR methodology |
| `coding-standards` | Gate 3.2 | Code quality and convention enforcement |
| `verification-loop` | Gate 3.3 | Lint/test/type/build verification |
| `api-design` | Gate 1 (conditional) | REST/GraphQL design patterns |
| `browser-qa` | Gate 3 (conditional) | UI smoke test, visual regression |
| `e2e-testing` | Gate 3 (conditional) | Playwright E2E patterns, Page Object Model |
| `security-review` | Gate 7 | Security checklist: auth, input, secrets, API, payments |
| `architecture-decision-records` | Gate 1 + cross-gate | Structured ADR capture for deviations |
| `database-migrations` | Gate 3 (conditional) | Zero-downtime schema changes, rollback |
| `deployment-patterns` | Gate 1, Gate 8 | CI/CD, Docker, rollback, production readiness |
| `production-audit` | Gate 7 (conditional) | Pre-merge production readiness audit |
| `codebase-onboarding` | Gate 0 (first run) | Codebase analysis and onboarding guide |
| `search-first` | Any gate | Quick research and reference lookup |
| `deep-research` | Any gate | Deep research when needed |
| `dmux-workflows` | Gate 3 (parallel) | Parallel coding lanes via worktrees |

## Key Design Principles

1. **Handoff-first** — no product-phase work here; handoff is the input contract
2. **Story-based decomposition** — large features broken into independently verifiable units
3. **TDD per story** — RED/GREEN/REFACTOR is not optional
4. **Failure isolation** — blocked stories don't cascade; independent work continues
5. **End-to-end traceability** — PRD → design → code → test chain is verified
6. **Bidirectional feedback** — DCR flows back to product when design issues are found
7. **Fresh-context reviews** — no self-review; dispatched in clean sub-agent context
8. **Baseline-first governance** — deviations require ADR + approval

## ECC Knowledge Architecture

This workflow draws its engineering methodology from [ECC](https://github.com/anthropics/courses/tree/master/prompt_engineering) (Everything Claude Code) — a curated library of domain-specific skills. Unlike the product side (which uses BMAD personas/frameworks/templates), the engineering side uses **imported skill files** as its knowledge layer.

### Knowledge Categories

#### Core Methodology (always active)

Skills that define HOW engineering work is done, active in every Standard/Strict run:

| Skill | Knowledge Provided | Gate |
|-------|-------------------|------|
| `tdd-workflow` | TDD discipline: RED before GREEN, cycle stall detection, refactor patterns | 3.1 |
| `coding-standards` | Convention enforcement, minimal changes, no silent failures | 3.2 |
| `verification-loop` | Multi-layer verification: lint → type → test → build | 3.3 |
| `git-workflow` | Branch strategy, conventional commits, PR flow | Bootstrap |

#### Security & Compliance (Gate 7)

Skills that provide security domain knowledge for review gates:

| Skill | Knowledge Provided |
|-------|-------------------|
| `security-review` | Authentication patterns, input validation, secrets handling, API security, payment flow security, OWASP checklist |
| `production-audit` | Pre-merge production readiness: error handling, logging, monitoring, graceful degradation |

#### Architecture & Design (Gate 1)

Skills that provide design methodology and decision capture:

| Skill | Knowledge Provided |
|-------|-------------------|
| `api-design` | REST/GraphQL conventions: resource naming, status codes, pagination, error format, rate limiting |
| `architecture-decision-records` | ADR structure, when to capture, context/decision/consequences format |
| `deployment-patterns` | CI/CD pipelines, Docker patterns, health checks, rollback strategies, blue-green/canary |
| `database-migrations` | Zero-downtime migrations, rollback plans, data backfill, ORM patterns (Prisma, Django, etc.) |

#### Testing (Gate 3)

Skills that provide testing methodology beyond unit tests:

| Skill | Knowledge Provided |
|-------|-------------------|
| `e2e-testing` | Playwright patterns, Page Object Model, test isolation, CI/CD integration, flaky test strategies |
| `browser-qa` | Visual regression, accessibility (WCAG AA), Core Web Vitals, responsive breakpoints |

#### Research & Context (any gate)

Skills that provide information-gathering capability:

| Skill | Knowledge Provided |
|-------|-------------------|
| `search-first` | Quick targeted research, reference lookup |
| `deep-research` | Multi-source deep investigation for complex problems |
| `codebase-onboarding` | Codebase analysis: architecture map, entry points, conventions, patterns |

### Gate × Knowledge Matrix

| Gate | Core | Security | Architecture | Testing | Research |
|------|------|----------|-------------|---------|----------|
| **0: Handoff Intake** | — | — | — | — | `codebase-onboarding` |
| **1: Feature Design** | — | — | `api-design`, `architecture-decision-records`, `deployment-patterns`, `database-migrations` | — | `deep-research` |
| **1R: Design Review** | — | — | — | — | — |
| **2: Story Decomposition** | — | — | — | — | — |
| **3: Story Loop** | `tdd-workflow`, `coding-standards`, `verification-loop` | — | `database-migrations` | `e2e-testing`, `browser-qa` | `search-first` |
| **4: Acceptance** | `verification-loop` | — | — | — | — |
| **5: Deviation Control** | — | — | `architecture-decision-records` | — | — |
| **6: Traceability** | — | — | — | — | — |
| **7: Code Review** | — | `security-review`, `production-audit` | — | — | — |
| **8: PR Readiness** | `git-workflow` | — | `deployment-patterns` | — | — |

## DCR (Design Change Request)

When engineering discovers a design issue that can't be resolved within scope:

1. Write `docs/feedback/<feature>-dcr.md` (issue, impact, proposed fix, priority)
2. Stop work on affected stories
3. Continue with unaffected stories
4. Product pipeline receives DCR, fixes, and re-issues updated handoff

## File Layout

```
<project-root>/
├── .hep/
│   ├── runs/<run_id>/
│   │   └── run-manifest.yaml          ← gate progress tracking
│   └── review-context/<run_id>.yaml   ← cumulative findings
├── docs/
│   ├── handoff/<version>/<feature>.md ← INPUT (from product)
│   ├── prd/<feature>.md               ← read for traceability
│   ├── design/<feature>.md            ← Gate 1 output
│   ├── stories/<feature>/             ← Gate 2 output
│   │   ├── story-001.md
│   │   ├── story-002.md
│   │   └── ...
│   ├── adr/                           ← ADR captures
│   ├── feedback/<feature>-dcr.md      ← DCR output (back to product)
│   └── handoff/<feature>-traceability.md ← Gate 6 output
└── (implementation files)
```
