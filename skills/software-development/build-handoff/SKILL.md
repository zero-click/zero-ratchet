---
name: build-handoff
description: Package PRD + Design into a single handoff file that a fresh coding agent can use to implement independently. Supports Lite (4-field), Standard (full), and Strict (full + extras) templates. Includes spec versioning, Constitution reference, Delta annotations, DCR Protocol, and Git Branch field.
version: 2.1.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [handoff, build, implementation, agent-bridge, delivery, constitution, delta]
    related_skills:
      - feature-design-flow
      - engineering-workflow
      - feature-design
      - woos-prd-authoring
      - woos-feature-design
---

# Build Handoff

## Purpose

Synthesize PRD and Design documents into a single, self-contained handoff file. This file is the contract between the research agent and the coding agent — it must contain everything a fresh coding agent needs to work independently.

## When to Use

Use when:

- PRD has passed review (or Lite mode: PRD+Design merged doc is complete)
- Design has passed review (Standard/Strict modes)
- Ready to hand off to the coding agent

Skip when:

- No design exists yet → run `woos-feature-design` first
- PRD has not passed review (Standard/Strict) → run `woos-prd-review-gate` first

## Input Artifacts

| Artifact | Required | Source |
|----------|----------|--------|
| PRD | Yes | `woos-prd-authoring` → `docs/prd/<feature>.md` |
| Design | Yes (Standard/Strict) | `woos-feature-design` → `docs/design/<feature>.md` |
| Research notes | Optional | `docs/research/<topic>.md` |
| Idea capture | Optional | `ideas/<slug>/00-idea-capture.md` |
| Constitution | If exists | `.hep/constitution.md` |

In Lite mode, PRD and Design are merged into a single document.

## Output

File: `docs/handoff/<feature>.md`

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

### Standard Template (12 sections)

For Standard mode. Full handoff with all required fields.

```markdown
---
spec-version: 1.0
based-on: (empty for first version, or path to previous handoff)
constitution-ref: .hep/constitution.md  (if exists)
git-branch: feature/<feature-slug>  (recommended)
---

# <Feature Name> — Build Handoff

## Mission
One sentence: what to build.

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

## Technical Architecture
- System architecture overview
- Main components and their interactions
- **Only deviations from Constitution** (if constitution exists, link it; don't repeat)
Source: Design §Architecture.

## Data Model
- Entities, fields, relationships
- Storage technology and schema
- Migration notes (if any)
Source: Design §Data Model.

## API Contracts
- Endpoints: method, path, request/response shapes
- Authentication/authorization requirements
- Error response format
Source: Design §Interfaces/API Contracts.

## Implementation Phases

### Phase 1: <Name>
- Goal: [what this phase achieves]
- Tasks:
  1. [task description]
  2. [task description]
- Verification: [how to confirm phase is done]

### Phase 2: <Name>
- Goal: [what this phase achieves]
- Tasks:
  1. [task description]
- Verification: [how to confirm phase is done]

## Build Tasks (granular)

### Task 1: [ADDED] <Small objective>
- Objective: [what to accomplish]
- Files to create/modify:
  - `path/to/file.ext` — [purpose]
- Steps:
  1. [step]
  2. [step]
- Verification: [test command or check]
- Expected result: [observable outcome]

### Task 2: [MODIFIED] <Existing component>
- What changes: [description]
- Files to modify:
  - `path/to/file.ext` — [what changes]
- Steps:
  1. [step]
- Verification: [test command or check]
- Expected result: [observable outcome]

### Task 3: [REMOVED] <Deprecated component>
- What to remove: [description]
- Migration notes: [if applicable]
- Files affected:
  - `path/to/file.ext`
- Verification: [test command or check]

## Acceptance Criteria
- Given [context], When [action], Then [expected result]
- Given [context], When [action], Then [expected result]
Source: PRD §Acceptance Criteria.

## Security Considerations
- Auth requirements
- Data sensitivity
- Input validation needs
Source: PRD §Security + Design §Security.

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

### Strict Template

Same as Standard template, plus add these sections when applicable:

```markdown
## Auth / Secrets / Sharing Model
## Platform Targets
## Hosting / Data Location / Deployment Details
## Integrations (third-party services)
## UI Design Brief (reference to external mockups)
## Capability Contract (reference to capability doc)
## Rollout Plan
## Rollback Plan
```

**Strict rules:**
- Constitution MUST exist and be referenced
- All Build Tasks MUST have Delta annotations
- `based-on` header required for iteration handoffs

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

## Constitution Reference Guide

When `.hep/constitution.md` exists:

```yaml
# In handoff header
constitution-ref: .hep/constitution.md
```

**Technical Architecture section behavior:**
- With constitution: only write DEVIATIONS (e.g., "Using Redis for caching instead of default Cloudflare KV")
- Without constitution: write full tech stack as before
- Lite mode: skip constitution reference entirely (keep it minimal)

## Spec Versioning

Every handoff file includes:

```yaml
spec-version: 1.0          # Current version of this handoff
based-on: (path or empty)  # Previous handoff version (for iterations)
```

- First handoff: `spec-version: 1.0`, `based-on:` (empty)
- Iteration: `spec-version: 1.1`, `based-on: docs/handoff/feature-v1.md` (or just increment)
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

Standard and Strict handoffs SHOULD include a Git Branch field in the YAML frontmatter to tell the coding agent which branch to work on:

```yaml
---
spec-version: 1.0
based-on:
constitution-ref: .hep/constitution.md
git-branch: feature/<feature-slug>
---
```

If not specified, the coding agent creates its own branch following project conventions.

Lite handoffs: Git branch field is optional.

## Handoff Quality Checklist

Before finalizing the handoff, verify:

1. **Self-contained**: A fresh coding agent with NO prior context can understand and implement everything
2. **No dangling references**: Every referenced file/path exists or will be created
3. **Testable AC**: Every acceptance criterion is machine-checkable
4. **No ambiguity**: Tasks are concrete, not "handle edge cases" — specify which cases
5. **Stack explicit**: No guessing required for technology choices
6. **Phases ordered**: Dependencies between phases are clear; earlier phases don't depend on later ones
7. **Verification defined**: Each task and phase has a clear "done" check
8. **Delta annotations**: Every Build Task has `[ADDED]`/`[MODIFIED]`/`[REMOVED]` prefix
9. **Constitution reference**: Present if `.hep/constitution.md` exists; Technical Architecture only has deviations
10. **Spec versioning**: `spec-version` header present; `based-on` set for iterations

## Anti-Patterns to Avoid

- **Vague tasks**: "Implement the feature" → too broad; break into specific file-level tasks
- **Missing context**: Assuming the coding agent knows project conventions → state them explicitly
- **PRD copy-paste**: Don't just copy the PRD; transform requirements into buildable tasks
- **Design copy-paste**: Don't just copy the design; extract what the coder needs (skip rationale)
- **Missing verification**: Every task needs a test command or observable check
- **Missing Delta annotations**: Without `[ADDED]`/`[MODIFIED]`/`[REMOVED]`, coding agent doesn't know intent
- **Repeating Constitution**: Don't copy the full tech stack into Technical Architecture when Constitution exists

## File Location

`docs/handoff/<feature-slug>.md`

Slug: lowercase, hyphens, matches PRD/design slug.

## Handoff to Coding Agent

The handoff file is the input to Phase 6 (Implementation Planning). The coding agent:

1. Reads the handoff file
2. Checks Constitution reference (if present)
3. Breaks tasks into implementation steps based on Delta annotations
4. Follows the phase ordering
5. Verifies each task against the acceptance criteria
6. If design issue found → writes DCR to `docs/feedback/<feature>-dcr.md`

Any deviation from the handoff spec requires going back to the research agent via DCR.
