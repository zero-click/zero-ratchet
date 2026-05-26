# Epics & Stories Breakdown Framework

## Purpose

Decompose a PRD into implementable epics and user stories. Each epic delivers complete user value; stories within an epic are individually shippable units of work.

## Input

- PRD (functional requirements with stable IDs, user journeys, personas)
- System architecture (component boundaries — informs story scoping)

## Methodology

### 1. Epic Design Principles

**Group by user value, NOT by technical layer:**
- ❌ WRONG: "Database Setup", "API Development", "Frontend Components"
- ✅ RIGHT: "User Authentication", "Content Creation", "Search & Discovery"

**Each epic must be standalone:**
- Epic N delivers complete functionality for its domain
- Epic N should not REQUIRE Epic N+1 to work (though it may be enhanced by it)
- A user can get value from Epic 1 alone

**File-churn rule:**
- If two epics repeatedly modify the same core files → consolidate into one epic
- This reduces feedback loops and merge conflicts during implementation

### 2. Epic Identification Process

**Step A: Identify themes from PRD**
- Group related FRs by the user outcome they enable
- Each group = candidate epic
- Name it by what the user can DO, not what the developer builds

**Step B: Validate independence**
- Can this epic be built and shipped without other epics existing?
- If not, either merge with dependency or mark explicit build order

**Step C: Check file overlap**
- For each epic pair, estimate which source files they'd both modify
- High overlap → consider merging
- Low overlap → good separation

**Step D: Order by value and dependency**
- Which epic delivers the most value soonest?
- Which epics enable other epics? (build these first)
- Result: ordered epic list (not a graph — a linear build sequence)

### 3. FR Coverage Tracking

Every Functional Requirement in the PRD MUST map to exactly one epic:

```
FR-1: Epic 1 — User Authentication
FR-2: Epic 1 — User Authentication
FR-3: Epic 2 — Content Creation
FR-4: Epic 3 — Search & Discovery
...
```

If any FR is unmapped → create an epic or assign to existing one. Zero gaps allowed.

### 4. Story Writing (within each epic)

For each story:
- **Title**: As a [persona], I want to [action] so that [value]
- **Acceptance criteria**: Testable conditions (Given/When/Then or checklist)
- **Scope boundary**: What's explicitly NOT in this story
- **Dependencies**: Other stories that must be done first (minimize these)

## Output Structure

```markdown
# Epics & Stories — [Project/Feature]

## Epic Overview
| # | Epic | FRs Covered | Depends On | Estimated Stories |
|---|------|-------------|-----------|-------------------|
| 1 | [Name] | FR-1, FR-2 | — | 4 |
| 2 | [Name] | FR-3, FR-4, FR-5 | Epic 1 | 6 |
| 3 | [Name] | FR-6, FR-7 | — | 3 |

## FR Coverage Map
| FR | Epic | Status |
|----|------|--------|
| FR-1 | Epic 1 | ✅ Covered |
| FR-2 | Epic 1 | ✅ Covered |
| ... | ... | ... |

## Epic 1: [Name]
**Goal**: [What user can accomplish when this epic is done]
**FRs**: FR-1, FR-2

### Story 1.1: [Title]
As a [persona], I want to [action] so that [value].
**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Story 1.2: [Title]
...

## Epic 2: [Name]
...
```

## Quality Criteria

- 100% FR coverage — every FR maps to an epic (zero gaps)
- Epics named by user outcome, not technical layer
- Each epic is independently valuable (can ship alone)
- Stories have testable acceptance criteria (not vague "should work")
- Build order is logical (dependencies flow forward, not circular)
- No epic touches the same core files as another (file-churn rule checked)
