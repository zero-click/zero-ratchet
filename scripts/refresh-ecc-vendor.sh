#!/usr/bin/env bash
# Refresh vendored ECC snapshot from a local ECC checkout.
#
# Usage: scripts/refresh-ecc-vendor.sh <path-to-ecc-repo>
#
# Overwrites vendor/ecc/ in place. Review the diff and commit.

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path-to-ecc-repo>" >&2
  exit 1
fi

ECC="$1"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$REPO_ROOT/vendor/ecc"

if [ ! -d "$ECC/skills" ] || [ ! -d "$ECC/rules" ] || [ ! -f "$ECC/mcp-configs/mcp-servers.json" ]; then
  echo "Error: $ECC does not look like an ECC repo (missing skills/, rules/, or mcp-configs/mcp-servers.json)" >&2
  exit 1
fi

SKILLS=(
  git-workflow
  search-first
  deep-research
  dmux-workflows
  tdd-workflow
  coding-standards
  verification-loop
  api-design
  browser-qa
  security-review
  architecture-decision-records
  e2e-testing
  deployment-patterns
  database-migrations
  codebase-onboarding
)

echo "Refreshing vendored ECC snapshot from: $ECC"

rm -rf "$VENDOR/skills" "$VENDOR/rules" "$VENDOR/mcp-configs"
mkdir -p "$VENDOR/skills" "$VENDOR/rules" "$VENDOR/mcp-configs"

for s in "${SKILLS[@]}"; do
  if [ ! -d "$ECC/skills/$s" ]; then
    echo "  ! missing upstream skill: $s (skipped)"
    continue
  fi
  cp -R "$ECC/skills/$s" "$VENDOR/skills/"
  echo "  ✓ skill: $s"
done

cp -R "$ECC/rules/." "$VENDOR/rules/"
echo "  ✓ rules synced"

cp "$ECC/mcp-configs/mcp-servers.json" "$VENDOR/mcp-configs/"
echo "  ✓ mcp-configs synced"

echo
echo "Done. Review with: git -C $REPO_ROOT status vendor/ecc"
