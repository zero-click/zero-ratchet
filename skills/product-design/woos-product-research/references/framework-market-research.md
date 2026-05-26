# Market Research Framework

## Purpose

Investigate the competitive landscape, technical feasibility, and existing solutions to inform product decisions. Produce a structured research document with verified findings and clear recommendations.

## Input

- Idea capture document (problem statement, target users, constraints)
- Any existing research or competitor references from the user

## Methodology

### 1. Scope Clarification

Before researching, clarify:
- **Core question**: What exactly needs to be answered?
- **Research goals**: What decisions will this research inform?
- **Boundaries**: What's in scope vs. out of scope?
- **Depth vs. breadth**: Deep dive on one area, or survey across many?

### 2. Multi-Angle Research (execute in parallel)

**A. Market Landscape**
- Who are the existing players? (direct competitors, adjacent products, open-source alternatives)
- What's their positioning? (enterprise vs. developer vs. consumer)
- What's the market trajectory? (growing, consolidating, fragmenting)

**B. Technical Feasibility**
- What technology approaches exist for this problem?
- What are the proven patterns vs. experimental ones?
- What are the hard technical constraints or risks?

**C. Existing Solutions & Reusable Components**
- What can be reused vs. must be built from scratch?
- Are there open-source foundations to build on?
- What integration points exist with the user's current stack?

### 3. Synthesis

- Cross-reference findings across angles
- Identify patterns (multiple sources saying the same thing = strong signal)
- Surface contradictions (one source says X, another says Y = needs resolution)
- Extract actionable recommendations

## Output Structure

```markdown
# [Topic] Research

## Executive Summary
[2-3 sentence overview of key findings and recommendation]

## Market Landscape
### Key Players
[Table: Name | Category | Positioning | Strengths | Weaknesses]

### Market Dynamics
[Growth trends, consolidation, emerging segments]

## Technical Feasibility
### Proven Approaches
[What works today, with evidence]

### Risks & Unknowns
[What's uncertain, what could go wrong]

## Existing Solutions Analysis
### Reusable Components
[What exists that can be leveraged]

### Build vs. Buy Assessment
[What must be custom vs. what's available]

## Recommendations
[Concrete next steps based on findings]

## Sources
[All URLs and references cited]
```

## Quality Criteria

- Every factual claim has a cited source
- Recommendations are actionable (not just "consider X")
- Critical unknowns are explicitly flagged as blockers
- Research answers the original scope questions (trace back to goals)
- No hallucinated competitor names or features — verify everything
