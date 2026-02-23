#!/usr/bin/env bash
# Push current branch and create PR using GitHub token from 1Password.
# Run from repo root: GH_HOST=github.com op run --env-file=<path-to-.env.gh> -- bash scripts/push-and-pr.sh
# 1Password may prompt to sign in or unlock; complete the prompt in the terminal.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" = "main" ]]; then
  echo "ERROR: On main. Create/use a dev branch first, e.g.: git checkout -b feature/plex-linker-v3 && git add -A && git commit -m 'feat: Plex Linker v3 ...'"
  exit 1
fi
echo "Branch: $BRANCH | Repo root: $(pwd)"
if [[ -z "${GH_TOKEN:-}" ]]; then
  echo "GH_TOKEN not set. Run with: GH_HOST=github.com op run --env-file=<path-to-.env.gh> -- bash $0"
  exit 1
fi
echo "Pushing to origin/$BRANCH..."
git push -u origin "$BRANCH"
echo "Creating PR..."
gh pr create --base main --head "$BRANCH" \
  --title "Plex Linker v3 — bjw-s chart, optional media, release automation, post-link refresh" \
  --body-file PR_DESCRIPTION.md
echo "Done."
