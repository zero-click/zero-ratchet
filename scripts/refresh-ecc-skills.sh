#!/usr/bin/env bash
# Refresh the snapshot of upstream ECC skills under skills/ecc/.
#
# Usage: scripts/refresh-ecc-skills.sh <path-to-ecc-repo>
#
# Overwrites skills/ecc/ in place. Review the diff and commit.

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path-to-ecc-repo>" >&2
  exit 1
fi

ECC="$1"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO_ROOT/skills/ecc"

if [ ! -d "$ECC/skills" ]; then
  echo "Error: $ECC does not look like an ECC repo (missing skills/)" >&2
  exit 1
fi

SKILLS=(
  git-workflow
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

echo "Refreshing ECC skill snapshot from: $ECC"

rm -rf "$DEST"
mkdir -p "$DEST"

for s in "${SKILLS[@]}"; do
  if [ ! -d "$ECC/skills/$s" ]; then
    echo "  ! missing upstream skill: $s (skipped)"
    continue
  fi
  cp -R "$ECC/skills/$s" "$DEST/"
  echo "  ✓ skill: $s"
done

echo
echo "Done. Review with: git -C $REPO_ROOT status skills/ecc"
