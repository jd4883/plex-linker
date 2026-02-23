#!/usr/bin/env bash
# Push chart content from home repo to the two CronJob chart repos' PR branches and update PR descriptions.
# Run with 1Password so you get prompted for creds:
#   From repo root: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/sync-cronjob-chart-prs.sh
set -e
HELM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_OWNER="${GITHUB_OWNER:-jd4883}"
BRANCH="${BRANCH:-feature/initial-helm-chart}"

if [ -z "${GH_TOKEN:-}" ]; then
  echo "GH_TOKEN is not set. Run with: GH_HOST=github.com op run --env-file=homelab/.env.gh -- $0"
  exit 1
fi

_gh_url() { echo "https://x-access-token:${GH_TOKEN}@github.com/${1}.git"; }

_pr_body() {
  local repo_name=$1
  cat << EOF
Generic CronJob chart; expects existing Secret (e.g. from 1Password in Plex chart).

## After you merge

GitHub Actions will run automatically:

1. **Release on merge to main** – Lint chart, then bump patch version, create tag (e.g. \`v0.1.0\`) and GitHub Release.
2. **Release notes** (if configured) – Populate release body from PR.
3. **Helm chart publish** – Package the chart, upload \`.tgz\` to the GitHub Release, and publish the Helm repo index to the \`gh-pages\` branch so you can:
   \`\`\`
   helm repo add <name> https://${REPO_OWNER}.github.io/${repo_name}
   helm install <name> <name>/<chart> ...
   \`\`\`
EOF
}

_sync_one() {
  local repo_full=$1
  local chart_name=$2
  local repo_name=${repo_full#*/}
  local tmpdir
  tmpdir=$(mktemp -d)
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
    else
      GIT_AUTHOR_EMAIL="${REPO_OWNER}@users.noreply.github.com" GIT_COMMITTER_EMAIL="${REPO_OWNER}@users.noreply.github.com" \
        git commit -m "ci: add helm-publish workflow and release-on-merge docs"
      git push -u origin "$BRANCH"
      echo "Pushed to $repo_full $BRANCH"
    fi
  ) )
  rm -rf "$tmpdir"

  # Update PR description (PR #1 for branch feature/initial-helm-chart)
  pr_num=$(gh pr list --repo "$repo_full" --head "$BRANCH" --json number -q '.[0].number' 2>/dev/null || true)
  if [ -n "$pr_num" ]; then
    _pr_body "$repo_name" | gh pr edit "$pr_num" --repo "$repo_full" --body-file -
    echo "Updated PR #$pr_num in $repo_full"
  else
    echo "No PR found for $repo_full head $BRANCH; create one manually if needed."
  fi
}

echo "Syncing chart content and PR descriptions (owner: $REPO_OWNER, branch: $BRANCH)..."

_sync_one "${REPO_OWNER}/one-pace-plex-assistant-helm-chart" "one-pace-plex-assistant"
_sync_one "${REPO_OWNER}/plex-prefer-non-forced-subs-helm-chart" "plex-prefer-non-forced-subs"

echo "Done."
