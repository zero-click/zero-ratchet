# Customer Pain Points Analysis Framework

## Purpose

Validate that the identified problem is real, painful, and worth solving. Extract structured evidence of customer pain to ground product decisions in reality rather than assumptions.

## Input

- Idea capture document (problem hypothesis, target users)
- Any available user feedback, complaints, support tickets, or behavioral data

## Methodology

### 1. Pain Discovery

For each identified user segment, investigate:

**A. Challenges & Friction**
- What tasks are unnecessarily difficult today?
- Where do users get stuck, confused, or frustrated?
- What workarounds have they invented? (workarounds = strong pain signal)

**B. Unmet Needs**
- What do users want to accomplish but cannot?
- What's the gap between current state and desired state?
- How do they describe the ideal solution in their own words?

**C. Adoption Barriers**
- What prevents users from switching to a better solution?
- Cost? Complexity? Lock-in? Learning curve? Trust?

**D. Satisfaction Gaps**
- Where do existing solutions fall short?
- What are the most common complaints about current tools?
- What features are "good enough" vs. genuinely painful?

### 2. Evidence Classification

For each pain point found, classify the evidence:

| Signal | Strength |
|--------|----------|
| Users actively complaining / requesting | Strong |
| Workaround exists but is painful | Strong |
| Data shows drop-off / failure at this point | Strong |
| Users paying (time/money) for inferior alternatives | Strong |
| "It would be cool" with no observed behavior | Weak — probe deeper |
| Only the requester has this problem | Weak — validate breadth |

### 3. Prioritization Matrix

Rank pain points by:
- **Frequency**: How often does this pain occur? (daily / weekly / rarely)
- **Intensity**: How painful is it? (blocking / annoying / minor)
- **Breadth**: How many people experience it? (all users / segment / edge case)
- **Alternatives**: Are there acceptable workarounds? (none / painful / adequate)

### 4. Verdict

Based on evidence, declare one of:
- **PROCEED** — Problem is real, painful, frequent, and broad. Continue to research.
- **PIVOT** — Problem exists but framing is wrong. Reframe and return to ideation.
- **PARK** — Insufficient evidence of pain. Record and revisit later.

## Output Structure

Append to the idea capture document:

```markdown
## Problem Validation

### Pain Points Identified
1. [Pain point] — Evidence: [source/data] — Severity: [High/Medium/Low]
2. ...

### Prioritization
| Pain Point | Frequency | Intensity | Breadth | Alternatives | Priority |
|------------|-----------|-----------|---------|--------------|----------|
| ... | ... | ... | ... | ... | ... |

### Evidence Summary
- Strong signals: [list]
- Weak signals requiring more data: [list]
- Contradictory evidence: [list]

### Verdict: [PROCEED / PIVOT / PARK]
[Rationale in 2-3 sentences]
```

## Quality Criteria

- At least 3 distinct pain points identified with evidence
- Each pain point traced to observable behavior (not speculation)
- Prioritization matrix completed with honest assessments
- Verdict is justified by evidence, not by desire to proceed
- Weak signals acknowledged honestly rather than inflated
