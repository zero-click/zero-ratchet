# PRD: <Feature Name>

**Version**: <version>
**Created**: <date>
**Based on**: `docs/prd/<version>/<feature>-requirements.md`
**Status**: Draft | Reviewed | Approved

## Background

Why this feature exists. Link to roadmap context and problem statement.

## User Personas

| Persona | Description | Primary Need |
|---------|-------------|--------------|
| [Name] | [Who they are] | [What they need] |

## Functional Requirements

### FR-1: <Capability>

[Description of what the system must do]

**Acceptance Criteria:**
- Given [context], When [action], Then [expected result]
- Given [context], When [action], Then [expected result]

**User value:** [Why this matters to the user]

### FR-2: <Capability>

[Description]

**Acceptance Criteria:**
- Given [context], When [action], Then [expected result]

**User value:** [Why this matters]

## Non-Functional Requirements

- **Performance**: [NEEDS CLARIFICATION: latency target?] or [specific target, e.g. p95 < 200ms]
- **Scale**: [expected load / data volume]
- **Security**: [auth, data sensitivity, compliance]
- **Accessibility**: [WCAG level or N/A]

## User Flows

### Flow 1: <Happy Path Name>

```
[Start State] → [Action] → [Screen/State] → [Action] → [End State]
```

### Flow 2: <Error Path>

```
[Start State] → [Action] → [Error] → [Recovery] → [End State]
```

## Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Empty state (no data) | [What shows] |
| Network error | [What happens] |
| Concurrent access | [How resolved] |
| [NEEDS CLARIFICATION: ...] | [Decision pending] |

## Non-Goals

- [Explicitly excluded — carried from requirements]

## Dependencies

- [Dependency on other feature or service — or "none"]

## Open Questions

- [Unresolved question] — [NEEDS CLARIFICATION: impact if unresolved]

## Success Metrics

- [Measurable outcome that proves this feature works]
- [User behavior signal or business metric]
