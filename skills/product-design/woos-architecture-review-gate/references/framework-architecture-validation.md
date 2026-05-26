# Architecture Validation Framework

## Purpose

Validate that a system architecture document is coherent, complete, and ready to guide implementation. Identify gaps before engineering begins.

## Input

- Architecture document (components, decisions, patterns, project structure)
- PRD (functional and non-functional requirements for coverage checking)
- Epics (if available — for mapping requirements to implementation)

## Methodology

### 1. Coherence Validation

Check that all architectural decisions work together without contradictions:

**Decision Compatibility:**
- Do all technology choices work together without conflicts?
- Are all versions compatible with each other?
- Do patterns align with technology choices?
- Are there any contradictory decisions?

**Pattern Consistency:**
- Do implementation patterns support the architectural decisions?
- Are naming conventions consistent across all areas?
- Do structure patterns align with technology stack?
- Are communication patterns coherent?

**Structure Alignment:**
- Does the project structure support all architectural decisions?
- Are boundaries properly defined and respected?
- Does the structure enable the chosen patterns?
- Are integration points properly structured?

### 2. Requirements Coverage Validation

Verify all project requirements are architecturally supported:

**Functional Requirements:**
- Does every FR have architectural support?
- Are all FR categories fully covered by architectural decisions?
- Are cross-cutting FRs (auth, logging, error handling) properly addressed?
- Are there any missing architectural capabilities?

**Epic/Feature Coverage (if epics exist):**
- Does every epic have architectural support?
- Are all user stories implementable with these decisions?
- Are cross-epic dependencies handled architecturally?

**Non-Functional Requirements:**
- Are performance requirements addressed architecturally?
- Are security requirements fully covered?
- Are scalability considerations properly handled?
- Are compliance requirements architecturally supported?

### 3. Implementation Readiness Validation

Assess if AI agents can implement consistently from this architecture:

**Decision Completeness:**
- Are all critical decisions documented with specific versions?
- Are implementation patterns comprehensive enough?
- Are consistency rules clear and enforceable?
- Are examples provided for major patterns?

**Structure Completeness:**
- Is the project structure complete and specific?
- Are all files and directories defined?
- Are integration points clearly specified?
- Are component boundaries well-defined?

**Pattern Completeness:**
- Are all potential conflict points addressed?
- Are naming conventions comprehensive?
- Are communication patterns fully specified?
- Are process patterns (error handling, etc.) complete?

### 4. Gap Analysis

Classify findings by severity:

**Critical Gaps** — blocks implementation:
- Missing architectural decisions needed for core features
- Incomplete patterns that could cause conflicts
- Missing structural elements needed for development
- Undefined integration points between components

**Important Gaps** — causes rework or confusion:
- Areas needing more detailed specification
- Patterns that could be more comprehensive
- Documentation holes that will generate questions

**Minor Gaps** — nice to have:
- Additional patterns that would be helpful
- Supplementary documentation
- Tooling and workflow recommendations

## Output Structure

```markdown
# Architecture Validation Results

## Coherence Validation ✅/❌
**Decision Compatibility:** [assessment]
**Pattern Consistency:** [assessment]
**Structure Alignment:** [assessment]

## Requirements Coverage ✅/❌
**FR Coverage:** [X of Y FRs have architectural support]
**NFR Coverage:** [assessment]

## Implementation Readiness ✅/❌
**Decision Completeness:** [assessment]
**Structure Completeness:** [assessment]
**Pattern Completeness:** [assessment]

## Gap Analysis
### Critical
[list or "None"]
### Important
[list or "None"]
### Minor
[list or "None"]

## Architecture Completeness Checklist
**Requirements Analysis**
- [ ] Project context thoroughly analyzed
- [ ] Scale and complexity assessed
- [ ] Technical constraints identified
- [ ] Cross-cutting concerns mapped

**Architectural Decisions**
- [ ] Critical decisions documented with versions
- [ ] Technology stack fully specified
- [ ] Integration patterns defined
- [ ] Performance considerations addressed

**Implementation Patterns**
- [ ] Naming conventions established
- [ ] Structure patterns defined
- [ ] Communication patterns specified
- [ ] Process patterns documented

**Project Structure**
- [ ] Complete directory structure defined
- [ ] Component boundaries established
- [ ] Integration points mapped
- [ ] Requirements-to-structure mapping complete

## Architecture Readiness Assessment
**Status:** [READY / READY WITH MINOR GAPS / NOT READY]
- READY: All 16 checklist items checked, no critical gaps
- READY WITH MINOR GAPS: No critical gaps, some items unchecked
- NOT READY: Critical gaps exist or Requirements/Decisions items unchecked

**Key Strengths:** [list]
**Recommendations:** [ordered actions to reach READY if not already]
```

## Quality Criteria

- All three validation dimensions assessed (coherence, coverage, readiness)
- Every gap has a severity classification
- Checklist is honest (only mark [x] when actually validated, not assumed)
- Status reflects checklist state (don't claim READY with unchecked items)
- Specific enough that an engineer reading the report knows exactly what's missing
