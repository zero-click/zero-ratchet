# Vendored ECC artifacts

This directory contains a frozen snapshot of upstream ECC artifacts that the
profile depends on. Vendoring them removes the install-time requirement to
point `install-profile.py` at a local ECC repo.

## Contents

- `skills/` — 15 ECC native skills referenced by Hermes workflows
- `rules/` — ECC rule packs (per-language + common)
- `mcp-configs/mcp-servers.json` — recommended MCP server definitions

## Refreshing from upstream

Run `scripts/refresh-ecc-vendor.sh <path-to-ecc-repo>` from the repo root.
The script overwrites the snapshot in place. Commit the diff to lock the
new version.

## Upstream

ECC repo: <https://github.com/everything-claude-code/everything-claude-code>
(or the local checkout used during refresh).

## Notes

- `production-audit` was removed from upstream and is therefore not vendored.
  If the workflow ever references it, replace with a current ECC skill or
  drop the reference.
