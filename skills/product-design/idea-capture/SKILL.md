---
name: idea-capture
description: Capture and structure raw ideas through guided interview or quick note. Produces a structured idea document ready for PRD or research pass. Includes Constitution detection and creation.
version: 2.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [idea, capture, interview, product, ideation, constitution]
    related_skills:
      - product-discovery
      - woos-prd-authoring
---

# Idea Capture

## Purpose

Transform a raw idea or feature request into a structured document that can feed into research, PRD, or directly into implementation (Lite mode).

Also responsible for **Constitution detection**: checking if the project has a `.hep/constitution.md` file and offering to create one if it doesn't exist.

## When to Use

Use when:

- User presents a new idea, feature request, or product vision
- Starting the product-discovery flow at Step 1
- Need to clarify scope before committing to a full PRD

Skip when:

- Idea already has a PRD → go to `woos-prd-authoring` or later phases
- Pure bugfix with clear reproduction → no capture needed

## Constitution Detection & Creation

**Before starting capture, check for Constitution:**

1. Check if `.hep/constitution.md` exists in the project root
2. If **exists**: note its presence for handoff reference; proceed with capture
3. If **NOT exists**:
   - Ask user: "This project doesn't have a constitution file (`.hep/constitution.md`). Would you like to create one? It captures project-level conventions (tech stack, architecture, coding standards) so handoffs stay focused on what's new."
   - If yes: extract from project context (scan `package.json`, `pyproject.toml`, `AGENTS.md`, existing code structure)
   - If no: proceed without constitution; handoffs will include full tech details

**Constitution creation sources (auto-detect from project):**

| Source | Extract |
|--------|---------|
| `package.json` / `pyproject.toml` | Language, framework, dependencies |
| `AGENTS.md` / `CLAUDE.md` / `.cursorrules` | Coding conventions, project rules |
| Existing directory structure | Architecture patterns |
| `tsconfig.json` / `wrangler.toml` / etc. | Runtime, deployment platform |
| `vitest.config` / `pytest.ini` / etc. | Testing framework |

**Constitution template:**

```markdown
# Project Constitution

## Tech Stack
- Language: [detected]
- Runtime: [detected]
- Framework: [detected]
- Database: [detected or "N/A"]
- Deployment: [detected]

## Architecture
- API style: [detected or ask]
- Auth: [detected or ask]
- State: [detected or ask]

## Coding Standards
- Linter: [detected]
- Testing: [detected]
- Commit: Conventional Commits (default) or [detected]

## Baseline Decisions
- Default ecosystem: [detected — deviations need ADR]
- [other conventions from AGENTS.md etc.]
```

**When to skip Constitution creation:**
- Lite mode and user said no → skip
- No project directory (pure ideation phase) → defer to later

## Capture Modes

### Lite Mode — Quick Note

For: small-scope ideas, feature requests with clear intent, internal improvements.

**Process:**

1. Record a concise idea summary
2. Identify target user, core problem, and proposed solution
3. Note constraints if any
4. Output to `ideas/<slug>.md`

**Lite template:**

```markdown
# <Idea Title>

## Summary
One paragraph: what and why.

## Problem
Who has this problem? What pain does it cause?

## Proposed Solution
What should we build?

## Constraints (if any)
- Time, budget, technical, or compatibility constraints

## Success Signal
How do we know it worked?
```

### Full Mode — Guided Interview

For: new product features, cross-cutting changes, ideas with unclear scope.

**Process:**

1. Check Constitution (see above)
2. Run through interview questions one at a time
3. Capture answers in structured format
4. Recommend technical defaults (recommend-then-confirm)
5. User can say `GREENLIGHT NEXT STAGE` to skip remaining questions
6. Output to `ideas/<slug>/00-idea-capture.md`

## Interview Question Bank

Ask sequentially. Skip if user already provided the information unprompted.

### Category 1: Problem & Users

1. **Who will use this?** (Target persona / user type)
2. **What problem does it solve?** (Pain point, frequency, severity)
3. **How do they solve it today?** (Current workaround, if any)

### Category 2: Vision & Behavior

4. **What should the ideal experience look like?** (User's mental model)
5. **What are the core behaviors?** (Must-have interactions / flows)
6. **What would make this feel "done" to you?** (Definition of success)

### Category 3: Scope & Boundaries

7. **What's explicitly out of scope?** (Things you do NOT want built)
8. **Are there time or resource constraints?** (Deadline, budget, team size)
9. **Does this need to work on day one, or can it be iterative?** (MVP vs complete)

### Category 4: Technical Context

10. **Any platform or technology requirements?** (Must work on X, must use Y)
11. **Are there integration points?** (Third-party services, existing systems)
12. **Any security or compliance concerns?** (Data sensitivity, access control)

### Category 5: Quality & Risk

13. **What would make this fail?** (Risks, failure modes, deal-breakers)
14. **How important is performance?** (Latency, throughput, scale expectations)
15. **What's the rollback plan if something goes wrong?** (Risk mitigation)

## Technical Defaults (Recommend-Then-Confirm)

After capturing answers, suggest sensible defaults:

```text
"I'd recommend [X] for [domain] because [reason].
 Does that work, or do you have a preference?"
```

| Domain | Default | Reason |
|--------|---------|--------|
| Frontend | Project's existing stack | Consistency |
| Backend | Project's existing stack | Consistency |
| Database | Project's existing DB | No migration overhead |
| Auth | Project's existing auth | No new security surface |
| Deployment | Project's existing pipeline | No infra changes |

Record overrides in the capture document. If Constitution exists, defaults come from Constitution — only deviations need recording.

## Output Format (Full Mode)

```markdown
# <Idea Title>

## Capture Date
YYYY-MM-DD

## Source
How did this idea come up?

## Constitution Status
- `.hep/constitution.md`: exists / not found / created this session
- Deviations from constitution: [list or "none"]

## Problem Statement
Who: [target users]
Pain: [what hurts]
Current workaround: [how they cope today]

## Vision
Ideal experience: [describe]

## Core Behaviors
1. [behavior 1]
2. [behavior 2]

## Success Criteria
- [observable outcome 1]
- [observable outcome 2]

## Out of Scope
- [explicitly excluded]

## Constraints
- Time: [deadline or "none"]
- Resources: [team size or "flexible"]
- Technical: [hard requirements]
- Security: [concerns or "standard"]

## Technical Defaults
| Domain | Choice | User Override |
|--------|--------|---------------|
| Frontend | [default] | [override or "accepted"] |

## Risks
- [risk]: [mitigation or "accepted"]

## Open Questions
- [unresolved question]

## Interview Status
- Questions answered: N/15
- GREENLIGHT used: yes/no
```

## File Locations

- Lite: `ideas/<slug>.md`
- Full: `ideas/<slug>/00-idea-capture.md` + `ideas/<slug>/README.md`
- Constitution: `.hep/constitution.md` (project root)

Slug: lowercase, hyphens, max 50 chars, from idea title.

## Handoff to Next Phase

After capture:

1. Lite mode → proceed to PRD (Phase 3)
2. Full + research needed → Research Pass (Phase 2)
3. Full + scope clear → PRD (Phase 3)

## Pitfalls

- Don't re-ask questions the user already answered unprompted
- Don't prescribe architecture — capture requirements, not solutions
- Don't skip open questions — they feed the research pass
- Don't write the PRD here — that's `woos-prd-authoring`
- Don't force Constitution creation on Lite mode — keep it lightweight
- Don't create Constitution from guesses — use detected project facts, ask for confirmation
