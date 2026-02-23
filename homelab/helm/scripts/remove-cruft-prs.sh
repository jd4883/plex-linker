#!/usr/bin/env bash
# Create PRs to remove unwanted files (PR_DESCRIPTION.md, Chart.lock, charts/) from chart repos.
# Usage: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/scripts/remove-cruft-prs.sh [repo ...]
# With no args, uses repos that audit reported as having cruft (harbor, homelab-immich, homelab-nextcloud for PR_DESCRIPTION).

set -e
BRANCH="${BRANCH:-chore/remove-cruft}"
REPOS=("jd4883/harbor" "jd4883/homelab-immich" "jd4883/homelab-nextcloud")

[ $# -gt 0 ] && REPOS=("$@")
[ -z "${GH_TOKEN}" ] && echo "GH_TOKEN required" && exit 1

TMPD=$(mktemp -d)
trap 'rm -rf "$TMPD"' EXIT
export GH_TOKEN

for repo in "${REPOS[@]}"; do
  echo "--- $repo ---"
  git clone "https://x-access-token:${GH_TOKEN}@github.com/${repo}.git" "$TMPD/clone"
  cd "$TMPD/clone"
  git config user.email "jd4883@users.noreply.github.com"
  git config user.name "jd4883"
  default_branch=$(git remote show origin | awk '/HEAD branch/ { print $3 }')
  [ -z "$default_branch" ] && default_branch=main
  git checkout "$default_branch"
  git pull origin "$default_branch"
  git checkout -b "$BRANCH"
  to_remove=""
  [ -f PR_DESCRIPTION.md ] && git rm PR_DESCRIPTION.md && to_remove="${to_remove} PR_DESCRIPTION.md"
  [ -f Chart.lock ] && git rm Chart.lock && to_remove="${to_remove} Chart.lock"
  if [ -d charts ] && ls charts/*.tgz 1>/dev/null 2>&1; then
    git rm -rf charts/
    to_remove="${to_remove} charts/"
  fi
  if [ -z "$to_remove" ]; then
    echo "  No cruft to remove"
    cd - >/dev/null
    rm -rf "$TMPD/clone"
    continue
  fi
  git commit -m "chore: remove cruft (do not commit PR_DESCRIPTION, Chart.lock, charts)"
  git push origin "$BRANCH"
  gh pr create --base "$default_branch" --head "$BRANCH" --title "chore: remove PR_DESCRIPTION.md and other cruft" --body "Remove files that should not be in the repo: PR_DESCRIPTION.md (use only as PR body), Chart.lock, charts/*.tgz."
  cd - >/dev/null
  rm -rf "$TMPD/clone"
done
echo "Done."
