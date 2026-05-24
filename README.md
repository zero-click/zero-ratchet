# hermes-ecc-profile

[中文说明 / Chinese README](./README.zh-CN.md)

Skill-first coding profile for Hermes — a complete idea-to-delivery pipeline with role-specialized agents, hard gates, and traceable review at every stage.

## Vision

- **Unattended delivery is the long-term vision**: use role-specialized agents and hard gates so more work can run reliably with minimal human intervention.
- **Design principles are the core differentiator**: this profile enforces role separation, deterministic gate progression, and traceable review from idea to merged PR.
- **Baseline-first governance**: default to mainstream, maintainable, evolvable baselines; deviations require ADR + explicit approval.

## Two-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    Product Design Stage                          │
│                  (skills/product-design/)                        │
│                                                                 │
│  Idea → Capture → Discovery → 🚦 Human Gate → PRD → Handoff   │
│                                                                 │
│  Entry: woos-idea-to-delivery                                   │
│  Modes: Lite / Standard / Strict                                │
└────────────────────────────┬────────────────────────────────────┘
                             │  Build Handoff (file-based contract)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Software Development Stage                     │
│               (skills/software-development/)                     │
│                                                                 │
│  Design → Implement → Verify → Review → PR                     │
│                                                                 │
│  Entry: woos-development-workflow                                │
│  Modes: Lite / Standard / Strict                                │
└─────────────────────────────────────────────────────────────────┘
```

**Key boundary:** Product defines WHAT/WHY. Engineering decides HOW. The handoff file is the contract between stages.

## Product Design Stage

See [`skills/product-design/README.md`](./skills/product-design/README.md) for full details.

**Skills:**

| Skill | Role |
|-------|------|
| `woos-idea-to-delivery` | Entry point — umbrella orchestrator, tier routing |
| `woos-idea-capture` | Phase 1 — idea interview and structuring |
| `woos-product-discovery` | Phase 2 — research, roadmap, architecture |
| `woos-product-design-flow` | Phase 3 — PRD pipeline orchestrator |
| `woos-ui-design-brief` | UI direction and wireframes |
| `woos-build-handoff` | Handoff packaging |

**Enforcement:** 7 non-negotiable rules (E1–E7) prevent agents from skipping steps, ignoring templates, or doing shallow reviews.

## Software Development Stage

**Entry skill:** `woos-development-workflow`

```mermaid
flowchart TD
  A[Run Orchestrator<br/>woos-run-orchestrator] --> B[Git Workflow<br/>git-workflow]
  B --> C[Requirement Contract<br/>woos-requirement-contract]
  C --> D[Research<br/>search-first or deep-research]
  D --> E[PRD Draft<br/>woos-prd-authoring]
  E --> F[PRD Review Gate<br/>woos-prd-review-gate]
  F --> G[Capability Contract<br/>product-capability]
  G --> H[Feature Design<br/>woos-feature-design]
  H --> H1{Has API?}
  H1 -->|Yes| H2[API Design Review<br/>api-design]
  H1 -->|No| I
  H2 --> I[Design Review Gate<br/>woos-design-review-gate]
  I --> J[TDD<br/>tdd-workflow]
  J --> K[Implement<br/>coding-standards]
  K --> L[Verify<br/>verification-loop]
  L --> L1{Has UI?}
  L1 -->|Yes| L2[Browser QA<br/>browser-qa]
  L1 -->|No| M
  L2 --> M[Executable Acceptance<br/>woos-executable-acceptance-gate]
  M --> N[Deviation Control<br/>woos-deviation-control-gate]
  N --> O[Code/Security Review Gate<br/>woos-code-review-gate]
  O --> P[PR Readiness<br/>woos-pr-readiness]
  P --> Q[Workflow Memory Update<br/>woos-workflow-memory]

  R[Failure State Machine<br/>woos-failure-state-machine] -.controls all stages.- A
  R -.retry/degrade/escalate.- O
  R2[Systematic Debugging<br/>woos-systematic-debugging] -.activates on repeated failures.- R
  S[Human Handoff<br/>woos-human-handoff] -.escalation/resume.- R
  T[Parallel lanes when needed<br/>dmux-workflows] -.optional.- K

  U[product-planner] -.used by wrapper.- F
  V[architect] -.used by wrapper.- F
  V -.used by wrapper.- I
  Y[woos-review-context] -.used by wrappers.- F
  Y -.used by wrappers.- I
  Y -.used by wrappers.- O
  W[code-reviewer] -.used by wrapper.- O
  X[security-reviewer] -.used by wrapper.- O
  Z[woos-agent-decision] -.on reviewer conflict.- O
```

**Development workflow profiles:**

1. **Lite**: Run Orchestrator → Git → Requirement Contract → Implement → Verify → Code/Security Review → PR
2. **Standard (default)**: adds PRD/design review and workflow memory
3. **Strict**: full hard-gate flow (research/capability/TDD/acceptance/deviation + conditional API/Browser QA)

## Feedback Loop (DCR)

When the engineering stage discovers a product assumption is wrong, it issues a **Design Change Request** back to product:

```
Engineering → docs/feedback/<feature>-dcr.md → Product Design → updated handoff → Engineering resumes
```

Available in Standard and Strict modes.

## Install

```bash
cd /path/to/hermes-ecc-profile
python3 install-profile.py
```

The installer will prompt for local ECC repo path.

Optional:

```bash
python3 install-profile.py --ecc-path /path/to/ecc --profile-root ~/.hermes/profiles/coding --install-soul
```

Backup options:

```bash
# custom backup path
python3 install-profile.py --backup-dir ~/.hermes/profiles/coding.backup.manual

# skip backup (not recommended)
python3 install-profile.py --no-backup
```

MCP sync options:

```bash
# sync recommended MCP servers into <profile>/config.yaml (default interactive: yes)
python3 install-profile.py --sync-mcp

# skip MCP sync
python3 install-profile.py --no-sync-mcp
```

Rules sync options:

```bash
# sync ECC rule groups into <profile>/rules/ecc-import
python3 install-profile.py --sync-rules

# skip rules sync
python3 install-profile.py --no-sync-rules
```

`./install-profile.sh` remains as a thin wrapper to `python3 install-profile.py`.

Installed layout (default profile root: `~/.hermes/profiles/coding`):

- `skills/product-design/*` (product workflow skills)
- `skills/software-development/*` (local workflow skills)
- `skills/ecc-import/*` (imported ECC skills)
- `skills/ecc-agent-skills/*` (agent adapters)
- `SOUL.md` (only if `--install-soul`)

## Near-Unattended Execution Foundation

Seven-part foundation for near-unattended delivery:

1. `woos-requirement-contract` — structured requirement intake
2. `woos-executable-acceptance-gate` — machine-checkable done criteria
3. `woos-failure-state-machine` — deterministic retry/degrade/escalation
4. `woos-deviation-control-gate` — implementation-vs-spec drift blocking
5. `woos-workflow-memory` — persistent failure/rework pattern capture
6. `woos-run-orchestrator` — run queue, concurrency, timeout/retry
7. `woos-human-handoff` — explicit takeover and recovery protocol

## ADR Governance

- ADR template: `docs/adr/ADR-template.md`
- Design/code review gates require: `baseline_compliance_status`, `deviation_detected`, `deviation_adr_path`
- Run finalization requires verified run manifest: `<workspace_root>/hep/runs/<run_id>/run-manifest.yaml`
