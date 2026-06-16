# PRD Authoring Framework (Per-Feature)

## Purpose

Write a detailed Product Requirements Document for a specific feature within an existing product roadmap. This is per-feature PRD authoring, not greenfield product definition.

## Input

- Product roadmap (versioned scope, personas, success metrics)
- System architecture (components, boundaries, constraints)
- Feature scope from roadmap (which feature this PRD covers)

## Methodology

### 0. Problem Framing Before PRD Writing

Before filling any PRD section, force the feature into plain language:
- **Observable problem** — what is going wrong today?
- **Affected actor** — who feels it?
- **Root cause / mismatch** — if known, why does it happen?
- **Current workaround** — how is the user/operator coping today?
- **Impact** — what confusion, waste, risk, or failure does the status quo create?

Do not compress these into one overstuffed sentence.

**Guardrails:**
- A concrete example is not automatically the whole problem.  
  - ✅ "Standard egress visibility is unclear; Teams is the current example."
  - ❌ "Teams egress is the problem" when the issue applies to standard egress generally
- A deployment convention is not automatically a contract.  
  - ✅ "The product must explain the relationship between `--config` and `--socket`."
  - ❌ "Config lives under `~/.cos/cos/<name>/...`" unless the product truly requires that path

### 1. Feature Scoping

Before writing requirements:
- **Identify the feature boundary** — what's in, what's explicitly out
- **Map to architecture** — which system components does this feature touch?
- **Identify dependencies** — does this feature require other features to exist first?
- **Clarify the user journey** — what's the end-to-end flow for this feature?

### 2. Requirements Discipline

**Shape requirements correctly:**
- Group by capability, not by implementation layer
- Functional Requirements: numbered with stable IDs (FR-1, FR-2, ...)
- Non-Functional Requirements: separate section (NFR-1, NFR-2, ...)
- Each requirement is TESTABLE — if you can't write an acceptance test, rewrite it
- Each FR should express **one capability or one relationship**. If it mixes cause, precedence, observability, fallback, and exception policy, split it.

**Describe capabilities, not implementation:**
- ✅ "System SHALL authenticate users via email + password"
- ❌ "Implement bcrypt hashing with salt rounds = 12"
- Technical HOW belongs in architecture/design docs, not PRD

**Be specific:**
- ✅ "Search results SHALL appear within 200ms (p95)"
- ❌ "Search should be fast"
- ✅ "System SHALL support 1000 concurrent users"
- ❌ "System should be scalable"

**Prefer relationship statements when ambiguity is the real pain:**
- ✅ "System SHALL show which socket target is used when `--config` is present without `--socket`."
- ✅ "System SHALL define what happens when `--config` and `--socket` are both provided."
- ❌ "System SHALL derive socket from CoS directory" unless that derivation is itself the chosen product rule

### 3. Edge Cases & Error States

For each major flow:
- What happens when input is invalid?
- What happens when a dependency is unavailable?
- What happens at scale limits?
- What happens for first-time vs. returning users?

### 4. Success Metrics

Define how you'll know this feature succeeded:
- **Primary metric**: The ONE number that moves if the feature works
- **Counter-metric**: What you're watching to ensure you didn't break something else
- **Leading indicator**: Early signal before the primary metric moves

## Output Structure

Use `templates/prd-template.md` as the authoring template — it defines the canonical section structure that Step 4 (PRD Review) checks against. `references/template-prd-template.md` is supplemental reading only; when it conflicts with `templates/prd-template.md`, the template wins. Key sections:

```markdown
# [Feature Name] — PRD

## Background
[The real problem in plain language: observable problem, root cause/mismatch if known, workaround, user impact]

## User Personas
[Relevant personas only. Internal tools / single-operator features may keep this extremely lean.]

## Functional Requirements
### FR-1: [Capability or relationship]
[Description + Given/When/Then acceptance criteria + at least one testable Consequences bullet + optional per-FR Out of Scope + user value]

## Non-Functional Requirements
[Performance, scale, security, accessibility — use concrete bounds, not adjectives]

## User Flows
[Operational or user-observable flows. Internal-tool features may keep these minimal.]

## Edge Cases
| Scenario | Expected Behavior |
|----------|------------------|

## Non-Goals
[Explicitly excluded scope]

## Success Metrics
- Primary: [metric + target]
- Counter-metric: [what shouldn't degrade]
- Leading indicator: [early signal]

## Dependencies *(optional)*
[Only if they matter downstream]

## Open Questions *(optional)*
[Only if there are real unresolved decisions]

## Assumptions Index *(required when any inline `[ASSUMPTION]` tag is used)*
[Surface every inline `[ASSUMPTION: ...]` tag here for explicit confirmation]
```

## Quality Criteria

- Background names the real problem plainly before diving into feature structure
- The PRD distinguishes the general problem from the current example that exposed it
- Deployment conventions and examples are not silently promoted to product contract
- Personas and flows are as light or as heavy as the product shape justifies
- Every FR is testable (can write acceptance criteria)
- No implementation details leaked into requirements
- Edge cases identified for all major flows
- Metrics have specific numbers, not qualitative words
- Feature boundary is clear — adjacent features not conflated
- Dependencies on other features explicitly stated
