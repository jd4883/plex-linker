#!/usr/bin/env bash
# One-time: if you pushed v3 to main by mistake, this moves that work to feature/plex-linker-v3 and restores main.
# Run from repo root. Requires GH_TOKEN (e.g. op run --env-file=homelab/.env.gh -- bash this-script).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
DEV_BRANCH="feature/plex-linker-v3"
git fetch origin
# Main before any mistaken push (clone default)
MAIN_BEFORE="47df019f86de0d7d691c5c012c2844453a66f2b6"
if [[ "$(git rev-parse origin/main)" = "$MAIN_BEFORE" ]]; then
  echo "origin/main is already at $MAIN_BEFORE; nothing to fix."
  exit 0
fi
echo "Moving origin/main commits to $DEV_BRANCH and restoring main to $MAIN_BEFORE..."
git checkout -B "$DEV_BRANCH" origin/main
git push -u origin "$DEV_BRANCH"
git push origin "$MAIN_BEFORE:refs/heads/main" --force
git checkout main
git reset --hard origin/main
echo "Done. main is restored; v3 work is on $DEV_BRANCH. Create PR: gh pr create --base main --head $DEV_BRANCH --title '...' --body-file PR_DESCRIPTION.md"
