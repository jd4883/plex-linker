#!/usr/bin/env bash
# For chart repos with open PR #1: push workflows from workspace and update PR body from PR_DESCRIPTION.md.
# Run from repo root: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/update-open-prs-and-push-workflows.sh
# Note: Pushing workflow files requires GH_TOKEN with "workflow" scope; otherwise only PR body updates run.
set -euo pipefail
HELM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HELM_DIR/../.." && pwd)"
BRANCH="${BRANCH:-feature/initial-helm-chart}"

if [[ -z "${GH_TOKEN:-}" ]]; then
  echo "GH_TOKEN not set. Run with: GH_HOST=github.com op run --env-file=homelab/.env.gh -- $0"
  exit 1
fi

# repo | chart_name (for paths)
CHARTS=(
  "jd4883/homelab-mealie|mealie"
  "jd4883/homelab-paperless-ngx|paperless-ngx"
  "jd4883/homelab-gotify|gotify"
  "jd4883/homelab-postgresql-backup-to-minio|postgresql-backup-to-minio"
)

for entry in "${CHARTS[@]}"; do
  IFS='|' read -r repo chart_name <<< "$entry"
  CHART_SOURCE="$HELM_DIR/$chart_name"
  PR_BODY_FILE="$CHART_SOURCE/PR_DESCRIPTION.md"
  echo "=== $repo ==="
  if ! gh pr view 1 --repo "$repo" --json state -q .state 2>/dev/null; then
    echo "  No PR #1; skip."
    continue
  fi
  STATE=$(gh pr view 1 --repo "$repo" --json state -q .state)
  if [[ "$STATE" != "OPEN" ]]; then
    echo "  PR #1 is $STATE; skip push (workflows may already be on main)."
    if [[ -f "$PR_BODY_FILE" ]] && [[ "$STATE" = "MERGED" ]]; then
      echo "  (PR already merged; body update not needed.)"
    fi
    continue
  fi
  tmpdir=$(mktemp -d)
  trap "rm -rf $tmpdir" EXIT
  git clone "https://x-access-token:${GH_TOKEN}@github.com/${repo}.git" "$tmpdir"
  (
    cd "$tmpdir"
    git config user.email "jd4883@users.noreply.github.com"
    git config user.name "Jacob Dresdale"
    git fetch origin "$BRANCH" 2>/dev/null && git checkout "$BRANCH" 2>/dev/null || { echo "  Branch $BRANCH not found"; exit 1; }
    rsync -a --exclude='.git' --exclude='PR_DESCRIPTION*.md' --exclude='Chart.lock' "$CHART_SOURCE"/ .
    if [[ -d "$CHART_SOURCE/.github/workflows" ]]; then
      mkdir -p .github/workflows
      cp "$CHART_SOURCE"/.github/workflows/*.yml .github/workflows/
    fi
    git add -A
    if git diff --staged --quiet; then
      echo "  No changes to push."
    else
      git commit -m "chore: add release workflows and keep chart in sync"
      git push origin "$BRANCH"
      echo "  Pushed workflows."
    fi
  )
  trap - EXIT
  rm -rf "$tmpdir"
  if [[ -f "$PR_BODY_FILE" ]]; then
    BODY_ESC=$(jq -Rs . "$PR_BODY_FILE")
    gh api "repos/$repo/pulls/1" -X PATCH --input - <<< "{\"body\": $BODY_ESC}" && echo "  Updated PR body." || echo "  Could not update PR body (check gh auth)."
  fi
  echo ""
done
echo "Done."
