---
name: woos-agent-decision
description: Resolve multi-agent review conflicts with explicit authority matrix, evidence weighting, and escalation criteria.
version: 1.1.0
author: Hermes Profile
license: MIT
---

# Woos Agent Decision

## Purpose

Provide deterministic conflict resolution when reviewers disagree on gate outcomes.

## Decision Policy

1. Domain authority first:
   - Security issues: `woos-security-reviewer` authoritative.
   - Architecture issues: `woos-architect` authoritative.
   - Planning/sequencing issues: `woos-product-planner` (with `mode: planning`) authoritative.
2. Evidence-backed conclusion over opinion-only conclusion.
3. Lower-risk path over speed-optimized path when evidence is similar.

## Escalation Triggers

- Same blocking disagreement unresolved after `reconciliation_attempt_max`.
- Conflict spans multiple domains with no clear authority winner.
- High-risk decision without sufficient evidence.

## Counter Contract

- `review_round_max`: 2
- `reconciliation_attempt_max`: 1 (within each round)
- Counter precedence:
  1. if `reconciliation_attempt_max` exceeded -> escalate immediately
  2. else if `review_round_max` exceeded -> escalate

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `resolution`: `agent_a` | `agent_b` | `hybrid` | `escalated_to_human`
- `reason`
- `evidence_used`
- `requires_human_handoff`: boolean
