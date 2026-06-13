---
name: woos-product-planner
description: Planning and decomposition review skill adapted from ECC planner agent. Covers story-table review (called from the plan review gate) and planning consults for the feature plan skill. PRD-quality review is NOT in scope — that is owned by `woos-product-prd-review-gate`.
origin: ECC-agent-adapter
ecc_source_repo: affaan-m/everything-claude-code
ecc_source_path: agents/planner.md
ecc_source_commit: 0e9f613fd196f6d4157765b17d39c2c42ebbf564
---

# Product Planner

## When to Use

- **Story-table review** (called by `woos-plan-review-gate`): validate AC coverage, dependency DAG, and AI-checkpoint sizing of the story table inside the feature plan
- **Planning consult** (called by `woos-feature-plan`): produce/validate a phased implementation plan, decomposition consult, or dependency-sequencing review while the plan is being authored
- When a task spans multiple files or phases
- When ordering and dependencies are unclear

PRD-quality review is owned by `woos-product-prd-review-gate` and is not performed by this skill.

## Mode Contract

The dispatcher MUST set `mode` explicitly:

- `mode: story-review` — validate the Story Table section of `docs/engineering/<version>/<feature-id>-plan.md`: AC coverage completeness, DAG correctness, sizing against AI-checkpoint rules (one review-round bound, hard cap of 3 AC per story), concrete diff scopes, and non-overlap between unordered stories
- `mode: planning` — produce/validate a phased implementation plan, decomposition consult, or dependency-sequencing review for the feature plan being authored

Each dispatch MUST be a separate fresh-context invocation. PRD-quality review is NOT performed by this skill — it lives in `woos-product-prd-review-gate` on the product-design side.

## Input Contract

- `mode` (required: `story-review` | `planning`)
- Feature goal and scope
- For `story-review`: PRD path + `docs/engineering/<version>/<feature-id>-plan.md` (the Story Table section) + `run-manifest.yaml` excerpt with `execution_order` and `ac_coverage_map`
- For `planning`: relevant PRD context as provided by the caller
- Existing constraints (architecture, policy, timelines if provided)
- Relevant artifact paths (PRD, roadmap, architecture, design, and supporting interface/UI docs when available)

## Workflow

1. Clarify objective, boundaries, and success criteria for the dispatched mode.
2. In `story-review`: validate the story set against AC coverage, DAG integrity, sizing rules, and overlap.
3. In `planning`: identify impacted components and dependency order; produce phased steps with concrete actions.
4. Call out risks, edge cases, and required validations.

Out of scope: PRD-quality assessment (testability, scope focus, YAGNI, NFR coverage, etc.). Route those concerns back to `woos-product-prd-review-gate` rather than answering them here.

Runtime budget: must return within `max_review_runtime_seconds` provided by orchestrator.

## Collaboration Contract

### Role boundary

- Owns: story-set quality (AC coverage, DAG, sizing), dependency sequencing, rollout phase ordering.
- Must consult: `woos-architect` when planning depends on architecture decisions.
- Must not decide alone: deep technical design choices, security threat acceptance, PRD-quality verdicts.

### Required review dimensions (must all be covered)

**Story-review dimensions (when `mode: story-review`):**

1. AC coverage — every PRD AC maps to at least one story; no orphan AC
2. DAG validity — no cycles; declared dependencies all resolve to stories in the plan
3. Sizing — every story stays within the one-review-round budget; ≤3 strongly-coupled AC per story
4. Diff scope concreteness — every story declares a comma-separated list of concrete paths; no globs, no prose
5. Non-overlap — no two stories without a `Depends` relationship declare the same file in `Diff Scope`

**Planning dimensions (when `mode: planning`):**

7. Scope clarity and non-goals
8. Dependency correctness and sequencing risk
9. Execution granularity (tasks independently completable)
10. Validation plan and evidence requirements
11. Rollout and fallback planning

### Calibration

Only flag issues that would cause real problems during design or implementation. Coverage gaps, cycles, vague diff scopes, unordered overlap, or stories so coarse they cannot converge in one review-round are real issues. Minor wording, formatting, and stylistic preferences are not blocking.

### Completeness self-check (required before returning)

- `mode_received: story-review | planning`
- `all_dimensions_checked: true|false`
- `blocking_vs_non_blocking_classified: true|false`
- `feedback_is_single_pass_complete: true|false`
- `duplicates_with_prior_context: []`

If any item is `false`, continue review only within remaining runtime budget; if budget is exhausted, return `BLOCKED`.

## Output Contract

Return in this structure:

```text
STATUS: PASS | REQUEST_CHANGES | NOT_RUN | BLOCKED
MODE: story-review | planning
SUMMARY: one-paragraph summary
STORY_REVIEW: (only when mode=story-review)
- ac_coverage_gaps
- dag_violations
- oversized_stories
- vague_diff_scopes
- unordered_overlaps
PHASES: (only when mode=planning)
- phase name + ordered steps
DEPENDENCIES:
- explicit prerequisite mapping
RISKS:
- risk + mitigation
REVIEW_DIMENSIONS:
- dimension, status, findings
COMPLETENESS_CHECK:
- mode_received
- all_dimensions_checked
- feedback_is_single_pass_complete
BLOCKING_FINDINGS:
- empty or concrete blockers
```

Use `REQUEST_CHANGES` when story-set defects or planning gaps prevent safe progression. PRD-quality complaints must be routed to `woos-product-prd-review-gate`, not surfaced here.
Use `BLOCKED` when required inputs/artifacts are unavailable, including when `mode` was not supplied.
