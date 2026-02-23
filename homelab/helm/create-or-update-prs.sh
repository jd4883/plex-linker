#!/usr/bin/env bash
# Create or update PRs using PR_DESCRIPTION.md bodies and 1Password for GH_TOKEN.
# Usage: from repo root, with homelab/.env.gh containing GH_TOKEN=op://Vault/Item/field
#   GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-or-update-prs.sh
# Optional: set HOMELAB_REPO=owner/repo if this repo has no remote (e.g. jd4883/home).

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HELM_DIR="$SCRIPT_DIR"
REPO_ROOT="$(cd "$HELM_DIR/../.." && pwd)"
cd "$REPO_ROOT"

# Resolve repo: HOMELAB_REPO env, or gh repo view, or git remote
REPO="${HOMELAB_REPO:-}"
if [[ -z "$REPO" ]]; then
  if REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null); then
    :
  elif REMOTE=$(git remote get-url origin 2>/dev/null); then
    REPO=$(echo "$REMOTE" | sed -n 's/.*github\.com[:/]\([^./]*\/[^./]*\)\.git/\1/p')
  fi
fi
if [[ -z "$REPO" ]]; then
  echo "Could not resolve repo. Set HOMELAB_REPO=owner/repo (e.g. jd4883/homelab) or add git remote origin."
  exit 1
fi

BRANCH=$(git branch --show-current)
if [[ -z "$BRANCH" ]]; then
  echo "Not on a branch."
  exit 1
fi

# Map current branch to chart and PR body file (for this repo's single PR)
PR_BODY_FILE=""
PR_TITLE=""
case "$BRANCH" in
  feature/kubernetes-dashboard-latest-okta)
    PR_BODY_FILE="$HELM_DIR/kubernetes-dashboard/PR_DESCRIPTION.md"
    PR_TITLE="🖥️ Kubernetes Dashboard — skip-login for Okta bypass"
    ;;
  feature/organizr-tab-controller-in-helm)
    PR_BODY_FILE="$HELM_DIR/organizr-tab-controller/PR_DESCRIPTION.md"
    PR_TITLE="📋 organizr-tab-controller chart in homelab/helm"
    ;;
  feature/secrets-immich-harbor-longhorn)
    PR_BODY_FILE="$HELM_DIR/PR_DESCRIPTION-secrets-helm-standards.md"
    PR_TITLE="🔐 Helm: removals, README standards, Mealie/Paperless-ngx/Gotify, Argo CD"
    ;;
  feature/unpackerr-chart-cue-splitting)
    PR_BODY_FILE="$HELM_DIR/unpackerr/PR_DESCRIPTION.md"
    PR_TITLE="📦 Unpackerr chart — CUE splitting, 1Password, Argo CD, release automation"
    ;;
  *)
    # Default: try kubernetes-dashboard if file exists (current branch often has dashboard changes)
    if [[ -f "$HELM_DIR/kubernetes-dashboard/PR_DESCRIPTION.md" ]]; then
      PR_BODY_FILE="$HELM_DIR/kubernetes-dashboard/PR_DESCRIPTION.md"
      PR_TITLE="🖥️ Kubernetes Dashboard — skip-login for Okta bypass"
    fi
    ;;
esac

if [[ -z "$PR_BODY_FILE" || ! -f "$PR_BODY_FILE" ]]; then
  echo "No PR body mapped for branch $BRANCH. Create PR manually or add branch mapping in script."
  exit 1
fi

# Create or update PR
EXISTING=$(gh pr list --head "$BRANCH" --repo "$REPO" --json number -q '.[0].number' 2>/dev/null || true)
if [[ -n "$EXISTING" ]]; then
  echo "Updating existing PR #$EXISTING..."
  gh pr edit "$EXISTING" --repo "$REPO" --body-file "$PR_BODY_FILE" --title "$PR_TITLE"
  echo "Updated: https://github.com/$REPO/pull/$EXISTING"
else
  echo "Creating draft PR..."
  gh pr create --draft --base main --head "$BRANCH" --repo "$REPO" --title "$PR_TITLE" --body-file "$PR_BODY_FILE"
  echo "Created. Run: gh pr view --repo $REPO --web"
fi

# Cleanup ephemeral PR body files (per CHART_STANDARD: do not commit — use as PR body only)
if [[ "$PR_BODY_FILE" != *"PULL_REQUEST_TEMPLATE.md" ]]; then
  rm -f "$PR_BODY_FILE"
  echo "Removed $PR_BODY_FILE (ephemeral)."
fi

# Remove assessment doc (one-time use)
rm -f "$HELM_DIR/RECENT_CHARTS_PR_ASSESSMENT.md"
echo "Removed RECENT_CHARTS_PR_ASSESSMENT.md (ephemeral)."
