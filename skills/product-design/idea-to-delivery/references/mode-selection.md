# Mode Selection Guide

## Decision Tree

```
START
  │
  ├─ Is it a typo, docs fix, or trivial change?
  │   └─ YES → No workflow needed. Just do it.
  │
  ├─ Is it a pure bugfix with clear reproduction and low risk?
  │   └─ YES → woos-development-workflow Lite
  │            (no idea-to-delivery needed)
  │
  ├─ Is it security-sensitive or compliance-required?
  │   └─ YES → STRICT
  │
  ├─ Is it a major architecture change (new service, DB migration, API redesign)?
  │   └─ YES → STRICT
  │
  ├─ Is it a normal feature (multi-file, cross-component, needs design)?
  │   └─ YES → STANDARD
  │
  ├─ Is it scope-clear, single-purpose, low risk?
  │   └─ YES → LITE
  │
  └─ Unsure?
      └─ DEFAULT → STANDARD
```

## Tier Comparison

| Dimension | Lite | Standard | Strict |
|-----------|------|----------|--------|
| **Scope** | Small, clear | Multi-file feature | Major/critical |
| **Risk** | Low | Moderate | High |
| **Research** | Skip | search-first | deep-research |
| **PRD** | Merged with design | Full PRD | Full PRD + Requirement Contract |
| **PRD Review** | Skip | product-planner | product-planner + architect |
| **Design** | Merged with PRD | Full design | Full design + Capability Contract |
| **Design Review** | Skip | architect | architect + API review |
| **Handoff Template** | 4 fields (Mission, Tasks, AC, Verification) | Full 12 sections | Full 12 + optional sections |
| **Handoff Readiness** | Skip | Self-check checklist | Independent architect review |
| **Constitution** | Skip (optional) | Reference if exists | MUST exist + reference |
| **Delta Annotations** | Yes (still apply) | Yes | Yes (mandatory) |
| **Code Review** | Self-review | code-reviewer | code-reviewer + security-reviewer |
| **DCR Feedback Loop** | Skip (handle inline) | Available | Mandatory for deviations |
| **TDD** | Optional | Recommended | Required |
| **Acceptance Gate** | Skip | Skip | Executable acceptance |
| **Deviation Control** | Skip | Skip | Required |
| **Workflow Memory** | Skip | Skip | Required |

## What Each Tier Skips

### Lite skips:
- Research pass
- Independent PRD review gate
- Independent design review gate
- Handoff Readiness Gate
- Independent code review gate
- DCR feedback loop (handle small deviations inline)
- Executable acceptance gate
- Deviation control gate
- Workflow memory update
- Constitution creation (optional)

### Standard skips:
- Requirement contract
- Capability contract
- API design review (unless REST/GraphQL)
- Browser QA (unless frontend)
- Executable acceptance gate
- Deviation control gate
- Workflow memory update
- Independent Handoff Readiness reviewer (uses self-check instead)

### Strict skips:
- Nothing. All gates active.

## Override

User can say `GREENLIGHT NEXT STAGE` to:
- Skip remaining interview questions in idea capture
- Bypass optional exploration in research pass

Override does NOT skip review gates. Gate PASS is always required.
