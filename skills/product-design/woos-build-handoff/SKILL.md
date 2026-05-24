---
name: woos-build-handoff
description: Package product artifacts (PRD + UI brief) into a single handoff file that a fresh coding agent can use to implement independently. Supports Lite (4-field) and Standard (full) templates. Includes spec versioning, Delta annotations, DCR Protocol, and Git Branch field. Product-focused — technical design is engineering's job.
version: 3.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [handoff, build, implementation, agent-bridge, delivery, delta]
    related_skills:
      - woos-product-design-flow
      - woos-ui-design-brief
      - woos-development-workflow
---

# Build Handoff

## Purpose

Synthesize product artifacts (PRD, UI brief) into a single, self-contained handoff file. This file is the contract between the research agent and the coding agent — it defines WHAT to build and WHY. Technical decisions (architecture, data model, API design) are the coding agent's responsibility.

## When to Use

Use when:

- PRD has passed review (or Lite mode: brief PRD is complete)
- UI brief is complete (if applicable)
- Ready to hand off to the coding agent

Skip when:

- PRD is not written yet → run woos-product-design-flow first
- PRD has not passed review → complete review gate first

## Input Artifacts

| Artifact | Required | Source |
|----------|----------|--------|
| PRD | Yes | `woos-product-design-flow` → `docs/prd/<version>/<feature>.md` |
| UI Brief | Optional | `woos-ui-design-brief` → `docs/design/<version>/<feature>-ui-brief.md` |
| Research notes | Optional | `docs/research/<topic>.md` |
| Idea capture | Optional | `ideas/<slug>/00-idea-capture.md` |

In Lite mode, PRD is abbreviated (user stories + AC only).

## Output

File: `docs/handoff/<version>/<feature>.md`

## Template Selection by Mode

### Lite Template (4 fields)

For Lite mode only. Minimal but sufficient for small, clear-scope work.

```markdown
---
spec-version: 1.0
---

# <Feature Name> — Build Handoff

## Mission
One sentence: what to build.

## Build Tasks

### Task 1: [ADDED] <Small objective>
- Steps:
  1. [step]
  2. [step]
- Verification: [test command or check]

### Task 2: [ADDED] <Another objective>
- Steps:
  1. [step]
- Verification: [test command or check]

## Acceptance Criteria
- Given [context], When [action], Then [expected result]
- Given [context], When [action], Then [expected result]

## Verification Commands
\`\`\`bash
<test command>
\`\`\`
```

**Lite rules:**
- Only these 4 sections: Mission, Build Tasks, Acceptance Criteria, Verification Commands
- No Constitution reference (unless project has one and it's relevant)
- No spec `based-on` header (Lite is typically greenfield)
- Delta annotations still apply: `[ADDED]`/`[MODIFIED]`/`[REMOVED]`

### Standard Template (10 sections)

For Standard mode. Full handoff with all required fields.

```markdown
---
spec-version: 1.0
based-on: (empty for first version, or path to previous handoff)
git-branch: feature/<feature-slug>  (recommended)
---

# <Feature Name> — Build Handoff

## Mission
One sentence: what to build and why.

## Product Vision
Why we're building this, who it's for, what experience to deliver.
Source: PRD §Background + §Problem Statement.

## Non-Negotiable Requirements
- [requirement 1 — must satisfy, testable]
- [requirement 2 — must satisfy, testable]
Source: PRD §Functional Requirements + §Acceptance Criteria.

## Out of Scope
- [explicitly excluded 1]
- [explicitly excluded 2]
Source: PRD §Non-Goals + §Scope.

## User Flows
- Flow 1: [start state] → [action] → [end state]
- Flow 2: [start state] → [action] → [end state]
Source: PRD §User Stories.

## UI Direction (if applicable)
- Key screens and their purposes
- Visual direction summary
- Important states (empty, loading, error, success)
Source: UI Design Brief (if exists).

## Build Tasks

### Task 1: [ADDED] <Small objective>
- Objective: [what to accomplish]
- User story: [which requirement this satisfies]
- Steps:
  1. [step]
  2. [step]
- Verification: [test command or check]
- Expected result: [observable outcome]

### Task 2: [MODIFIED] <Existing component>
- What changes: [description]
- Steps:
  1. [step]
- Verification: [test command or check]
- Expected result: [observable outcome]

## Acceptance Criteria
- Given [context], When [action], Then [expected result]
- Given [context], When [action], Then [expected result]
Source: PRD §Acceptance Criteria.

## Verification Commands
\`\`\`bash
# Run all tests
<test command>

# Run linting
<lint command>

# Build check
<build command>
\`\`\`

## Open Questions
- [unresolved question] — [impact if unresolved]
- NOTE: Technical architecture decisions are the coding agent's responsibility

## DCR Protocol

When a product assumption is discovered to be incorrect during implementation:

1. Write `docs/feedback/<feature>-dcr.md` with:
   - Issue: description of the product problem
   - Impact: affected scope, risk level (Low / Medium / High)
   - Proposed Resolution: suggested fix
   - Priority: Blocking / Important / Nice-to-have

2. Research agent assesses:
   - Small change → update handoff directly, notify coding agent
   - Large change → roll back to PRD or UI brief for re-review

3. Resolution recorded in DCR file.
```

### Strict Template

Same as Standard template, plus add these sections when applicable:

```markdown
## Security Requirements
## Platform Targets
## Integrations (third-party services)
## UI Design Brief (reference to external mockups/brief)
## Rollout Plan
## Rollback Plan
```

**Strict rules:**
- All Build Tasks MUST have Delta annotations
- `based-on` header required for iteration handoffs
- Security Requirements section mandatory

## Delta Annotation Guide

Every Build Task title MUST be prefixed with one of:

| Prefix | Meaning | When to use |
|--------|---------|-------------|
| `[ADDED]` | New functionality, new files | First delivery; genuinely new features |
| `[MODIFIED]` | Changes to existing code | Iterations, enhancements to existing features |
| `[REMOVED]` | Deleting code/files | Deprecation, cleanup, feature removal |

**Rules:**
- First full delivery: all tasks are `[ADDED]`
- Iteration handoffs: mark each task based on actual change type
- A task can only have one prefix
- Coding agent uses this to know: new file? edit existing? delete?

## Spec Versioning

Every handoff file includes:

```yaml
spec-version: 1.0          # Current version of this handoff
based-on: (path or empty)  # Previous handoff version (for iterations)
```

- First handoff: `spec-version: 1.0`, `based-on:` (empty)
- Iteration: `spec-version: 1.1`, `based-on: docs/handoff/v1/feature.md`
- Major redesign: `spec-version: 2.0`

## DCR Protocol (in Handoff)

Every Standard and Strict handoff MUST include a DCR Protocol section so the coding agent knows how to feed design issues back to the research agent.

The DCR Protocol section in the handoff file should contain:

```markdown
## DCR Protocol

When a design issue is discovered during implementation:

1. Write `docs/feedback/<feature>-dcr.md` with:
   - Issue: description of the design problem
   - Impact: affected scope, risk level (Low / Medium / High)
   - Proposed Resolution: suggested fix
   - Priority: Blocking / Important / Nice-to-have

2. Research agent assesses:
   - Small change → update handoff directly, notify coding agent
   - Large change → roll back to PRD or Design step for re-review

3. Resolution recorded in DCR file; review context updated.
```

Lite handoffs do NOT include DCR Protocol (small deviations handled inline).

## Git Branch Field (in Handoff)

Standard and Strict handoffs SHOULD include a Git Branch field in the YAML frontmatter:

```yaml
---
spec-version: 1.0
based-on:
git-branch: feature/<feature-slug>
---
```

If not specified, the coding agent creates its own branch following project conventions.

## Handoff Quality Checklist

Before finalizing the handoff, verify:

1. **Self-contained**: A fresh coding agent with NO prior context can understand and implement everything
2. **No dangling references**: Every referenced file/path exists or will be created
3. **Testable AC**: Every acceptance criterion is machine-checkable
4. **No ambiguity**: Tasks are concrete, not "handle edge cases" — specify which cases
5. **Phases ordered**: Dependencies between tasks are clear
6. **Verification defined**: Each task has a clear "done" check
7. **Delta annotations**: Every Build Task has `[ADDED]`/`[MODIFIED]`/`[REMOVED]` prefix
8. **Spec versioning**: `spec-version` header present; `based-on` set for iterations
9. **Product-only**: No technical architecture decisions — leave those for engineering
10. **UI direction**: If feature has UI, reference UI brief or provide direction summary

## Anti-Patterns to Avoid

- **Vague tasks**: "Implement the feature" → too broad; break into specific objectives
- **Missing context**: Assuming the coding agent knows project conventions → state requirements explicitly
- **PRD copy-paste**: Don't just copy the PRD; transform requirements into buildable tasks
- **Missing verification**: Every task needs a test command or observable check
- **Missing Delta annotations**: Without `[ADDED]`/`[MODIFIED]`/`[REMOVED]`, coding agent doesn't know intent
- **Prescribing architecture**: Don't dictate data models, API shapes, or tech stack — that's engineering's job
- **Over-specification**: Define outcomes, not implementation steps

## File Location

`docs/handoff/<version>/<feature-slug>.md`

Slug: lowercase, hyphens, matches PRD/design slug. Version matches the roadmap version (e.g., `v1`, `v2`).

## Handoff to Coding Agent

The handoff file is the input to the engineering stage. The coding agent:

1. Reads the handoff file
2. Designs technical architecture (data model, API, etc.)
3. Creates/updates Constitution if needed
4. Breaks tasks into implementation steps based on Delta annotations
5. Implements and verifies against acceptance criteria
6. If product assumption is wrong → writes DCR to `docs/feedback/<feature>-dcr.md`

Technical decisions (architecture, data model, API design) are made by the coding agent — NOT prescribed in the handoff.
