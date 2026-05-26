# System Architecture Framework

## Purpose

Produce a high-level system architecture that spans all planned versions. Define component boundaries, communication patterns, data architecture, and key technical decisions with rationale.

## Input

- Product roadmap (vision, versioned scope, constraints)
- Technical preferences from idea capture (if any — treat as input, not constraint)
- Research findings (technical feasibility, existing solutions)

## Methodology

### 1. Requirements Extraction

From the roadmap, extract:
- **Functional requirements** — what the system must do (features → capabilities)
- **Non-functional requirements** — performance, security, scalability, reliability targets
- **Cross-cutting concerns** — auth, logging, error handling, deployment
- **Complexity indicators** — real-time features, multi-tenancy, regulatory needs, integration depth

### 2. Scale Assessment

Classify the project:
- **Solo/hobby**: Single developer, minimal infrastructure, optimize for simplicity
- **Small team**: 2-5 developers, moderate infrastructure, optimize for developer productivity
- **Production**: Multiple teams, robust infrastructure, optimize for reliability and scalability

This determines architectural complexity budget — don't over-architect for scale you won't reach.

### 3. Core Architectural Decisions

For each decision, document: **Choice + Alternatives Considered + Rationale**

**A. Component Architecture**
- What are the major system components/services?
- What is each component's single responsibility?
- Where are the boundaries? (If a component has >1 responsibility, split it)

**B. Communication Patterns**
- How do components talk? (REST API, gRPC, message queue, shared DB, events)
- Pick ONE primary pattern; justify exceptions explicitly
- Synchronous vs. asynchronous for each communication path

**C. Data Architecture**
- What storage types? (relational, document, cache, file, search)
- How does data flow between components?
- Where is the source of truth for each data entity?
- Introduce API boundaries between components sharing raw data

**D. Infrastructure & Deployment**
- How is it deployed? (containers, serverless, bare metal)
- What's the minimum viable infrastructure for V1?
- What infrastructure is NOT needed until V2+? (remove premature complexity)

### 4. Implementation Patterns

Define consistency rules that prevent implementation conflicts:
- Naming conventions (files, APIs, database tables)
- Error handling patterns (how errors propagate, what gets logged)
- Authentication/authorization approach
- Testing strategy (unit, integration, e2e boundaries)

### 5. Version Alignment

Map architecture to roadmap versions:
- **V1 architecture**: Minimum components needed. Can be built independently.
- **V2 additions**: What new components/services appear? How do they connect?
- **Migration path**: How does V1 architecture evolve to V2 without rewrite?

### 6. Risk Assessment

For each significant technical risk:
- What could go wrong?
- What's the impact if it happens?
- What's the concrete mitigation action? (not just "monitor")
- What's the fallback plan?

## Output Structure

```markdown
# [Project] — System Architecture

## Architecture Overview
[1-2 paragraph summary of the approach]

## System Components
### [Component 1]
- **Responsibility**: [single responsibility]
- **Technology**: [language/framework]
- **Interfaces**: [what it exposes, what it consumes]

### [Component 2]
...

## Communication Architecture
[Diagram description or table showing component interactions]
| From | To | Pattern | Protocol | Notes |
|------|-----|---------|----------|-------|

## Data Architecture
### Storage
| Data Entity | Storage Type | Owner Component | Access Pattern |
|-------------|-------------|-----------------|----------------|

### Data Flow
[How data moves through the system]

## Infrastructure
### V1 (Minimum Viable)
[What's needed to ship V1]

### V2+ (When Needed)
[What gets added and what triggers it]

## Implementation Patterns
- Naming: ...
- Error handling: ...
- Auth: ...
- Testing: ...

## Architecture Decisions
| Decision | Alternatives | Rationale |
|----------|-------------|-----------|

## Technical Risks
| Risk | Impact | Mitigation | Fallback |
|------|--------|-----------|----------|

## Version Alignment
| Component | V1 | V2 | V3 |
|-----------|----|----|-----|
```

## Quality Criteria

- Components have clear single responsibilities (not "backend" or "services")
- ONE primary communication pattern with justified exceptions
- No infrastructure that isn't needed until V2 (proportional complexity)
- Every dependency can be built independently (or explicitly marked as sequential)
- Risks have concrete mitigation actions, not "we'll figure it out"
- Architecture aligned to roadmap versions — V1 components are V1-scoped
- Technical preferences from user considered and either adopted with rationale or explicitly diverged with explanation
