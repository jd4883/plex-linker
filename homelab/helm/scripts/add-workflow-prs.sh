#!/usr/bin/env bash
# Create PRs that add release-on-merge and release-notes workflows to chart repos that lack them.
# Usage: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/scripts/add-workflow-prs.sh
# Requires: GH_TOKEN in env (with repo + workflow scope for pushing workflow files).

set -e
HELM_DIR="${HELM_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
REPO_ROOT="${REPO_ROOT:-$(cd "$HELM_DIR/../.." && pwd)}"
BRANCH="${BRANCH:-chore/add-github-actions}"

if [ -z "${GH_TOKEN}" ]; then
  echo "GH_TOKEN not set. Run with: op run --env-file=homelab/.env.gh -- $0"
  exit 1
fi

# repo_owner/repo_name <- path under helm/ (workflow source)
REPOS=(
  "jd4883/homelab-unpackerr:unpackerr"
  "jd4883/homelab-prometheus:prometheus"
  "jd4883/homelab-mealie:mealie"
  "jd4883/homelab-paperless-ngx:paperless-ngx"
  "jd4883/homelab-gotify:gotify"
  "jd4883/homelab-postgresql-backup-to-minio:postgresql-backup-to-minio"
  "jd4883/longhorn:longhorn"
)

TMPD=$(mktemp -d)
trap 'rm -rf "$TMPD"' EXIT
export GH_TOKEN

for entry in "${REPOS[@]}"; do
  repo="${entry%%:*}"
  chart="${entry##*:}"
  echo "--- $repo (from helm/$chart) ---"
  src="$REPO_ROOT/homelab/helm/$chart/.github/workflows"
  if [ ! -d "$src" ]; then
    echo "  Skip: no $src"
    continue
  fi
  git clone "https://x-access-token:${GH_TOKEN}@github.com/${repo}.git" "$TMPD/clone"
  cd "$TMPD/clone"
  git config user.email "jd4883@users.noreply.github.com"
  git config user.name "Jacob Dresdale"
  default_branch=$(git remote show origin | awk '/HEAD branch/ { print $3 }')
  [ -z "$default_branch" ] && default_branch=main
  git checkout "$default_branch"
  git pull origin "$default_branch"
  if git show-ref -q "refs/heads/$BRANCH"; then
    git branch -D "$BRANCH"
  fi
  git checkout -b "$BRANCH"
  mkdir -p .github/workflows
  for f in "$src"/*.yml; do
    [ -f "$f" ] || continue
    cp "$f" .github/workflows/
  done
  git add .github/workflows
  if git diff --staged --quiet; then
    echo "  No workflow changes; skip PR"
    cd - >/dev/null
    rm -rf "$TMPD/clone"
    continue
  fi
  git commit -m "chore: add release-on-merge and release-notes workflows"
  git push origin "$BRANCH"
  gh pr create --base "$default_branch" --head "$BRANCH" --title "chore: add GitHub Actions (release on merge + release notes)" --body "Adds workflows from expectedbehaviors/github-actions so that merges to $default_branch create a release and release notes are filled from the merged PR."
  cd - >/dev/null
  rm -rf "$TMPD/clone"
done
echo "Done."
