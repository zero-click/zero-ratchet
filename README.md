# hermes-ecc-profile

A complete **idea → delivery** skill collection for AI coding agents: product discovery, PRD, design, story plan, TDD loop, gates, traceability, PR — with role separation and hard checkpoints at every stage.

Host-agnostic. Works with any agent runtime that loads skills from a directory (Claude Code, Cursor, Hermes, …).

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

**Stage boundary:** Product defines **WHAT** and **WHY**. Engineering decides **HOW**. PRD + roadmap + architecture are the contract between the two stages.

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
  → Gate 1  Feature Design          (woos-feature-design)
  → Gate 1R Design Review           (woos-design-review-gate)
  → Gate 2  Story Decomposition     → plan.md (ID | AC | Depends | Diff Scope)
  → Gate 3  Story Loop              (TDD + Implement + Verify per story)
  → Gate 4  Executable Acceptance
  → Gate 5  Deviation Control
  → Gate 6  Traceability
  → Gate 7  Code / Security Review
  → Gate 8  PR Readiness
  → Workflow Memory
```

Lite mode skips Gates 1, 1R, 2, 4, 5, 6 — for low-risk small changes.

**Story output (Gate 2)** is a single per-feature `plan.md` table, not per-story narrative documents. PRD AC is the spec, tests in the diff scope are the verification, and `git restore -- <diff_scope>` is the rollback.

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
| `woos-executable-acceptance-gate` | Machine-checkable done criteria |
| `woos-failure-state-machine` | Deterministic retry / degrade / escalation |
| `woos-deviation-control-gate` | Implementation-vs-spec drift blocking |
| `woos-workflow-memory` | Persistent failure/rework pattern capture |
| `woos-human-handoff` | Explicit takeover and recovery protocol |
| `woos-review-context` | Cumulative cross-gate findings |

### ADR Governance

- ADR template lives in the consuming project: `docs/adr/ADR-template.md`
- Design / code review gates emit `baseline_compliance_status`, `deviation_detected`, `deviation_adr_path`
- Run finalization requires a verified run manifest: `<workspace_root>/hep/runs/<run_id>/run-manifest.yaml`
