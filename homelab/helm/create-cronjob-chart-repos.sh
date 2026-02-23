#!/usr/bin/env bash
# Create the two CronJob chart repos on GitHub, push chart content on a feature branch, and open PRs.
# Prereqs: gh auth login (gh auth status must succeed). Run from repo root or from homelab/helm.
set -e
HELM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_OWNER="${GITHUB_OWNER:-jd4883}"
BRANCH="${BRANCH:-feature/initial-helm-chart}"

_push_chart() {
  local repo_full=$1
  local chart_name=$2
  local desc=$3
  local tmpdir
  tmpdir=$(mktemp -d)
  trap "rm -rf $tmpdir" RETURN
  if ! gh repo view "$repo_full" &>/dev/null; then
    # Create with README so main exists; we replace content via branch + PR
    gh repo create "$repo_full" --public --description "$desc" --add-readme
  fi
  git clone "git@github.com:${repo_full}.git" "$tmpdir"
  cd "$tmpdir"
  git checkout -b "$BRANCH"
  rm -f README.md
  cp -r "$HELM_DIR/$chart_name"/* .
  git add -A
  if git diff --staged --quiet; then
    echo "No changes for $chart_name."
    return
  fi
  git commit -m "feat: initial Helm chart for $chart_name"
  git push -u origin "$BRANCH"
  gh pr create --base main --head "$BRANCH" --title "Initial Helm chart" --body "Generic CronJob chart; expects existing Secret (e.g. from 1Password in Plex chart)."
  echo "PR: https://github.com/$repo_full/pulls"
}

echo "Creating repos and opening PRs (owner: $REPO_OWNER, branch: $BRANCH)..."

_push_chart "${REPO_OWNER}/one-pace-plex-assistant-helm-chart" "one-pace-plex-assistant" \
  "Helm chart for One Pace Plex Assistant CronJob (generic; expects existing Secret)"

_push_chart "${REPO_OWNER}/plex-prefer-non-forced-subs-helm-chart" "plex-prefer-non-forced-subs" \
  "Helm chart for Plex prefer non-forced subs CronJob (generic; expects existing Secret)"

echo "Done. Merge the PRs, then set plex Chart.yaml deps to (and publish Helm index to GitHub Pages if needed):"
echo "  repository: https://${REPO_OWNER}.github.io/one-pace-plex-assistant-helm-chart"
echo "  repository: https://${REPO_OWNER}.github.io/plex-prefer-non-forced-subs-helm-chart"
