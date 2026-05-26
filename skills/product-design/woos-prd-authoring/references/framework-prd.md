# PRD Authoring Framework (Per-Feature)

## Purpose

Write a detailed Product Requirements Document for a specific feature within an existing product roadmap. This is per-feature PRD authoring, not greenfield product definition.

## Input

- Product roadmap (versioned scope, personas, success metrics)
- System architecture (components, boundaries, constraints)
- Feature scope from roadmap (which feature this PRD covers)

## Methodology

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

**Describe capabilities, not implementation:**
- ✅ "System SHALL authenticate users via email + password"
- ❌ "Implement bcrypt hashing with salt rounds = 12"
- Technical HOW belongs in architecture/design docs, not PRD

**Be specific:**
- ✅ "Search results SHALL appear within 200ms (p95)"
- ❌ "Search should be fast"
- ✅ "System SHALL support 1000 concurrent users"
- ❌ "System should be scalable"

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

Use the PRD template (`references/template-prd-template.md`) as the structural guide. Key sections:

```markdown
# [Feature Name] — PRD

## Background & Context
[Why this feature, why now, what problem it solves]

## User Personas
[Which personas from roadmap are relevant to this feature]

## User Journeys
### Journey 1: [Protagonist Name] — [Scenario]
1. [Step]
2. [Step]
3. [Climax — the moment of value delivery]

## Functional Requirements
### FR-1: [Capability]
[Description + acceptance criteria]

### FR-2: [Capability]
...

## Non-Functional Requirements
### NFR-1: [Quality attribute]
[Measurable target]

## Edge Cases
| Scenario | Expected Behavior |
|----------|------------------|

## Success Metrics
- Primary: [metric + target]
- Counter-metric: [what shouldn't degrade]
- Leading indicator: [early signal]

## Open Questions
[Things that need answers before implementation]
```

## Quality Criteria

- Every FR is testable (can write acceptance criteria)
- No implementation details leaked into requirements
- Edge cases identified for all major flows
- Metrics have specific numbers, not qualitative words
- Feature boundary is clear — adjacent features not conflated
- Dependencies on other features explicitly stated
