---
name: woos-review-context
description: Maintain cumulative cross-gate review context so reviewers build on prior findings instead of restarting from zero.
version: 1.5.0
author: Hermes Profile
license: MIT
---

# Woos Review Context

## Purpose

Provide a shared, cumulative review memory across PRD/design/code/security gates.

## Required Behavior

1. Load prior review context before invoking any reviewer.
2. Pass unresolved prior findings into the current review prompt.
3. Require explicit resolution status for each prior blocking finding.
4. Persist new findings with ownership, severity, and target artifact.
5. Preserve finding identity across gates and rounds; do not emit duplicate findings with new IDs.

## Persistence Contract (mandatory)

- Review context MUST be stored on disk (not only in transient prompt state).
- Canonical runtime root: `<workspace_root>/hep`.
- Default path: `<workspace_root>/hep/review-context/<run_id>.yaml`.
- `review-context/` directory is created lazily by orchestrator/runtime when missing.
- For gated runs, `run_id` is mandatory. If unavailable, return `BLOCKED`.
- Every review gate update MUST overwrite the same run file and append a new `gate_entry`.
- Reviewer prompts MUST include a concise summary loaded from this file.

## Review Context Schema

- `run_id`
- `artifact_id`
- `gate`
- `reviewers`
- `new_findings`
- `resolved_findings`
- `carry_forward_findings`
- `finding_id`
- `first_seen_gate`
- `status` (`open` | `resolved` | `reopened`)
- `resolved_in_gate`
- `supersedes`
- `coverage_summary`
- `completeness_check`
- `context_file_path`
- `gate_entries`

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `review_context_loaded`: boolean
- `review_context_updated`: boolean
- `context_file_path`
- `unresolved_findings`
- `resolved_findings`
- `carry_forward_findings`

## Machine-Readable Enforcement Output (required)

```json
{
  "enforcement": {
    "required_invocations": ["woos-review-context"],
    "actually_invoked": ["woos-review-context"],
    "missing_invocations": [],
    "context_file_written": true,
    "invocation_evidence": [
      {
        "skill": "woos-review-context",
        "invoked_at": "2026-05-12T22:00:00Z",
        "artifact_ref": "<workspace_root>/hep/review-context/<run_id>.yaml",
        "output_digest": "sha256:..."
      }
    ],
    "finding_identity_checks_passed": true,
    "completeness_passed": true
  }
}
```

Missing `invocation_evidence` MUST return `BLOCKED`.
