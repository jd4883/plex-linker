#!/usr/bin/env bash
# Single script: fix branch, commit, push, create PR. Run this in your terminal (Cursor agent shell can't spawn zsh).
# From repo root: bash RUN-PR-NOW.sh
set -euo pipefail
cd "$(dirname "$0")"
ENV_GH="${PLEX_LINKER_GH_ENV:-/Users/jacob.dresdale/Documents/Repositories/home/homelab/.env.gh}"
git checkout -b feature/plex-linker-v3 2>/dev/null || git checkout feature/plex-linker-v3
git add -A
git diff --cached --quiet || git commit -m "feat: Plex Linker v3 — deploy/helm, optional media, release automation, post-link refresh"
GH_HOST=github.com op run --env-file="$ENV_GH" -- git push -u origin feature/plex-linker-v3
GH_HOST=github.com op run --env-file="$ENV_GH" -- gh pr create --base main --head feature/plex-linker-v3 \
  --title "Plex Linker v3 — bjw-s chart, optional media, release automation, post-link refresh" \
  --body-file PR_DESCRIPTION.md
echo "Done. PR created."
