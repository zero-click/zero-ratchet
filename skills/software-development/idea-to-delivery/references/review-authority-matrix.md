# Review Authority Matrix

## Conflict Resolution

When multiple reviewers disagree, resolve by domain authority.

## Authority Order

| Domain | Authority | Reason |
|--------|-----------|--------|
| Security vulnerabilities | `security-reviewer` | Security has highest blast radius |
| Architecture decisions | `architect` | Architecture is structural foundation |
| Product/requirements | `product-planner` | Product owns scope and priorities |
| Code quality | `code-reviewer` | Code quality is craft domain |
| Handoff quality | `architect` (Strict) | Architecture review covers handoff completeness |
| Cross-domain conflicts | Lowest-risk path | Evidence over opinion |

## Resolution Protocol

1. Identify which domain the conflict belongs to
2. The authority for that domain has the final say
3. Record the decision with rationale in review context
4. Both reviewers see the resolution

## Cross-Domain Conflicts

When a conflict spans multiple domains (e.g., security vs. product):

1. **Default to lowest-risk path** — the option with fewer potential failures
2. **Evidence over opinion** — data beats preference
3. **If still tied** — escalate to human via `woos-human-handoff`

## Finding Lifecycle

Review findings have three states:

- **open** — unresolved, blocks progression
- **resolved** — addressed, verified
- **reopened** — was resolved but issue recurred

Each finding has a unique ID for cross-gate tracking via `woos-review-context`.

## Review Round Limits

| Parameter | Value |
|-----------|-------|
| Max review rounds per gate | 2 |
| Max reconciliation attempts per round | 1 |
| Exceeded | BLOCKED → escalate to human |

## Reviewers by Gate

| Gate | Lite | Standard | Strict |
|------|------|----------|--------|
| PRD Review (Phase 3R) | Skip | product-planner | product-planner + architect |
| Design Review (Phase 4R) | Skip | architect | architect + API review |
| Handoff Readiness (Phase 5R) | Skip | Self-check checklist | architect (independent dispatch) |
| Code Review (Phase 9) | Self-review | code-reviewer | code-reviewer + security-reviewer |

## DCR Assessment

When a DCR (Design Change Request) is submitted by coding agent:

| DCR Priority | Assessment Path |
|--------------|----------------|
| Blocking | Research agent assesses immediately |
| Important | Research agent assesses within current phase |
| Nice to have | Research agent records; may defer |

DCR resolution authority follows the same domain matrix:
- Architecture-related DCR → architect decides
- Product/requirements DCR → product-planner decides
- Cross-domain → lowest-risk path
