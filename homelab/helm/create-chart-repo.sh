#!/usr/bin/env bash
# Create jd4883/homelab-<CHART> (if missing), push chart from homelab/helm/<CHART>, open PR.
# Usage: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-chart-repo.sh <chart_name>
# Example: ... create-chart-repo.sh mealie
# Chart name = directory under homelab/helm (e.g. mealie, paperless-ngx, gotify, postgresql-backup-to-minio, onepassword-secrets).
set -euo pipefail
HELM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_OWNER="${GITHUB_OWNER:-jd4883}"
BRANCH="${BRANCH:-feature/initial-helm-chart}"

CHART_NAME="${1:-}"
if [[ -z "$CHART_NAME" ]]; then
  echo "Usage: $0 <chart_name>   # e.g. mealie, paperless-ngx, gotify, postgresql-backup-to-minio"
  exit 1
fi
if [[ "$CHART_NAME" = "onepassword-secrets" ]]; then
  echo "onepassword-secrets uses the existing repo jd4883/onepassword-secrets (private). Do not create homelab-onepassword-secrets."
  exit 1
fi

REPO_SUFFIX="homelab-${CHART_NAME}"
REPO_FULL="${REPO_OWNER}/${REPO_SUFFIX}"
CHART_SOURCE="$HELM_DIR/$CHART_NAME"
PR_BODY_FILE="$CHART_SOURCE/PR_DESCRIPTION.md"

if [ -z "${GH_TOKEN:-}" ]; then
  echo "GH_TOKEN is not set. Run with: GH_HOST=github.com op run --env-file=homelab/.env.gh -- $0 $CHART_NAME"
  exit 1
fi

if [[ ! -d "$CHART_SOURCE" ]] || [[ ! -f "$CHART_SOURCE/Chart.yaml" ]]; then
  echo "Chart not found at $CHART_SOURCE (expected $HELM_DIR/$CHART_NAME/Chart.yaml)."
  exit 1
fi

# Description for gh repo create (short; full text in set-repo-descriptions.sh)
declare -A DESC=(
  ["mealie"]="Mealie recipe manager. Argo CD."
  ["paperless-ngx"]="Paperless-ngx document management. Argo CD."
  ["gotify"]="Gotify push notifications. Argo CD."
  ["postgresql-backup-to-minio"]="PostgreSQL backup to MinIO (CronJob). Argo CD."
)
DESCRIPTION="${DESC[$CHART_NAME]:-$(awk '/^description:/ { $1=""; gsub(/^[ \t"]+|[ \t"]+$/,""); print; exit }' "$CHART_SOURCE/Chart.yaml")}"
[[ -z "$DESCRIPTION" ]] && DESCRIPTION="Helm chart. Argo CD."

_gh_url() { echo "https://x-access-token:${GH_TOKEN}@github.com/${1}.git"; }

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

if ! gh repo view "$REPO_FULL" &>/dev/null; then
  echo "Creating repo $REPO_FULL..."
  gh repo create "$REPO_FULL" --public --description "$DESCRIPTION" --add-readme
fi

echo "Cloning $REPO_FULL..."
git clone "$(_gh_url "$REPO_FULL")" "$tmpdir"

(
  cd "$tmpdir"
  git config user.email "${REPO_OWNER}@users.noreply.github.com"
  git config user.name "${REPO_OWNER}"
  git fetch origin "$BRANCH" 2>/dev/null && git checkout -b "$BRANCH" "origin/$BRANCH" 2>/dev/null || git checkout -b "$BRANCH"
  rm -f README.md
  if command -v rsync &>/dev/null; then
    rsync -a --exclude='.git' --exclude='PR_DESCRIPTION*.md' --exclude='Chart.lock' "$CHART_SOURCE"/ .
  else
    tar cf - -C "$CHART_SOURCE" . | tar xf -
    rm -rf .git 2>/dev/null || true
    rm -f PR_DESCRIPTION.md PR_DESCRIPTION*.md Chart.lock 2>/dev/null || true
  fi
  # Include .github/workflows if present (release-on-merge, release-notes)
  if [ -d "$CHART_SOURCE/.github/workflows" ]; then
    mkdir -p .github/workflows
    cp "$CHART_SOURCE"/.github/workflows/*.yml .github/workflows/ 2>/dev/null || true
  fi
  git add -A
  if git diff --staged --quiet; then
    echo "No changes for $CHART_NAME chart."
    exit 0
  fi
  git commit -m "feat: $CHART_NAME Helm chart — initial (Argo CD)"
  git push -u origin "$BRANCH"
  if gh pr view --repo "$REPO_FULL" --head "$BRANCH" &>/dev/null; then
    echo "PR already exists: https://github.com/$REPO_FULL/pulls"
  else
    PR_TITLE="Initial $CHART_NAME Helm chart"
    if [[ -f "$PR_BODY_FILE" ]]; then
      gh pr create --base main --head "$BRANCH" --title "$PR_TITLE" --body-file "$PR_BODY_FILE"
    else
      gh pr create --base main --head "$BRANCH" --title "$PR_TITLE" --body "Initial Helm chart for $CHART_NAME. Argo CD syncs from this repo with path \".\"."
    fi
    echo "PR: https://github.com/$REPO_FULL/pulls"
  fi
)

echo "Done. Argo CD (config.yaml) can sync from $REPO_FULL with path \".\"."
