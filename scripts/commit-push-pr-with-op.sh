#!/usr/bin/env bash
# From anywhere: create branch, commit all v3 changes, push and create PR using op for GH_TOKEN.
# Usage: ENV_GH=/path/to/.env.gh bash scripts/commit-push-pr-with-op.sh
#    or from home repo: bash personal_projects/docker/plex-linker/scripts/commit-push-pr-with-op.sh
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"
BRANCH="${PLEX_LINKER_PR_BRANCH:-feature/plex-linker-v3}"
ENV_GH="${PLEX_LINKER_GH_ENV:-}"
if [[ -z "$ENV_GH" ]]; then
  HOME_REPO="$(cd "$REPO_ROOT/../.." 2>/dev/null && pwd || echo "")"
  if [[ -f "$HOME_REPO/homelab/.env.gh" ]]; then
    ENV_GH="$HOME_REPO/homelab/.env.gh"
  fi
fi
if [[ -z "$ENV_GH" || ! -f "$ENV_GH" ]]; then
  echo "Set PLEX_LINKER_GH_ENV to path to .env.gh (with GH_TOKEN=op://...), or run from home repo with homelab/.env.gh"
  exit 1
fi
git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
git add -A
git status --short
if git diff --staged --quiet; then
  echo "Nothing to commit (already committed?). Pushing and creating PR..."
else
  git commit -m "feat: Plex Linker v3 — deploy/helm, optional media, release automation, post-link refresh

- deploy/helm: Chart 3.0.0, optional media.mountPath, conditional volume/MEDIA_ROOT
- App: early return when no media root; Sonarr RescanSeries (seriesId); Radarr RescanMovie after link
- Workflows: release-on-merge (initial_version 3.0.0), docker-build-push, release-notes
- PR_DESCRIPTION and scripts for push/PR with op"
fi
exec env GH_HOST=github.com op run --env-file="$ENV_GH" -- bash "$REPO_ROOT/scripts/push-and-pr.sh"
