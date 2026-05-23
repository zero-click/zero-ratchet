---
spec-version: 1.0
based-on: (empty for first version; path to previous handoff for iterations)
constitution-ref: .hep/constitution.md  (include if file exists; remove if not)
git-branch: feature/<feature-slug>  (recommended; remove if coding agent should choose)
---

# <Feature Name> — Build Handoff

## Mission
One sentence: what to build.

## Product Vision
Why we're building this, who it's for, what experience to deliver.

## Non-Negotiable Requirements
- [requirement 1 — must satisfy, testable]
- [requirement 2 — must satisfy, testable]

## Out of Scope
- [explicitly excluded 1]
- [explicitly excluded 2]

## Technical Architecture
- System architecture overview
- Main components and their interactions
- **Only deviations from Constitution** (if constitution-ref is set above, don't repeat stack; write only what differs)
- Data flow diagram (text description)

## Data Model
- Entities, fields, relationships
- Storage technology and schema
- Migration notes (if any)

## API Contracts
- Endpoints: method, path, request/response shapes
- Authentication/authorization requirements
- Error response format

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

> **Delta annotations**: prefix every task with [ADDED], [MODIFIED], or [REMOVED].
> First delivery = all [ADDED]. Iterations = mark actual change type.

### Task 1: [ADDED] <New functionality>
- Objective: [what to accomplish]
- Files to create:
  - `path/to/new-file.ext` — [purpose]
- Steps:
  1. [step]
  2. [step]
- Verification: [test command or check]
- Expected result: [observable outcome]

### Task 2: [MODIFIED] <Existing component>
- What changes: [description of modification]
- Files to modify:
  - `path/to/existing-file.ext` — [what changes]
- Steps:
  1. [step]
- Verification: [test command or check]
- Expected result: [observable outcome]

### Task 3: [REMOVED] <Deprecated component>
- What to remove: [description]
- Migration notes: [if applicable, how to migrate]
- Files affected:
  - `path/to/removed-file.ext`
- Verification: [test command or check]

## Acceptance Criteria
- Given [context], When [action], Then [expected result]
- Given [context], When [action], Then [expected result]

## Security Considerations
- Auth requirements
- Data sensitivity
- Input validation needs

## Verification Commands
```bash
# Run all tests
<test command>

# Run linting
<lint command>

# Build check
<build command>
```

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

---

<!-- OPTIONAL SECTIONS (Strict mode or when applicable) -->

## Auth / Secrets / Sharing Model
## Platform Targets
## Hosting / Data Location / Deployment Details
## Integrations (third-party services)
## UI Design Brief (reference to external mockups)
## Capability Contract (reference to capability doc)
## Rollout Plan
## Rollback Plan

---

<!-- LITE TEMPLATE (4 fields only — use this instead for Lite mode) -->

<!--
---
spec-version: 1.0
git-branch: feature/<feature-slug>  (optional)
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

## Verification Commands
```bash
<test command>
```
-->
