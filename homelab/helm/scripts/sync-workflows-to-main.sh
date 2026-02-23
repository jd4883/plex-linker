#!/usr/bin/env bash
# Sync chart content (including .github/workflows) from workspace to each chart repo's main branch and push.
# Same pattern as create-chart-repo: rsync chart + workflows, commit, push to main.
# Usage: GH_HOST=github.com op run --env-file=homelab/.env.gh -- bash ./homelab/helm/scripts/sync-workflows-to-main.sh
set -e
HELM_DIR="${HELM_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
REPO_ROOT="${REPO_ROOT:-$(cd "$HELM_DIR/../.." && pwd)}"
[ -z "${GH_TOKEN}" ] && echo "GH_TOKEN required" && exit 1

REPOS=(
  "jd4883/homelab-unpackerr:unpackerr"
  "jd4883/homelab-prometheus:prometheus"
  "jd4883/homelab-mealie:mealie"
  "jd4883/homelab-paperless-ngx:paperless-ngx"
  "jd4883/homelab-gotify:gotify"
  "jd4883/homelab-postgresql-backup-to-minio:postgresql-backup-to-minio"
)

for entry in "${REPOS[@]}"; do
  repo="${entry%%:*}"
  chart="${entry##*:}"
  src="$REPO_ROOT/homelab/helm/$chart"
  [ ! -d "$src" ] || [ ! -f "$src/Chart.yaml" ] && echo "Skip $repo: no chart at $src" && continue
  echo "=== $repo ==="
  tmpdir=$(mktemp -d)
  trap "rm -rf $tmpdir" EXIT
  git clone "https://x-access-token:${GH_TOKEN}@github.com/${repo}.git" "$tmpdir"
  (
    cd "$tmpdir"
    git config user.email "jd4883@users.noreply.github.com"
    git config user.name "Jacob Dresdale"
    default_branch=$(git remote show origin 2>/dev/null | awk '/HEAD branch/ { print $3 }') || default_branch=main
    git checkout "$default_branch"
    git pull origin "$default_branch"
    rsync -a --exclude='.git' --exclude='PR_DESCRIPTION*.md' --exclude='Chart.lock' "$src"/ .
    mkdir -p .github/workflows
    [ -d "$src/.github/workflows" ] && cp "$src"/.github/workflows/*.yml .github/workflows/ 2>/dev/null || true
    git add -A
    if git diff --staged --quiet; then
      echo "  No changes"
    else
      git commit -m "chore: sync chart and add release workflows"
      git push origin "$default_branch" && echo "  Pushed to $default_branch"
    fi
  )
  rm -rf "$tmpdir"
  trap - EXIT
done
echo "Done."
