---
name: woos-prd-authoring
description: Write high-quality, implementation-ready PRDs in Hermes using an ECC-aligned workflow. Covers PRD drafting, acceptance criteria quality, and mandatory independent PRD review gates before design/coding.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [prd, product, requirements, specification, planning, ecc]
---

# Woos PRD Authoring

## Why this skill exists

ECC provides strong downstream lanes like `product-capability` (PRD -> implementation contract), but it does not provide a dedicated first-class skill focused on writing PRDs from scratch.  
This skill fills that gap.

## When to use

Use for:

- New feature proposals
- Behavior-changing initiatives
- Cross-team or cross-service work that needs requirement clarity
- Any task where coding should not begin before requirements are explicit

Skip for:

- Tiny typo/docs edits
- Pure refactors with no behavior change

## Output artifact

Default file:

`docs/prd/<feature>.md`

If the repo uses a different convention, follow that convention.

## PRD structure (required)

```markdown
# <Feature Name> PRD

## 1. Background
## 2. Problem Statement
## 3. Goals
## 4. Non-Goals
## 5. Users / Personas
## 6. User Stories
## 7. Scope (In/Out)
## 8. Functional Requirements
## 9. Acceptance Criteria
## 10. Edge Cases / Failure Modes
## 11. Security / Privacy / Permission Notes
## 12. Rollout & Migration Notes
## 13. Metrics / Success Signals
## 14. Open Questions
```

## Acceptance criteria standard

Each critical story must have testable AC using Given/When/Then or equivalent deterministic format.

Bad:

- "Fast enough"
- "User-friendly"
- "Should work reliably"

Good:

- "Given a signed-in user with role=admin, when they archive a project, then the project status becomes `archived` within one request and appears archived after page refresh."

## Authoring workflow

1. **Intake**
   - Capture user intent, target users, constraints, and expected outcome.
2. **Define problem and goals**
   - Make problem explicit and measurable.
3. **Set boundaries**
   - Write non-goals and out-of-scope items early.
4. **Draft stories and requirements**
   - Convert intent into concrete user stories and functional requirements.
5. **Write acceptance criteria**
   - Ensure each critical behavior has explicit testable criteria.
6. **Risk and edge coverage**
   - Add failure modes, permissions, and security/privacy notes.
7. **Open questions**
   - List unresolved product decisions explicitly; do not invent missing truth.

## Mandatory PRD review gate

Before moving to design/coding, run independent PRD review using:

- `product-planner` (structure/completeness/testability)
- `architect` (feasibility/boundaries/non-functional risk)

Gate status must be one of:

- `PASS`
- `PASS_WITH_NOTES`
- `REQUEST_CHANGES`

`REQUEST_CHANGES` blocks progression until revised and re-reviewed.

## Handoff sequence

After PRD gate passes:

1. Run `product-capability` to convert PRD intent into implementation contract (constraints/invariants/interfaces).
2. Produce feature technical design.
3. Continue with TDD/implementation workflow.

## Practical invocation snippets

Use prompts like:

- "Use `woos-prd-authoring` to draft PRD for <feature> and stop at review gate."
- "Run PRD independent review using product-planner + architect, return PASS/REQUEST_CHANGES only."
- "Revise this PRD based on review findings and regenerate acceptance criteria."

## Quality checklist

Before marking PRD done:

- [ ] Problem is explicit and user-centered
- [ ] Goals are measurable
- [ ] Non-goals are explicit
- [ ] Scope boundaries are clear
- [ ] Critical stories have testable AC
- [ ] Security/permission concerns are captured
- [ ] Open questions are listed (not guessed away)
- [ ] `product-planner` + `architect` review gate passed
