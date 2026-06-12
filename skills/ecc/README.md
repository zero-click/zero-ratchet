# ECC Skills (upstream snapshot)

A frozen snapshot of upstream ECC (Everything Claude Code) skills used by the
local workflow.

**Do not hand-edit.** This directory is rewritten by
`scripts/refresh-ecc-skills.sh`. Local extensions belong under
`skills/software-development/` (with the `woos-` prefix) or
`skills/product-design/`.

## Refresh

```bash
scripts/refresh-ecc-skills.sh /path/to/everything-claude-code
git diff skills/ecc
git add skills/ecc && git commit
```

## Upstream

<https://github.com/everything-claude-code/everything-claude-code>

## Notes

- `production-audit` was removed from upstream. The local rewrite lives at
  `skills/software-development/woos-production-audit/`.
