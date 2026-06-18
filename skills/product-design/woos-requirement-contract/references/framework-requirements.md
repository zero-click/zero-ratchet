# Legacy Requirement Contract Framework (Deprecated)

## Purpose

Historical note only. Hermes no longer uses a standalone per-feature requirements contract in the active flow; BMAD-style single-PRD mode embeds requirements directly in the PRD. Keep this file only to explain older artifacts and migrations.

## Input

- Product roadmap (versioned scope, personas, success metrics) — Standard / Strict
- The idea capture file — Lite
- System architecture (components, boundaries, constraints) — reference for technical feasibility framing only
- Feature scope from roadmap or idea capture (which feature this contract covers)

## Methodology

### 0. Problem Framing Before Requirements

Before writing any goals or user stories, force the problem into plain language:
- **Observable pain** — what goes wrong today?
- **Affected actor** — who feels it?
- **Current workaround** — how do they cope now?
- **Root cause / mismatch** — if known, what actually causes the pain?
- **Cost of the status quo** — what confusion, risk, waste, or failure does this create?

Keep these distinct. Do **not** collapse them into one dense sentence.

**Critical discipline:**
- A current example is not always the problem.  
  - ✅ "Standard egress success is not visible in daemon logs; Teams is the current example that exposed it."
  - ❌ "Teams logging is broken" when the real issue is general egress visibility
- A deployment convention is not always a product contract.  
  - ✅ "The product must explain the relationship between `--config` and `--socket`."
  - ❌ "Config must live under `~/.cos/cos/<name>/...`" unless the feature truly depends on that path shape

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
- Each requirement should express **one capability or one relationship**. If a requirement is trying to express precedence, routing, observability, fallback, and rollout all at once, split it.

**Describe capabilities, not implementation:**
- ✅ "System SHALL authenticate users via email + password"
- ❌ "Implement bcrypt hashing with salt rounds = 12"
- Technical HOW belongs in architecture/design docs, not PRD

**Be specific:**
- ✅ "Search results SHALL appear within 200ms (p95)"
- ❌ "Search should be fast"
- ✅ "System SHALL support 1000 concurrent users"
- ❌ "System should be scalable"

**Prefer relationship statements when the real problem is ambiguity:**
- ✅ "System SHALL make clear which socket target is used when `--config` is provided without `--socket`."
- ✅ "System SHALL state how `--config` and `--socket` interact when both are present."
- ❌ "System SHALL use CoS-directory derivation" unless that derivation is itself the product decision

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

Use `templates/requirements-template.md` as the structural guide. Key sections:

```markdown
# Requirements: [Feature Name]

## Problem Statement
- Affected actor
- Observable problem
- Root cause / mismatch (if known)
- Current workaround
- Cost of the status quo
- Current example (optional)

## Goals
- [Goal 1]
- [Goal 2]

## User Stories
### US-1: [One capability or one relationship]
[As a / I want / so that + Given/When/Then acceptance + at least one testable Consequences bullet + optional per-US Out of Scope]

## Non-Goals
[Explicit exclusions]

## Constraints
[Non-negotiables]

## Risks & Unknowns
[Risks and unresolved blockers]

## Open Questions *(optional)*
[Only if there are real unresolved decisions]

## Assumptions Index *(required when any inline `[ASSUMPTION]` tag is used)*
[Surface every inline `[ASSUMPTION: ...]` tag here for explicit confirmation]

## Priority Ranking
- P0
- P1
- P2
- Cut-line
```

## Quality Criteria

- The Problem Statement clearly separates pain, cause, workaround, and impact
- Examples are labeled as examples, not silently promoted to the whole problem
- Deployment conventions are not smuggled into product contract unless intentional
- Every user story expresses one capability or one relationship
- Acceptance criteria are testable
- No implementation details leaked into requirements
- Feature boundary is clear — adjacent features not conflated
- Priorities and cut-line are explicit
