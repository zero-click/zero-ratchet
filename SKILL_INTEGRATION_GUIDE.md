# Skill Integration Guide

Updated workflow integration of `deep-research`, `api-design`, and `browser-qa` into the `woos-development-workflow`.

## Governance baseline (new)

This profile now applies one global technical governance rule across UI/backend/database/infra:

1. Default to mainstream, maintainable, evolvable engineering baseline.
2. Any deviation requires ADR + explicit approval reference.
3. Unconfirmed constraints must not be frozen into PRD/design.
4. Review gates must output machine-readable baseline/deviation fields.

ADR template path: `docs/adr/ADR-template.md`

## Profile-based activation (new)

To reduce unnecessary process overhead, `woos-development-workflow` now supports:

- **Lite** for small/low-risk changes
- **Standard** (default) for normal feature work
- **Strict** for high-risk/high-uncertainty delivery with full hard gates

## Collaboration hardening (new)

To reduce repeated `REQUEST_CHANGES` loops, the workflow now also uses:

- `woos-review-context` for cumulative cross-gate findings
- `woos-agent-decision` for deterministic reviewer conflict resolution

Review gates (`woos-prd-review-gate`, `woos-design-review-gate`, `woos-code-review-gate`) now require:

1. Loading prior review context before reviewer invocation
2. One-pass complete findings across required dimensions
3. Updating review context with resolved/carry-forward findings
4. Escalating to `woos-human-handoff` when review rounds exceed threshold

## New Conditional Skills

### 1. Deep Research (Research Phase)

**Location:** Gate 0.5 (Research)  
**Default:** `search-first`  
**Upgrade option:** `deep-research`

#### When to Use `deep-research`

- **Idea validation**: Requirement is vague; need market/user pain validation
- **Competitive analysis**: Need competitive landscape or technology evaluation
- **TAM sizing**: Building top-down market estimates
- **Vendor/tech due diligence**: Evaluating frameworks, tools, or architectural choices
- **Uncharted territory**: Building something without clear precedent

#### How It Works

1. `deep-research` searches multiple sources (web, documentation, academic papers)
2. Synthesizes findings with citations
3. Delivers decision-oriented research report
4. Validates your chosen direction against research evidence

#### Example Triggers

- "We think we should build X, but is there user demand?"
- "Should we use Framework A or B?"
- "What's the current state of Rust vs Go for our use case?"
- "Do we have competitive moat in this area?"

#### Cost

- Multi-source search + deep reads of key sources
- ~10-15 min per deep research run
- Best done before PRD authoring to validate direction

---

### 2. API Design Review (Feature Design Phase)

**Location:** Gate 2.1 (Optional, conditional on API scope)  
**Trigger:** "Does this feature include new/modified REST or GraphQL endpoints?"

#### When to Invoke

- Creating new REST endpoints
- Modifying existing API contracts
- Building public or partner-facing APIs
- Designing real-time or streaming APIs

#### Minimal Contract

1. ✅ Endpoints follow naming conventions
   - Plural nouns, kebab-case, no verbs
   - `GET /api/v1/users` (not `/api/v1/get-users`)
   - `POST /api/v1/users/:id/orders`

2. ✅ HTTP methods and status codes are semantically correct
   - 200 for success with body
   - 201 for created (+ Location header)
   - 204 for success without body
   - 4xx for client errors, 5xx for server errors

3. ✅ Pagination/filtering strategy defined
   - Cursor-based (for feeds, infinite scroll)
   - Offset-based (for dashboards, small datasets)

4. ✅ Authentication and authorization documented
   - Bearer token, API key, OAuth, etc.
   - Resource-level ownership checks
   - Role-based access control

5. ✅ Error response format is standard
   ```json
   {
     "error": {
       "code": "validation_error",
       "message": "Request validation failed",
       "details": [...]
     }
   }
   ```

6. ✅ Rate limiting policy defined (if applicable)
   - Per-user, per-IP limits
   - Tier-based (free/paid)

#### How to Use

During `woos-feature-design`:

```
Feature Design
  ↓
  If API endpoints in design:
    → Invoke `api-design` to validate contracts
    → Check design against checklist above
    → Update design artifact if issues found
  ↓
Design Review
```

#### Example Output

```markdown
# API Design Review — Create Order Endpoint

## Endpoints Designed
- `POST /api/v1/orders` — Create new order
- `GET /api/v1/orders/:id` — Retrieve order details
- `PATCH /api/v1/orders/:id` — Update order status

## Validation Results
- ✅ Resource naming: PASS (nouns, plural, kebab-case)
- ✅ Methods: PASS (POST for create, GET for read, PATCH for update)
- ✅ Status codes: PASS (201 for create, 200 for read, 200 for update)
- ✅ Pagination: PASS (cursor-based for list endpoints)
- ✅ Auth: PASS (Bearer token, resource ownership checked)
- ✅ Error format: PASS (standard envelope with code/message)

## Verdict: READY FOR IMPLEMENTATION
```

---

### 3. Browser QA (Verify Phase)

**Location:** Gate 5.3 (Optional, conditional on frontend scope)  
**Trigger:** "Does this feature include frontend/UI changes?"

#### When to Invoke

- Any frontend changes (new pages, components, interactions)
- UI redesigns or layout changes
- Cross-browser compatibility required
- Responsive design changes
- Accessibility improvements
- Pre-launch sanity check

#### Minimal Contract

1. ✅ **Smoke Test**
   - Page loads without 5xx errors
   - Console has no critical errors
   - All network requests succeed (or expected failures only)
   - Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms

2. ✅ **Interaction Test**
   - Key user flows execute successfully
   - Forms submit and show success state
   - Invalid input shows error state
   - Navigation links don't 404
   - Auth flows (login/logout) work

3. ✅ **Visual Regression**
   - Screenshots at 3 breakpoints: 375px, 768px, 1440px
   - No layout shifts > 5px
   - No missing elements or overflow
   - Dark mode (if applicable) consistent

4. ✅ **Accessibility**
   - WCAG AA violations checked (contrast, labels, focus)
   - Keyboard navigation works
   - Screen reader landmarks present
   - No `aria-*` misuse

5. ✅ **Evidence**
   - Screenshots provided
   - Issues logged with reproduction steps
   - Verdict: "ship as-is" vs "needs fixes" vs "blockers"

#### How to Use

After `verification-loop`:

```
Verify (build/lint/test)
  ↓
  If frontend changes detected:
    → Invoke `browser-qa`
    → Review smoke/interaction/visual/accessibility results
    → Block progression if critical issues found
  ↓
Executable Acceptance
```

#### Example Output

```markdown
# Browser QA Report — Dashboard Redesign

## Smoke Test ✅
- Page load: 1.2s LCP
- Core Web Vitals: PASS
- Network: 100% success (no 4xx/5xx)

## Interactions ✅
- Login form: works
- Chart filtering: works
- Modal open/close: works
- Dark mode toggle: works

## Visual Regression ⚠️
- Mobile (375px): PASS
- Tablet (768px): PASS
- Desktop (1440px): Layout shift detected in sidebar (-8px, should be ±5px)

## Accessibility ✅
- Axe audit: 0 AA violations
- Keyboard nav: works
- Focus order: correct

## Verdict: NEEDS FIXES (1 layout regression)
→ Fix sidebar alignment, re-run browser-qa
```

---

## Decision Table: Should I Invoke This Skill?

| Gate | Skill | Decision |
|------|-------|----------|
| Research | `deep-research`? | YES if: requirement is fuzzy, need market validation, competitive analysis needed |
| Feature Design | `api-design`? | YES if: scope includes REST/GraphQL endpoints |
| Verify | `browser-qa`? | YES if: scope includes frontend/UI changes |

---

## Integration with Existing Workflow

The three new skills are **optional conditional steps**, not mandatory gates.

```
woos-development-workflow logic:

IF research_phase AND idea_is_fuzzy:
  → Use deep-research instead of search-first
ELSE:
  → Use search-first (default, faster)

IF feature_design_phase AND api_in_scope:
  → Invoke api-design after design artifact created
ELSE:
  → Skip, proceed to design review

IF verify_phase AND frontend_in_scope:
  → Invoke browser-qa after verification-loop
ELSE:
  → Skip, proceed to executable acceptance
```

---

## FAQ

### Q: When do I use `deep-research` vs `search-first`?

**search-first** (faster, default):
- Requirement is already clear
- Just need to check for existing solutions/libraries
- Time budget: < 5 min

**deep-research** (thorough, optional):
- Requirement is vague or unvalidated
- Need to verify market demand or competitive landscape
- Need TAM/SAM estimates
- Time budget: 10-15 min

### Q: Does `api-design` replace code review?

No. `api-design` happens during design phase (before implementation).  
Code review happens after implementation (Gate 6).

- `api-design`: "Is the contract design correct?"
- `code-review`: "Is the implementation correct?"

### Q: Can I skip `browser-qa` if I have unit tests?

Not recommended. Unit tests validate logic; `browser-qa` validates real browser behavior.
- Unit tests: "Does the function work?"
- Browser QA: "Does it work in Chrome/Safari/Firefox? Can a user interact with it?"

### Q: What if `browser-qa` finds issues?

Return `REQUEST_CHANGES` and:
1. Fix the issue
2. Re-run `verification-loop` (build/lint/test)
3. Re-run `browser-qa`
4. Proceed when status = `PASS`

---

## File Changes

Modified:
- `skills/software-development/woos-development-workflow/SKILL.md` — Added gate definitions for deep-research, api-design, browser-qa
- `design.md` — Updated skill mapping and workflow topology
- `README.md` — Updated mermaid flowchart and skill list

Next steps:
- Install the updated profile
- Try a new feature with the full workflow
- Collect feedback on conditional skill triggers
