---
name: woos-problem-validation
description: Validate whether the captured problem is real, painful, frequent, and worth pursuing before broader discovery work begins.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, discovery, validation, research]
    related_skills:
      - woos-product-discovery
---

# Problem Validation

## Output Language

- Author all user-facing prose (narratives, findings, summaries) in the **user's most recent input language** (e.g. if the user is writing in Chinese, write the PRD body, review findings, and summaries in Chinese).
- Keep these tokens **verbatim in English** regardless of the user's language, because they are contract identifiers consumed by other skills and gates:
  - Verdict tokens: `PASS`, `REQUEST_CHANGES`, `BLOCKED`, `NOT_RUN`
  - Severity tokens: `critical`, `high`, `medium`, `low`, `warning`
  - Tag tokens: `[ASSUMPTION: ...]`, `[NEEDS CLARIFICATION: ...]`, `[NEEDS INPUT: ...]`
  - Phase / dimension IDs: `P0` … `P11`, `P2a`, `Phase A`, `Phase B`
  - Shape values: `internal-tool`, `single-operator`, `consumer-product`, `multi-stakeholder`, `CLI`
  - P0 rating values: `strong`, `adequate`, `thin`, `broken`
  - Section headings declared in templates (e.g. `## Background`, `## Functional Requirements`, `## Assumptions Index`) — translations break downstream structural checks
  - Field labels inside templates (e.g. `**Consequences (testable):**`, `**Out of Scope:**`, `**User value:**`, `Given … When … Then …`)
- Code, file paths, IDs, and quoted PRD excerpts stay in their original form.


## Purpose

Decide whether the captured problem should proceed, pivot, or park.

## Required Load Set (mandatory)

- `references/framework-customer-pain-points.md`
- `ideas/<slug>/00-idea-capture.md`

If any required file is not loaded, return `BLOCKED`.

## Output

- `ideas/<slug>/00-idea-capture.md` → append `## Problem Validation`

## Required Decision

The output must conclude with one of:

- `PROCEED`
- `PIVOT`
- `PARK`

## Must Answer

1. Is this a real problem?
2. How frequently does it occur?
3. How painful is it?
4. How many people have it?
5. Are people already paying time or money to solve it?
