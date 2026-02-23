#!/usr/bin/env bash
# Ensure we're on a dev branch (not main), commit any changes, then push and create PR.
# Run with: GH_HOST=github.com op run --env-file=<path-to-.env.gh> -- bash scripts/ensure-dev-branch-and-push-pr.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
DEV_BRANCH="${PLEX_LINKER_DEV_BRANCH:-feature/plex-linker-v3}"
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" = "main" ]]; then
  git checkout -b "$DEV_BRANCH" 2>/dev/null || git checkout "$DEV_BRANCH"
  BRANCH=$(git branch --show-current)
fi
if ! git diff --staged --quiet || ! git diff --quiet; then
  git add -A
  git commit -m "feat: Plex Linker v3 — deploy/helm, optional media, release automation, post-link refresh

- deploy/helm: Chart 3.0.0, optional media.mountPath, conditional volume/MEDIA_ROOT
- App: early return when no media root; Sonarr RescanSeries (seriesId); Radarr RescanMovie after link
- Workflows: release-on-merge (initial_version 3.0.0), docker-build-push, release-notes
- PR_DESCRIPTION and scripts for push/PR with op"
fi
exec bash "$(git rev-parse --show-toplevel)/scripts/push-and-pr.sh"
