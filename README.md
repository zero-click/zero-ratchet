# zero-ratchet

[English](./README.md) | [中文](./README.zh.md)

A complete **idea → delivery** skill collection for AI coding agents: product discovery, PRD, design, story plan, TDD loop, gates, traceability, PR — with role separation and hard checkpoints at every stage.

Host-agnostic. Works with any agent runtime that loads skills from a directory (Claude Code, Cursor, Hermes, …).

**Core thesis:** you remember two entry points (`woos-idea-to-design` for product work, `woos-development-workflow` for engineering). The orchestrator inside loads the right sub-skills, dispatches reviewers in fresh contexts, and gates progression. Skills are written for the AI to read, not for the human to memorize. Humans re-enter only at deliberately placed checkpoints.

## What's Inside

| Directory | What it does | Maintained as |
|-----------|--------------|---------------|
| `skills/product-design/` | Product flow: idea → discovery → PRD → roadmap → UI brief | local, `woos-*` |
| `skills/software-development/` | Engineering flow: design → story plan → TDD loop → review → PR | local, `woos-*` |
| `skills/ecc/` | Upstream [ECC](https://github.com/everything-claude-code/everything-claude-code) skills used by the engineering flow (tdd-workflow, security-review, …) | snapshot — do not hand-edit |

The three directories are independent. Take only what you need.

## Install

There is no installer. Copy or symlink the directories you want into wherever your agent host loads skills from. Symlinks let upstream `git pull` updates flow through:

```bash
ln -s "$PWD/skills/product-design"       ~/.claude/skills/product-design
ln -s "$PWD/skills/software-development" ~/.claude/skills/software-development
ln -s "$PWD/skills/ecc"                  ~/.claude/skills/ecc
```

Substitute `.claude/skills/` with `.cursor/skills/`, `~/.hermes/profiles/coding/skills/`, or whatever your runtime expects.

## Naming Convention

- **`woos-*`** — locally authored skills, edit freely
- **no prefix** (only under `skills/ecc/`) — upstream snapshot, do not hand-edit; use the refresh script

## Pipeline Overview

```
┌──────────────────────────────────┐        ┌──────────────────────────────────┐
│   Product Design Stage           │  PRD   │   Software Development Stage     │
│   skills/product-design/         │──────▶ │   skills/software-development/   │
│                                  │ Roadmap│                                  │
│   Idea → Capture → Discovery     │ Arch   │   Design → Story Plan → TDD Loop │
│   → 🚦 Human Gate                │        │   → Review → Trace → PR          │
│                                  │        │                                  │
│   Entry: woos-idea-to-design     │        │   Entry: woos-development-workflow│
│   Modes: Lite / Standard / Strict│        │   Modes: Lite / Standard         │
└──────────────────────────────────┘        └──────────────────────────────────┘
                                                          │
                                                   DCR (feedback)
                                                          ▼
                                              docs/feedback/<ver>/...
```

**Handoff contract between the two stages:**

- `docs/product/<project>-roadmap.md` — version scope, goals
- `docs/product/<project>-architecture.md` — top-level component map
- `docs/prd/<version>/<feature-id>.md` — per-feature PRD (problem, functional + non-functional requirements, behavior contract)
- `docs/prd/<version>/<feature-id>-interface.md` — shared interface summary (enums, data models, event/API shapes) when other features depend on this one
- `docs/design/<version>/<feature-id>-ui-brief.md` — UI direction when the feature has UI

Engineering owns the rest: code organization, library choice, internal data structures, test strategy, deployment.

**DCR loop:** when engineering discovers a wrong product assumption, it issues a Design Change Request back to product — the PRD is updated and engineering resumes.

## Product Design Stage

See [`skills/product-design/README.md`](./skills/product-design/README.md) for the full pipeline.

| Skill | Role |
|-------|------|
| `woos-idea-to-design` | Umbrella orchestrator from raw idea to engineering-ready artifacts |
| `woos-idea-capture` | Idea interview and structuring |
| `woos-product-discovery` | Research, roadmap, architecture |
| `woos-product-design-flow` | PRD pipeline orchestrator |
| `woos-ui-design-brief` | UI direction and wireframes |

Enforcement: 7 non-negotiable rules (E1–E7) block step-skipping, template ignorance, and shallow reviews.

## Software Development Stage

See [`skills/software-development/README.md`](./skills/software-development/README.md) for the full pipeline.

Entry: `woos-development-workflow`. Standard mode flow:

```
Run Orchestrator → Git → Product Intake
  → Gate 1  Feature Plan (architecture + story table)  (woos-feature-plan)
  → Gate 1R Plan Review (2 reviewers, fresh context)   (woos-plan-review-gate)
  → Gate 2  Story Loop              (TDD + Implement + Verify per story)
  → Gate 3  Review (code + security + AC coverage + scope drift)
  → Gate 4  Ship (traceability matrix + PR readiness + gh pr create)
  → Workflow Memory
```

Lite mode skips Gate 1 and 1R; Gate 3 skips its AC-coverage and scope-drift checks; Gate 4 skips traceability-matrix generation. Use for low-risk small changes.

**Gate 1 output** is a single per-feature `docs/engineering/<version>/<feature-id>-plan.md` containing architecture decisions, test strategy, rollout/rollback, baseline/deviation record, and the story execution table (`ID | AC | Depends | Diff Scope`). Interface contracts live in the PRD's `<feature-id>-interface.md` and are not duplicated. PRD AC is the spec, tests in the diff scope are the verification, and `git restore -- <diff_scope>` is the rollback.

## How This Compares

| Framework | Strength | Why this repo exists alongside it |
|-----------|----------|------------------------------------|
| [ECC](https://github.com/everything-claude-code/everything-claude-code) | High-quality engineering skill library (TDD, security, deployment, …) | ECC is a buffet — 50+ skills, no orchestrator, the user picks each time. This repo adds gate progression, conditional trigger rules, and PRD-side coverage on top of ECC. |
| [BMAD](https://github.com/bmadcode/BMAD-METHOD) | Persona-led product + agile flow | BMAD is conversation-led ("talk to the PM agent"); this repo is workflow-led (two trigger phrases, AI runs the rest). Lighter persona surface, more machine-checkable gates. |
| Superpowers | Practical engineering loop with strong TDD/debug discipline | Superpowers is engineering-only. This repo adds a full product pipeline (discovery, PRD, interface summaries, UI brief) before the engineering loop. |

**Use this repo when:** you want a long-horizon, multi-feature, gated, traceable, AI-driven pipeline where the human re-enters at specific checkpoints rather than every step.

**Probably overkill when:** a single small change you can describe in two sentences. Use Superpowers or raw ECC directly.

## Known Limitations

Honest list — these are real and not getting solved this week:

- **AI judges AI.** Every gate's PASS is emitted by an LLM. `fresh_context` reduces collusion but does not import outside judgment. A first-round false PASS is the largest blind spot — only failures escalate to `woos-human-handoff`, successes do not.
- **`invocation_evidence` is self-attested.** The same AI that should have invoked a sub-skill also writes the JSON claiming it did. Mitigation would require an external process to log dispatch events; currently absent.
- **No CI for skill cross-references.** SKILL.md files reference each other by string (`woos-architect`, `woos-product-planner`, …). A rename / delete is detected only when the orchestrator tries to dispatch and fails.
- **Definition of done stops at PR merge.** No post-merge hook for deployment, observability, or "did the roadmap success metric actually move".
- **Single-user, not battle-tested.** ECC, BMAD, Superpowers have communities surfacing edge cases. This pipeline has been run end-to-end by one person on a small number of features. Many failure modes are still latent.
- **DCR friction may suppress reporting.** Gate 3's scope-drift check makes unauthorized deviation expensive, which can incentivize hiding deviations rather than reporting them. No counter-incentive currently.
- **DAG rollback ambiguity.** If a downstream story committed against an upstream story that later needs revert, the cascade-revert procedure is left to the AI rather than spelled out in the workflow.

## Updating `skills/ecc/`

`skills/ecc/` is a snapshot of upstream ECC. Refresh from a local ECC checkout and commit the diff:

```bash
scripts/refresh-ecc-skills.sh /path/to/everything-claude-code
git diff skills/ecc
git add skills/ecc && git commit
```

## Design Principles

- **Unattended delivery is the long-term vision.** Role-specialized agents + hard gates so more work runs reliably with minimal human intervention.
- **Role separation, deterministic gate progression, traceable review from idea to merged PR.**
- **Baseline-first governance.** Prefer mainstream maintainable baselines; deviations require an ADR and explicit approval.

### Unattended Execution Foundation

Seven infrastructure skills that make the gated flow run hands-off:

| Skill | Role |
|-------|------|
| `woos-run-orchestrator` | Run queue, concurrency, timeout/retry |
| `woos-code-review-gate` | One-pass review: code/security findings, PRD AC coverage, scope-drift detection, baseline-deviation alignment |
| `woos-failure-state-machine` | Deterministic retry / degrade / escalation |
| `woos-pr-readiness` | Final verification + mechanically generated traceability matrix + PR creation |
| `woos-workflow-memory` | Persistent failure/rework pattern capture |
| `woos-human-handoff` | Explicit takeover and recovery protocol |
| `woos-review-context` | Cumulative cross-gate findings |

### ADR Governance

- ADR template lives in the consuming project: `docs/adr/ADR-template.md`
- Design / code review gates emit `baseline_compliance_status`, `deviation_detected`, `deviation_adr_path`
- Run finalization requires a verified run manifest: `<workspace_root>/hep/runs/<run_id>/run-manifest.yaml`
