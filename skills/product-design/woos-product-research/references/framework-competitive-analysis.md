# Competitive Analysis Framework

## Purpose

Map the competitive landscape to identify positioning opportunities, learn from existing solutions, and understand the market context for product differentiation.

## Input

- Idea capture document (problem, target users, proposed solution)
- Market research findings (if available)
- Known competitors or references from user

## Methodology

### 1. Competitor Identification

Identify players across three rings:

- **Direct competitors**: Solve the same problem for the same users
- **Adjacent products**: Solve a related problem or serve adjacent users
- **Alternative approaches**: Different solution to the same underlying need (including "do nothing" / manual workarounds)

### 2. Structured Analysis Per Competitor

For each significant player:

| Dimension | What to Capture |
|-----------|----------------|
| **Positioning** | Who they serve, how they describe themselves |
| **Core strengths** | What they do well (from user reviews, not marketing) |
| **Weaknesses** | Common complaints, gaps, limitations |
| **Pricing model** | Free / freemium / paid / enterprise |
| **Technology approach** | Open source? Cloud? Self-hosted? API-first? |
| **Market segment** | Enterprise / SMB / developer / consumer |
| **Maturity** | Startup / growth / established / declining |

### 3. SWOT Synthesis (for our product)

Based on competitive landscape:

- **Strengths**: What advantages do we have? (tech, positioning, constraints-as-features)
- **Weaknesses**: Where are we behind? (resources, brand, ecosystem)
- **Opportunities**: What gaps exist in the market? What's underserved?
- **Threats**: What could competitors do that would block us?

### 4. Differentiation Strategy

Answer:
- What is our unique angle that no competitor owns?
- "Unlike [closest competitor], we [key differentiator] because [reason it matters to users]"
- What would we explicitly NOT do that competitors do? (anti-positioning)

## Output Structure

```markdown
# Competitive Analysis

## Landscape Overview
[2-3 sentence summary of the market state]

## Competitor Profiles

### [Competitor 1]
- **What they do**: ...
- **Strengths**: ...
- **Weaknesses**: ...
- **Relevant to us because**: ...

### [Competitor 2]
...

## Comparison Matrix
| Dimension | Us | Competitor A | Competitor B | Competitor C |
|-----------|-----|-------------|-------------|-------------|
| Target user | ... | ... | ... | ... |
| Core value prop | ... | ... | ... | ... |
| Pricing | ... | ... | ... | ... |
| Key limitation | ... | ... | ... | ... |

## SWOT
| Strengths | Weaknesses |
|-----------|-----------|
| ... | ... |

| Opportunities | Threats |
|--------------|---------|
| ... | ... |

## Differentiation
**Our unique angle**: ...
**Anti-positioning** (what we won't do): ...

## Sources
[All URLs cited]
```

## Quality Criteria

- At least 3 competitors analyzed (or justification why fewer exist)
- Analysis based on verifiable facts (user reviews, docs, pricing pages) not assumptions
- SWOT is honest — weaknesses and threats acknowledged, not minimized
- Differentiation statement is specific and testable, not generic ("better UX")
- Each source cited with URL
