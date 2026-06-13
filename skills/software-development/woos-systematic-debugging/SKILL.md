---
name: woos-systematic-debugging
description: Use when implementation or verification hits repeated failures. Enforces root-cause investigation before fix attempts.
version: 1.0.0
author: Hermes Profile
license: MIT
---

# Woos Systematic Debugging

## Purpose

Prevent "fix-by-guessing" loops that waste context and introduce new bugs. When repeated failures occur during TDD, verification, or any gate retry, this skill enforces a structured root-cause-first approach.

## When to Activate

- TDD RED-GREEN cycle: test fails for 2+ consecutive fix attempts
- Verification gate (`verification-loop`): lint/test/build fails after implementation and fix is not obvious
- Any gate retry: `woos-failure-state-machine` reaches 2+ retries on the same failure
- Bug investigation: reproducing and fixing a reported defect

**Activation is mandatory, not optional.** If you are on your 2nd failed fix attempt, you MUST switch to this skill before trying again.

## The Iron Law

```
NO FIX WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Proposing a fix before completing Phase 1 is invalid. Delete the fix. Start Phase 1.

## Four-Phase Protocol

```
Phase 1: Evidence Collection (DO NOT CHANGE CODE)
  ↓
Phase 2: Pattern Analysis
  ↓
Phase 3: Single-Hypothesis Verification
  ↓
Phase 4: Fix with Regression Test
```

### Phase 1 — Evidence Collection

**Goal:** Understand what is happening. Do not guess. Do not change code.

Steps:

1. Reproduce the failure with a single command. Record exact output.
2. At each component boundary (function call, API call, DB query, file I/O), log what enters and what exits.
3. Compare actual behavior vs expected behavior at each boundary.
4. Identify the FIRST point where actual diverges from expected.

**Phase 1 output (required before proceeding):**

```text
FAILURE_REPRODUCTION:
  command: <exact command>
  output: <exact output>
  exit_code: <number>

BOUNDARY_TRACE:
  - boundary: <name>
    input: <what entered>
    output_expected: <what should exit>
    output_actual: <what actually exited>
    diverges: true|false

FIRST_DIVERGENCE_POINT: <boundary name>
```

**Hard gate:** If you cannot fill in `FIRST_DIVERGENCE_POINT`, you have not completed Phase 1. Keep investigating.

### Phase 2 — Pattern Analysis

**Goal:** Understand WHY it diverges at that point.

Steps:

1. Read the code at the divergence point. Trace the logic path.
2. Check: is this a data problem, a logic problem, a state problem, or an environment problem?
3. Check: has this pattern failed before? (consult `woos-workflow-memory` if available)
4. List candidate root causes (max 3). Each must reference specific code location.

**Phase 2 output (required before proceeding):**

```text
DIVERGENCE_ANALYSIS:
  type: data|logic|state|environment
  code_location: <file:line>
  
CANDIDATE_ROOT_CAUSES:
  1. <cause> at <file:line> — evidence: <why you think this>
  2. <cause> at <file:line> — evidence: <why you think this>
  
MOST_LIKELY: <number>
REASONING: <why this one over others>
```

### Phase 3 — Single-Hypothesis Verification

**Goal:** Confirm or eliminate the most likely root cause. Change ONE thing.

Steps:

1. State your hypothesis as a falsifiable prediction: "If X is the cause, then changing Y should produce Z."
2. Make exactly ONE minimal change to test the hypothesis.
3. Run the reproduction command from Phase 1.
4. Did the prediction hold?
   - YES → Proceed to Phase 4.
   - NO → Revert the change. Move to next candidate. If all candidates exhausted, return to Phase 1 with deeper tracing.

**Hard gate:** Do not change more than one variable at a time. Multi-variable changes make results uninterpretable.

### Phase 4 — Fix with Regression Test

**Goal:** Implement the real fix and prove it works.

Steps:

1. Write a failing test that reproduces the original bug (RED).
2. Run it — confirm it fails for the expected reason.
3. Implement the fix (minimal, targeted).
4. Run the failing test — confirm it passes (GREEN).
5. Run the full test suite — confirm no regressions.
6. Revert the fix temporarily — confirm the test fails again (proves the test is real).
7. Restore the fix — confirm everything passes.

**Phase 4 output (required):**

```text
REGRESSION_TEST:
  test_file: <path>
  test_name: <name>
  red_confirmed: true
  green_confirmed: true
  revert_confirmed_red: true
  full_suite_passes: true
```

## Escalation Ceiling

```
fix_attempt_max: 3
```

After 3 failed fix attempts (across all phases):

1. STOP. Do not attempt fix #4.
2. Question whether this is an architectural problem, not a local bug.
3. Document findings so far.
4. Escalate to `woos-human-handoff` with full Phase 1-3 evidence.

## Integration with Workflow

This skill is a **cross-cutting protocol**, not a fixed gate. It activates during:

- Gate 2.1 (TDD): when RED-GREEN cycle stalls
- Gate 2.2 (Implement): when implementation creates cascading failures  
- Gate 2.3 (Verify): when verification fails and fix is non-obvious
- `woos-failure-state-machine`: when `FAILED_RETRYABLE` retry count reaches 2+

When activated, the current gate pauses. Debugging protocol runs. When Phase 4 completes, the original gate resumes.

## Output Contract

```text
STATUS: RESOLVED | ESCALATED | BLOCKED
ROOT_CAUSE: <one-sentence description>
ROOT_CAUSE_LOCATION: <file:line>
FIX_DESCRIPTION: <what was changed and why>
REGRESSION_TEST: <test name and path>
FIX_ATTEMPTS_USED: <number>
PHASES_COMPLETED: [1, 2, 3, 4]
```

`RESOLVED` requires all four phases completed with evidence.
`ESCALATED` when fix_attempt_max exceeded — must include all collected evidence.
`BLOCKED` when reproduction itself is not achievable.
