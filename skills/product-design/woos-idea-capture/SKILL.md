---
name: woos-idea-capture
description: Capture and structure raw ideas through guided interview or quick note. Produces a structured idea document ready for research or PRD pass. Focuses purely on product intent — no technical decisions.
version: 3.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [idea, capture, interview, product, ideation]
    related_skills:
      - woos-product-discovery
      - woos-product-design-flow
---

# Idea Capture

## Purpose

Transform a raw idea or feature request into a structured document that can feed into research, PRD, or product planning.

This skill focuses exclusively on **product intent**: what problem to solve, for whom, and what success looks like. It does NOT make technical decisions — those belong in later stages.

## When to Use

Use when:

- User presents a new idea, feature request, or product vision
- Starting the woos-product-discovery flow at Step 1
- Need to clarify scope before committing to a full PRD

Skip when:

- Idea already has a PRD → go to `woos-product-design-flow`
- Pure bugfix with clear reproduction → no capture needed

## Capture Process

> **Note:** Capture itself always runs the same way, but mode selection happens in two places:
> - **Lite** may branch immediately after Capture if the idea is obviously trivial and the user confirms.
> - **Standard / Strict** are inferred later, after Product Discovery, from the approved roadmap.

**Two capture depths based on idea complexity:**

### Quick Note (trivially simple ideas)

For: single-line fixes, obvious improvements, user already has full clarity.

**Process:**

1. Record a concise idea summary
2. Identify target user, core problem, and proposed solution
3. Note constraints if any
4. Output to `ideas/<slug>.md`

**Quick Note template:**

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

### Guided Interview (anything non-trivial)

For: features, product initiatives, anything requiring design thinking.

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

10. **Does this need to connect to anything that already exists?** (Existing products, data sources, user accounts — NOT tech stack)
11. **Any security or compliance concerns?** (Data sensitivity, access control, regulatory)

### Category 5: Quality & Risk

12. **What would make this fail?** (Risks, failure modes, deal-breakers)
13. **How will you know this is successful?** (Observable outcomes, metrics)

## Handling Technical Preferences

Users often volunteer technical opinions during capture ("I want to use Go", "let's use SQLite", "no React"). This is natural — but it must NOT become a hard constraint in this phase.

**Rules:**

1. **Do NOT ask** questions about tech stack, frameworks, languages, or databases
2. **If user volunteers a tech preference** → acknowledge it, then record it in the output under a dedicated `## Technical Preferences (Deferred)` section
3. **Label clearly** — these are preferences, not decisions. They will be evaluated by the architect sub-agent in Discovery Step 5
4. **Do NOT let preferences leak** into Problem Statement, Vision, Core Behaviors, or Constraints sections
5. **Do NOT push back** on preferences — just record and defer. No debate in this phase.

**Output format for deferred preferences:**

```markdown
## Technical Preferences (Deferred)

> ⚠️ These are user preferences expressed during idea capture. They are NOT confirmed
> technical decisions. They will be evaluated by the architect sub-agent in Discovery
> Step 5, where trade-offs can be properly assessed.

- "Backend in Go" — user preference, to be evaluated in architecture
- "SQLite for storage" — user preference, to be evaluated in architecture
```

## Output Format (Standard / Strict Mode)

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

## Technical Preferences (Deferred)

> ⚠️ User preferences only. NOT decisions. Evaluated in Discovery Step 5 (Architecture).

- [preference]: user preference, to be evaluated in architecture
- (or "None expressed")

## Risks
- [risk]: [mitigation or "accepted"]

## Open Questions
- [unresolved question]

## Interview Status
- Questions answered: N/13
- GREENLIGHT used: yes/no
```

## File Locations

- Quick Note (trivial): `ideas/<slug>.md`
- Guided Interview: `ideas/<slug>/00-idea-capture.md`

Slug: lowercase, hyphens, max 50 chars, from idea title.

## After Capture — Lite Branch Decision

After capture is complete, assess complexity:

```text
Is it obviously trivial? (typo, 1-liner, single obvious change, user explicitly says it's simple)
  → Yes → Propose Lite to user: "This looks straightforward. I suggest Lite mode — go directly to handoff. Agree?"
           → User confirms → `woos-product-design-flow` Lite
           → User says no  → proceed to Discovery
  → No  → proceed to `woos-product-discovery` (research needed)
```

**Rules:**
- Lite is a PROPOSAL, not a default. User must confirm.
- If there are open questions, risks, or dependencies → NOT trivial → Discovery.
- When in doubt, proceed to Discovery. Lite is only for the obviously simple.

## Pitfalls

- Don't re-ask questions the user already answered unprompted
- Don't prescribe architecture — capture requirements, not solutions
- Don't skip open questions — they feed the research pass
- Don't write the PRD here — that's handled in `woos-product-design-flow`
- Don't make technical decisions — those belong in later stages
- Don't discuss tech stack, frameworks, or databases — stay on product intent
- Don't auto-select Lite without user confirmation
- **Don't ASK about tech stack** — if user volunteers preferences, record under "Technical Preferences (Deferred)", never in Constraints
- **Don't let tech preferences become constraints** — "user wants Go" ≠ "must use Go". Record as preference, let architect evaluate in Discovery Step 5
- **Don't debate tech choices** — this phase has no authority to confirm or reject technical decisions
