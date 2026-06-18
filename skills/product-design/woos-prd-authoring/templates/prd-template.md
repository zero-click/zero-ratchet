# PRD: <Feature Name>

**Version**: <version>
**Created**: <date>
**Based on**: `docs/product/<project>-roadmap.md` (or Lite idea capture)
**Status**: Draft | Reviewed | Approved

## Background

**Shape:** [internal-tool / single-operator / CLI | consumer-product / multi-stakeholder | other — required; the review gate keys conditional sections off this]

Why this feature exists. Link to roadmap context and problem statement.

[State the real problem in plain language before describing the solution shape. Separate: (1) observable problem, (2) root cause or mismatch if known, (3) current workaround, and (4) user/operator impact. If a concrete channel, environment, or path exposed the issue, clarify whether it is the problem itself or merely the example that revealed the general problem.]

## Goals

- [Goal 1 — measurable product outcome this feature should move]
- [Goal 2 — measurable product outcome this feature should move]

## User Personas *(conditionally required — include when shape is `consumer-product` / `multi-stakeholder` or the feature has user-facing UI / multiple distinct user types; omit entirely for `internal-tool` / `single-operator` / `CLI` rather than write a one-row placeholder)*

| Persona | Description | Primary Need |
|---------|-------------|--------------|
| [Name] | [Who they are] | [What they need] |

## Functional Requirements

### FR-1: <Capability>

[Description of one capability or one relationship the system must make true. Avoid combining multiple concerns such as precedence, routing, observability, fallback behavior, and policy boundaries in one FR.]

**Acceptance Criteria:**
- Given [context], When [action], Then [expected result]
- Given [context], When [action], Then [expected result]

**Consequences (testable):**
- [Specific atomic condition with a concrete threshold or observable outcome, e.g. "System returns HTTP 429 when request rate exceeds 100/sec per merchant."]
- [Another specific testable condition. Avoid "system handles X gracefully" or "reasonable performance" — those are not consequences.]

**Out of Scope:** *(optional — what this FR explicitly does NOT cover)*
- [Adjacent capability that could be confused with this FR but is deliberately excluded]

**User value:** [Why this matters to the user]

### FR-2: <Capability>

[Description]

**Acceptance Criteria:**
- Given [context], When [action], Then [expected result]

**Consequences (testable):**
- [Atomic, measurable condition]

**User value:** [Why this matters]

## Non-Functional Requirements

- **Performance**: [NEEDS CLARIFICATION: latency target?] or [specific target, e.g. p95 < 200ms]
- **Scale**: [expected load / data volume]
- **Security**: [auth, data sensitivity, compliance]
- **Accessibility**: [WCAG level or N/A]

## MVP Scope

### In Scope

- [What is in for this version]

### Out of Scope for MVP

- [What is explicitly deferred]
- [Cut-line / deferred adjacent work]

## User Flows *(conditionally required — same condition as `## User Personas`; omit entirely when shape is `internal-tool` / `single-operator` / `CLI`)*

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

## Dependencies *(optional — include only if they matter downstream)*

- [Dependency on other feature or service — or "none"]

## Open Questions *(optional — omit if none)*

- [Unresolved question] — [NEEDS CLARIFICATION: impact if unresolved]

## Assumptions Index *(required if any `[ASSUMPTION]` tags appear inline)*

Every `[ASSUMPTION: ...]` tag used anywhere above must be surfaced here for explicit confirmation. Each entry: section reference + the assumption statement.

- §[X.Y] — [ASSUMPTION restated in one line so a reviewer can confirm or reject it]
- ...

## Success Metrics

At least one **quantitative primary metric with a target value**, AND at least one **counter-metric** (the thing this feature must NOT degrade). Qualitative-only bullets like "users complete without confusion" are not metrics.

- **Primary:** [Measurable outcome with target value, e.g. "P95 envelope-to-handler latency ≤ 2s for X% of events over a 7-day window"]
- **Counter-metric:** [The thing this feature must NOT regress, e.g. "Daemon memory steady-state stays under 200 MB"] or `[NEEDS CLARIFICATION: counter-metric]`
- [Additional supporting signal — optional]
