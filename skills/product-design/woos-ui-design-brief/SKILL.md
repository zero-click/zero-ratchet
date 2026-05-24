---
name: woos-ui-design-brief
description: Transform product requirements into a focused UI/UX design brief with screens, flows, visual direction, and optional image-generation concepts. Bridge between product thinking and implementation.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [ui, ux, design, visual, screens, interface, product-design]
    related_skills:
      - woos-idea-capture
      - woos-product-design-flow
      - woos-build-handoff
---

# UI Design Brief

## Purpose

Convert product requirements (from PRD or idea capture) into a practical UI/UX design brief that defines what the interface should look, feel, and behave like — without prescribing implementation details.

This skill bridges product intent and engineering execution for interface-heavy products.

## When to Use

Use when:

- Feature has user-facing interface (web, mobile, desktop)
- Product experience requires visual/interaction clarity before coding
- Multiple screens or complex user flows need definition
- Team needs alignment on look & feel before implementation
- User asks for UI direction, mockup guidance, or visual exploration

Skip when:

- Pure API/backend work with no UI
- CLI-only tool with trivial interface
- UI is already well-defined in existing design system
- Lite mode and user hasn't asked for UI guidance

## Inputs

Before writing the brief, gather or infer from existing artifacts (PRD, idea capture):

- Product purpose and target user
- Core user flows (from PRD or idea capture)
- Main screens or surfaces
- Platform target: web, desktop, mobile, or multi-surface
- Desired feel: calm, command-center, playful, professional, dense, minimal, etc.
- Important states: empty, loading, error, success, first-run, repeat-use

If critical inputs are missing and user has not forced progression, ask one concise question at a time. Do NOT re-interview — use existing artifacts first.

## Output

File: `docs/design/<version>/<feature>-ui-brief.md`

## Brief Structure

```markdown
# <Feature Name> — UI Design Brief

## Purpose
What this interface achieves for the user.

## Product Feel
Calm / command-center / playful / professional / minimal / dense / etc.

## Design Principles
3-5 principles that guide UI decisions for this feature.
e.g., "Information density over whitespace", "Progressive disclosure", "Single primary action per screen"

## User Personas (from PRD)
Brief reminder of who uses this.

## Primary Screens / Surfaces
Numbered list of main screens with one-line purpose.

## Screen-by-Screen Notes

### Screen 1: <Name>
- Purpose: what user accomplishes here
- Layout: how information is organized
- Key elements: what must be visible
- Actions: what user can do
- States: empty / loaded / error / first-run

### Screen 2: <Name>
...

## Key User Flows
Numbered flows showing screen transitions.
e.g., "1. Landing → Sign up → Onboarding → Dashboard"

## Component Inventory
Reusable UI components needed across screens.
| Component | Used In | Notes |
|-----------|---------|-------|
| ... | ... | ... |

## States to Design
| State | Screens Affected | Behavior |
|-------|-----------------|----------|
| Empty | [list] | What shows when no data |
| Loading | [list] | Skeleton / spinner / progressive |
| Error | [list] | How errors display |
| Success | [list] | Confirmation behavior |
| First-run | [list] | Onboarding / guidance |

## Visual Direction
- Color mood: (warm/cool/neutral, high-contrast/soft)
- Typography: (compact/spacious, serif/sans)
- Density: (information-dense / breathing room)
- Dark/light mode: (required / optional / light-only)
- Existing design system: (reference if applicable)

## Accessibility & Responsiveness
- WCAG target: AA / AAA
- Breakpoints: mobile / tablet / desktop
- Keyboard navigation: required flows
- Screen reader considerations

## Content / Copy Notes
Tone and key copy decisions (formal/casual, verbose/terse).

## Open Questions
UI/UX decisions that need user input or testing.

## Handoff Notes for Implementation
Key constraints the coding agent must respect.
```

## Optional: Image-Generation Concepts

When visual direction is ambiguous, offer concept exploration:

**Three default concepts:**
1. **Conservative** — familiar, low-risk, easy to implement
2. **Strong-fit** — best interpretation of the product brief
3. **Divergent** — more distinctive, useful for taste discovery

**Image prompt template:**
```text
High-fidelity UI concept screenshot for <product>.
Platform: <desktop web/mobile/etc>.
Screen: <main dashboard/settings/etc>.
Target user: <user>.
Product feel: <feel>.
Layout: <key layout description>.
Must show: <components/data/actions>.
Avoid: generic SaaS filler, fake metrics, stock photos, unreadable text.
Style: <visual direction>.
```

**Rules for image concepts:**
- Images are inspiration, NOT the source of truth
- Always translate selected concepts back into written requirements
- Never ask coding agent to "copy this image" — extract principles and components

## After Concepts Are Chosen

If user selects a visual direction:
1. Update `Selected Direction` section with chosen layout, components, visual rules
2. Translate image choices into concrete component specs
3. Update handoff notes with constraints

## Relation to Product Design Flow

In `woos-product-design-flow`:
- Runs after PRD is approved (user knows WHAT to build)
- Runs before Build Handoff packaging (handoff includes UI direction)
- **Lite mode:** skipped entirely
- **Standard mode:** skipped (Standard is single-feature, keeps scope tight)
- **Strict mode:** triggered when feature has user-facing UI (orchestrator asks user)

## Pitfalls

- Don't prescribe implementation technology (React, Tailwind, etc.) — that's engineering
- Don't produce generic dashboard screenshots with fake data
- Don't skip states (empty, error, first-run) — they matter for quality
- Don't replace product decisions — if "what to build" is unclear, go back to PRD
- Don't over-specify — give direction, not pixel-perfect mockups
- Don't block the workflow if UI brief is skipped — carry UI as assumptions
