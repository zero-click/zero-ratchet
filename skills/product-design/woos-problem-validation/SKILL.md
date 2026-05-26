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
