---
name: woos-product-prd-review-gate
description: Independent product-side PRD review gate. Runs the full PRD checklist in fresh context and returns PASS or REQUEST_CHANGES.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, prd, review, gate, validator]
    related_skills:
      - woos-product-design-flow
---

# Product PRD Review Gate

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

Run Step 4 of `woos-product-design-flow` as an isolated review skill so the reviewer cannot coast on the parent orchestrator's momentum.

This skill exists to enforce:

- fresh-context review
- full checklist coverage
- explicit structural + content verdicts
- fail-closed behavior when evidence is missing

## Required Invocation (hard gate)

- MUST be invoked as a separate skill from `woos-product-design-flow`
- MUST use fresh context; same-session self-review is invalid
- MUST read all declared inputs before issuing a verdict
- MUST cover Phase A and Phase B in one run
- If any required section or checklist row is skipped, return `BLOCKED`

## Required Load Set (mandatory)

Before reviewing, load and report:

- `references/persona-prd-validator.md`
- `references/template-prd-validation-checklist.md`
- `docs/prd/<version>/<feature-id>.md`
- `docs/prd/<version>/<feature-id>-requirements.md`
- `docs/product/<project>-architecture.md`

If any required file is not loaded, return `BLOCKED`.

## Conditional Load Set (upstream dependencies)

When the orchestrator provides upstream interface summaries, also load:

- `docs/prd/<version>/<upstream-feature-id>-interface.md` for each declared upstream dependency

When upstream interface summaries are present, add **P8** to the content quality checklist:

| P8 | Upstream interface alignment | Verify all shared concepts (enums, models, events, endpoints, terms) match upstream interface definitions exactly. Flag any divergence. |

P8 failures count toward `REQUEST_CHANGES`.

## Output

- `docs/reviews/<version>/<feature-id>-prd-review-rN.md`

## Review Protocol

The reviewer MUST use `references/template-prd-validation-checklist.md` as a real judgment rubric, not as background reading only. In particular:

- Use **Decision-readiness** to judge whether the actual problem and decisions are clearly stated
- Use **Substance over theater** to reject writing that looks complete but does not describe the real problem
- Use **Done-ness clarity** to judge whether FRs and ACs actually define "done"
- Use **Shape fit** to reject over-formalized persona / flow / PRD weight when the feature is really an internal-tool or capability spec

### Reviewer Discipline (non-negotiable)

- **Severity ranks impact on the PRD's usefulness, not how easy the fix is.** A vague background or a missing testable consequence is `critical` even though it's a one-paragraph fix. Glossary drift may be `low` even though it appears in many places.
- **Be specific. Cite exact PRD locations, quote phrases, name what is missing.** Abstract criticism ("not clear enough", "could be tighter") is failure of nerve and MUST be rewritten as concrete finding + concrete fix.
- **No blanket-pass language.** "Looks good overall" is invalid output and forces the gate to `BLOCKED`.
- **REQUEST_CHANGES findings MUST cite specific PRD locations and quote the problematic phrase.** A finding without evidence is invalid; the row defaults to PASS for that dimension. This rule is symmetric to the no-blanket-pass rule — it prevents lazy or fabricated REQUEST_CHANGES that would cause unnecessary fix-then-rereview loops.

### Phase A — Structural Completeness

Read the `Shape:` declaration at the top of the PRD's `## Background` (e.g. `Shape: internal-tool / single-operator`). If absent, treat shape as `unspecified` and require the author to declare it before passing Phase A.

**Always required:**

1. `## Background` (with Shape declaration)
2. `## Functional Requirements`
3. `## Non-Functional Requirements`
4. `## Edge Cases`
5. `## Non-Goals`
6. `## Success Metrics`

**Conditionally required:**

- `## User Personas` and `## User Flows` — required when shape is `consumer-product`, `multi-stakeholder`, or any feature with user-facing UI / multiple distinct user types. Optional (and preferably omitted) when shape is `internal-tool`, `single-operator`, or `CLI`.
- `## Assumptions Index` — required whenever any `[ASSUMPTION: ...]` tag appears anywhere in the PRD.

If a required section is missing, the result is immediately `REQUEST_CHANGES`. If a conditionally required section is present for the wrong shape and contains only placeholder filler ("the user is the operator"), flag it under P5 as persona theater.

### Phase B — Content Quality Checklist

| # | Criterion | Fix Hint |
|---|-----------|----------|
| P0 | Problem framing clarity *(rated `strong / adequate / thin / broken`)* | Separate actual problem, current example, root cause/mismatch, workaround, and user impact. The PRD MUST NOT pass if P0 is `thin` or `broken`. See **P0 Calibration Anchors** below for tier definitions. |
| P1 | Value-traced | Add `User value:` lines linking each requirement to user outcome |
| P2 | AC + testable Consequences | Every FR/US MUST carry at least one atomic, observable **Consequences (testable)** bullet with a concrete threshold or outcome. Rewrite "graceful handling", "reasonable performance", "user-friendly" as concrete bounds. |
| P2a | FR atomicity (one relationship per FR) | Each FR MUST express one capability or one relationship. Flag FRs that combine routing + observability + fallback + scope-boundary in one statement. Quote the FR text and propose the split. |
| P3 | Non-goals effective | Make non-goals concrete enough to reject a real request |
| P4 | Edge cases covered | Add empty/error/timeout/concurrent-access scenarios |
| P5 | Real user behavior and shape fit | Replace developer-centric wording with user-observable behavior. Reject persona/flow theater when shape is internal-tool. Reject under-specified personas/flows when shape is consumer-product. |
| P6 | No internal contradictions | Resolve conflicting statements or move scope to non-goals |
| P7 | Architecture reference check | Compare routes/constants/state names against architecture and annotate divergence; flag deployment conventions accidentally promoted into product contract without architectural basis |
| P9 | Assumptions surfaced and indexed | Two checks: (a) **Roundtrip** — every inline `[ASSUMPTION]` tag is in the index; every index entry can be located inline. (b) **Positive evidence** — reviewer MUST proactively identify at least **two domain-specific inferences** in the PRD (specific paths, enum values, default behaviors, precedence rules, timeout values, threshold numbers not stated in the requirements doc or roadmap quote) and verify they are either tagged or genuinely traced to explicit input. **A non-trivial PRD with zero `[ASSUMPTION]` tags is a red flag** and MUST be marked `critical` unless the reviewer can affirmatively list the inferences and show their source quotes. |
| P10 | Strategic coherence | Does the PRD have a thesis? Do FRs serve a unified arc, or is it a backlog with section headers? Does at least one Success Metric validate the thesis rather than just measure activity? Is a counter-metric named for the primary metric? Flag PRDs that read as feature lists with no central bet. |
| P11 | Downstream usability *(only when this PRD feeds engineering / UX)* | Are domain nouns used consistently across FRs / NFRs / Success Metrics (no synonym drift)? Do FR / US IDs resolve? For terminology-heavy features, recommend (do not require) a Glossary subsection. |

#### P0 Calibration Anchors

To make the four-tier rating repeatable, judge by these anchors:

- **`strong`** — All five components (observable problem / root cause / workaround / impact / example-vs-problem distinction) present and named, AND the "observable problem" is the general problem, not the current example. Example labels are explicit ("Teams is the example that exposed it"; "config-path X is one valid path, not the contract").
- **`adequate`** — All five components present, and the general-vs-example distinction is recoverable from the prose even if not labeled. Reviewer can summarize the real problem in one sentence after reading.
- **`thin`** — At least one component missing, OR the "observable problem" reads as the example itself ("Teams egress is broken" when the issue is general egress visibility), OR a deployment convention is asserted as product requirement without justification. Gate cannot PASS.
- **`broken`** — Problem framing is essentially the symptom or a feature request, with no underlying observable problem stated. Gate cannot PASS.

When borderline between two tiers, drop one tier. A `thin/adequate` borderline → `thin`.

## Special Rule — P7 Does Not Auto-Fail

Architecture is a reference, not a hard constraint.

- `✅` = aligned
- `📐` = intentional or explainable divergence — **MUST cite an explicit product reason in the PRD** (not just operator habit or current deployment state). Operator habit alone is not a valid product reason and reverts the row to `❌`.
- `❌` = true contradiction with no rationale

Only unsupported contradictions count toward `REQUEST_CHANGES`.

## Output Contract (required)

The output MUST include:

1. Structural checklist results (Phase A) — explicitly note the declared shape and which conditional sections apply
2. Full P0-P11 review table (skip P8 unless upstream interface summaries are present; skip P11 if the PRD does not feed downstream engineering or UX). P0 row MUST state `strong | adequate | thin | broken` before its finding; other rows use concrete PASS/FAIL per fix-hint.
3. `## Architecture Divergences` section when needed
4. `## Upstream Interface Alignment` section when P8 applies
5. `## Assumptions Roundtrip` section — list (a) inline `[ASSUMPTION]` tags missing from the index, (b) index entries that cannot be located inline, and (c) **the ≥2 inferences the reviewer proactively identified for P9 positive-evidence**, each with its source quote from roadmap/requirements OR `UNVERIFIED — should be tagged`.
6. `## Summary` with explicit verdict

## Verdicts

- `PASS` — all required structural checks pass; P1-P7 + P9-P11 have no failures; P0 is `strong` or `adequate`; P8 has no failures when it applies
- `REQUEST_CHANGES` — one or more structural/content failures remain, OR P0 is `thin` or `broken`, OR P9 positive-evidence found ≥1 hidden inference
- `BLOCKED` — review incomplete, missing inputs, checklist rows skipped, blanket-pass language detected, or REQUEST_CHANGES findings without cited evidence

## Fail-Closed Rules

- No blanket pass language ("looks good overall", "generally aligned")
- No blanket fail language either (every REQUEST_CHANGES finding must cite location + quote)
- Every checklist row MUST have a status and a concrete finding
- If any row has no finding or no judgment, verdict is `BLOCKED`
- If the reviewer cannot confirm a point, mark it explicitly and fail the gate
- If the actual problem is not plainly described (P0 `thin` or `broken`), the gate MUST NOT pass even if the rest of the structure is complete
- If P9 positive-evidence cannot find ≥2 inferences in a non-trivial PRD AND the PRD has zero `[ASSUMPTION]` tags, escalate to BLOCKED — the absence of inferences is itself suspect
