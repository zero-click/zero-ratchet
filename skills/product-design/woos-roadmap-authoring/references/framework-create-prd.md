# PRD Creation Framework

## Purpose

Synthesize research findings, pain points, and competitive analysis into a product roadmap document that defines vision, scope, versioning, and success metrics.

## Input

- Idea capture document (problem, users, constraints)
- Research document (market landscape, technical feasibility)
- Problem validation (pain points, evidence, verdict)
- Competitive analysis (if available)

## Methodology

### 1. Discovery (Synthesize Inputs)

Before writing, extract from all inputs:
- **Core problem statement** — one sentence, grounded in evidence
- **Target users** — specific personas with observed behaviors
- **Value proposition** — what changes for users if this exists
- **Constraints** — what's fixed (tech stack, timeline, budget, team size)
- **Non-goals** — what this explicitly is NOT

### 2. Vision & Differentiation

Articulate:
- **Vision**: Where does this go in 2-3 years? (aspirational but grounded)
- **Differentiation**: "Unlike [X], we [Y] because [Z]" — must be specific
- **Core experience**: What's the one thing users do most often? Nail this.

### 3. Versioned Roadmap

Structure scope into sequential versions:

**V1 (MVP)** — Smallest thing that delivers core value
- Features: [only what's essential to prove the concept]
- Non-goals: [everything else, explicitly stated]
- Success metrics: [measurable, with specific numbers]
- Timeline signal: [what indicates V1 is ready to ship]

**V2** — Expand based on V1 learnings
- Features: [things that depend on V1 validation]
- Trigger: [what V1 signal justifies building V2]

**V3** — Scale / mature
- Features: [nice-to-haves, integrations, polish]

### 4. PRD Discipline

Follow these principles:
- **Shape, don't fill**: Features grouped logically; FRs nested with stable IDs. No template-filling.
- **Capabilities, not implementation**: Describe WHAT, not HOW. Tech choices belong in architecture.
- **Length scales with stakes**: Solo project ≈ 2 pages. Internal tool ≈ 5-8. Launch product = as long as needed.
- **Every metric measurable**: Replace "fast" with "< 200ms p95". Replace "many users" with "> 100 DAU in month 1".
- **Non-goals are concrete**: Not "we won't do bad things" but "we will NOT support offline mode even if users request it, because [reason]".

### 5. Decision Log

Record key decisions made during this process:
- What was decided
- What alternatives were considered
- Why this choice won (evidence-based rationale)

This log is append-only and carries forward through all stages.

## Output Structure

```markdown
# [Project Name] — Product Roadmap

## Vision
[Who it's for, what problem it solves, why it matters]

## Differentiation
Unlike [closest alternative], we [unique value] because [reason].

## User Personas
### [Persona 1]
- Who: [specific description]
- Goal: [what they want to accomplish]
- Pain today: [current situation]

## Core Experience
[The primary user flow in 3-5 steps]

## Versioned Roadmap

### V1 — [Theme]
**Scope**: [feature list]
**Non-goals**: [explicit exclusions with rationale]
**Success Metrics**:
- [Metric 1]: [target number] by [timeframe]
- [Metric 2]: ...

### V2 — [Theme]
**Trigger**: [what V1 signal justifies this]
**Scope**: ...

### V3 — [Theme]
**Scope**: ...

## Constraints
- [Technical constraint and why]
- [Resource constraint and impact]

## Decision Log
| Decision | Alternatives Considered | Rationale |
|----------|------------------------|-----------|
| ... | ... | ... |
```

## Quality Criteria

- Vision is differentiated (not generic "better X")
- V1 scope is shippable alone (doesn't depend on V2)
- Every metric has a specific number and timeframe
- Non-goals are concrete "we will NOT do X even if Y"
- Decision log has real alternatives (not strawmen)
- Personas grounded in observed behavior, not hypothetical "ideal users"
