---
name: woos-feature-design
description: Create implementation-ready feature technical design after PRD and capability contract are available.
version: 1.2.0
author: Hermes Profile
license: MIT
---

# Woos Feature Design

## Purpose

Produce a technical design artifact that is precise enough for TDD and implementation.

## Required Invocation (hard gate)

- MUST invoke `architect` to produce/revise the design.
- For high-complexity scope, also invoke `product-planner` to validate decomposition and sequencing.
- If required invocation is missing, return `NOT_RUN` and stop.
- If required component is unavailable, return `BLOCKED` and stop.
- Do not substitute with undocumented ad-hoc design notes.

## Reviewer Isolation (hard gate)

- The `architect` (and `product-planner` when invoked) MUST be dispatched as a separate agent instance with fresh context (e.g., via task/spawn tool). In-context skill injection where the same LLM session plays the reviewer role is NOT a valid invocation.
- The dispatched agent receives only the design inputs (approved PRD, capability contract, prior context). It MUST NOT inherit the implementer's session history or reasoning.
- `invocation_evidence` MUST include `dispatch_mode: "fresh_context"`. Any other value is invalid and MUST return `BLOCKED`.

## Contract

- Input: approved PRD + capability contract
- Output file: `docs/design/<feature>.md` (or project convention)
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output fields (required):
  - `design_owner: architect`
  - `review_dependencies` (e.g., product-planner for complex scope)
  - `baseline_compliance_status: PASS | REQUEST_CHANGES`
  - `deviation_detected: true|false`
  - `deviation_adr_path` (required when deviation_detected=true)
  - `approval_ref` (required when deviation_detected=true)
  - `unconfirmed_constraints_frozen: true|false`
- Required sections:
  - Overview
  - Architecture
  - Interface/API contracts
  - Data model implications
  - Security considerations
  - Test strategy
  - Rollout/rollback
  - Risks
  - Baseline/Deviation Decision Record (cross-domain: UI, backend, database, infra where applicable)

## Baseline and Deviation Rules (hard gate)

1. Default to mainstream, maintainable, evolvable baseline for each affected domain.
2. Any below-baseline or outlier decision requires ADR at `docs/adr/ADR-*.md`.
3. Deviation without explicit `approval_ref` MUST return `REQUEST_CHANGES`.
4. Do not freeze architectural constraints that were not user-provided or ADR-approved.
5. If `unconfirmed_constraints_frozen=true`, return `REQUEST_CHANGES`.
