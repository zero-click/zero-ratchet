---
name: idea-capture
description: Capture and structure raw ideas through guided interview or quick note. Produces a structured idea document ready for research or PRD pass. Focuses purely on product intent — no technical decisions.
version: 3.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [idea, capture, interview, product, ideation]
    related_skills:
      - product-discovery
      - woos-prd-authoring
---

# Idea Capture

## Purpose

Transform a raw idea or feature request into a structured document that can feed into research, PRD, or product planning.

This skill focuses exclusively on **product intent**: what problem to solve, for whom, and what success looks like. It does NOT make technical decisions — those belong in later stages.

## When to Use

Use when:

- User presents a new idea, feature request, or product vision
- Starting the product-discovery flow at Step 1
- Need to clarify scope before committing to a full PRD

Skip when:

- Idea already has a PRD → go to `woos-prd-authoring` or later phases
- Pure bugfix with clear reproduction → no capture needed

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

1. Run through interview questions one at a time
2. Capture answers in structured format
3. User can say `GREENLIGHT NEXT STAGE` to skip remaining questions
4. Output to `ideas/<slug>/00-idea-capture.md`

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

### Category 4: Context & Dependencies

10. **Are there integration points?** (Third-party services, existing systems)
11. **Any security or compliance concerns?** (Data sensitivity, access control)

### Category 5: Quality & Risk

12. **What would make this fail?** (Risks, failure modes, deal-breakers)
13. **How will you know this is successful?** (Observable outcomes, metrics)

## Technical Defaults (Recommend-Then-Confirm)

This section has been removed from idea-capture. Technical decisions belong in later stages (feature-design or engineering workflow). Idea capture focuses purely on product intent.

## Output Format (Full Mode)

```markdown
# <Idea Title>

## Capture Date
YYYY-MM-DD

## Source
How did this idea come up?

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
- Dependencies: [integration points or "none"]
- Security: [concerns or "standard"]

## Risks
- [risk]: [mitigation or "accepted"]

## Open Questions
- [unresolved question]

## Interview Status
- Questions answered: N/13
- GREENLIGHT used: yes/no
```

## File Locations

- Lite: `ideas/<slug>.md`
- Full: `ideas/<slug>/00-idea-capture.md` + `ideas/<slug>/README.md`

Slug: lowercase, hyphens, max 50 chars, from idea title.

## Handoff to Next Phase

After capture:

1. Lite mode + scope clear → proceed to PRD
2. Full + research needed → Research Pass
3. Full + scope clear → PRD

## Pitfalls

- Don't re-ask questions the user already answered unprompted
- Don't prescribe architecture — capture requirements, not solutions
- Don't skip open questions — they feed the research pass
- Don't write the PRD here — that's `woos-prd-authoring`
- Don't make technical decisions — those belong in later stages
- Don't discuss tech stack, frameworks, or databases — stay on product intent
