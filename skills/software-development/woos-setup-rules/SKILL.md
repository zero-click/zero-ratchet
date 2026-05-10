---
name: woos-setup-rules
description: Setup project rule routing for Hermes by generating `AGENTS.md` from imported rule packs in profile `rules/ecc-import`.
version: 1.0.0
author: Hermes Profile
license: MIT
---

# Woos Setup Rules

## Purpose

Configure project-level rule routing so Hermes can apply language-appropriate rules consistently.

## When to Use

- New repository onboarding
- Profile upgrade after rule-pack sync
- Mixed-language project setup
- Rule routing drift or ambiguity

## Preconditions

- Coding profile has imported rules under: `~/.hermes/profiles/coding/rules/ecc-import/`
- If missing, run installer with rules sync enabled.

## Workflow

1. Detect active languages in the current repository.
2. Select rule packs:
   - Always include `common`.
   - Include language packs only when corresponding file types exist.
3. Create or update project `AGENTS.md` with:
   - Rule routing policy
   - Language-to-rule mapping
   - Mixed-language precedence policy
4. Ensure the routing text is explicit and deterministic.

## Output Contract

Return:

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `routing_file`: path of updated `AGENTS.md`
- `rule_packs_used`: list of selected packs
- `notes`: any unresolved ambiguity

## Recommended `AGENTS.md` Routing Template

```markdown
## Scope

This file defines project-level coding rules routing for Hermes and compatible coding agents.

## Rule Routing

- Always apply: common baseline rules.
- If touched files include `*.ts,*.tsx,*.js,*.jsx`: apply TypeScript/JS rules.
- If touched files include `*.py`: apply Python rules.
- If touched files include `*.go`: apply Go rules.
- If touched files include `*.java`: apply Java rules.
- If touched files include `*.rs`: apply Rust rules.
- If mixed-language changes touch shared interfaces, use the stricter rule on boundary contracts.
```
