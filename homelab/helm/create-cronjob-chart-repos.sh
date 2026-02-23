#!/usr/bin/env bash
# Create the two CronJob chart repos on GitHub, push chart content on a feature branch, and open PRs.
# Run with 1Password so you get prompted for creds (no need to be logged in to gh):
#   From repo root: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-cronjob-chart-repos.sh
# homelab/.env.gh must contain: GH_TOKEN=op://Vault/Item/field
set -e
HELM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_OWNER="${GITHUB_OWNER:-jd4883}"
BRANCH="${BRANCH:-feature/initial-helm-chart}"

if [ -z "${GH_TOKEN:-}" ]; then
  echo "GH_TOKEN is not set. Run with: GH_HOST=github.com op run --env-file=homelab/.env.gh -- $0"
  exit 1
fi

# HTTPS URL for clone/push using token (no SSH needed)
_gh_url() { echo "https://x-access-token:${GH_TOKEN}@github.com/${1}.git"; }

_push_chart() {
  local repo_full=$1
  local chart_name=$2
  local desc=$3
  local tmpdir
  tmpdir=$(mktemp -d)
  if ! gh repo view "$repo_full" &>/dev/null; then
    gh repo create "$repo_full" --public --description "$desc" --add-readme
  fi
  git clone "$(_gh_url "$repo_full")" "$tmpdir"
  ( cd "$tmpdir" && (
    git config user.email "${REPO_OWNER}@users.noreply.github.com"
    git config user.name "${REPO_OWNER}"
    git fetch origin "$BRANCH" 2>/dev/null && git checkout -b "$BRANCH" "origin/$BRANCH" 2>/dev/null || git checkout -b "$BRANCH"
    rm -f README.md
    cp -r "$HELM_DIR/$chart_name"/. .
    git add -A
    if git diff --staged --quiet; then
      echo "No changes for $chart_name."
      exit 0
    fi
    GIT_AUTHOR_EMAIL="${REPO_OWNER}@users.noreply.github.com" GIT_COMMITTER_EMAIL="${REPO_OWNER}@users.noreply.github.com" \
      git commit -m "feat: initial Helm chart for $chart_name"
    git push -u origin "$BRANCH"
    gh pr create --base main --head "$BRANCH" --title "Initial Helm chart" --body "Generic CronJob chart; expects existing Secret (e.g. from 1Password in Plex chart)."
    echo "PR: https://github.com/$repo_full/pulls"
  ) )
  rm -rf "$tmpdir"
}

echo "Creating repos and opening PRs (owner: $REPO_OWNER, branch: $BRANCH)..."

_push_chart "${REPO_OWNER}/one-pace-plex-assistant-helm-chart" "one-pace-plex-assistant" \
  "Helm chart for One Pace Plex Assistant CronJob (generic; expects existing Secret)"

_push_chart "${REPO_OWNER}/plex-prefer-non-forced-subs-helm-chart" "plex-prefer-non-forced-subs" \
  "Helm chart for Plex prefer non-forced subs CronJob (generic; expects existing Secret)"

echo "Done. Merge the PRs, then set plex Chart.yaml deps to (and publish Helm index to GitHub Pages if needed):"
echo "  repository: https://${REPO_OWNER}.github.io/one-pace-plex-assistant-helm-chart"
echo "  repository: https://${REPO_OWNER}.github.io/plex-prefer-non-forced-subs-helm-chart"
