#!/usr/bin/env bash
# Create PRs to remove unwanted files (PR_DESCRIPTION.md, Chart.lock, charts/, .DS_Store) from chart repos.
# Commits use author Jacob Dresdale so you remain the sole contributor (no Cursor/bot).
# Usage: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/scripts/remove-cruft-prs.sh [repo ...]
# With no args, uses repos that audit reported as having cruft (harbor, homelab-immich, homelab-nextcloud for PR_DESCRIPTION).

set -e
BRANCH="${BRANCH:-chore/remove-cruft}"
REPOS=("jd4883/harbor" "jd4883/homelab-immich" "jd4883/homelab-nextcloud")
# Author: you as contributor (never Cursor/agent)
GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-Jacob Dresdale}"
GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-jd4883@users.noreply.github.com}"
export GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME" GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"

[ $# -gt 0 ] && REPOS=("$@")
[ -z "${GH_TOKEN}" ] && echo "GH_TOKEN required" && exit 1

TMPD=$(mktemp -d)
trap 'rm -rf "$TMPD"' EXIT
export GH_TOKEN

for repo in "${REPOS[@]}"; do
  echo "--- $repo ---"
  git clone "https://x-access-token:${GH_TOKEN}@github.com/${repo}.git" "$TMPD/clone"
  cd "$TMPD/clone"
  git config user.email "$GIT_AUTHOR_EMAIL"
  git config user.name "$GIT_AUTHOR_NAME"
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
  # .DS_Store: remove from tracking and ensure .gitignore
  while IFS= read -r f; do git rm --cached "$f" 2>/dev/null && to_remove="${to_remove} $f"; done < <(git ls-files 2>/dev/null | grep '\.DS_Store$' || true)
  if [ -f .gitignore ]; then
    grep -q '^\.DS_Store$' .gitignore || { echo '.DS_Store' >> .gitignore; git add .gitignore; to_remove="${to_remove} .gitignore"; }
  else
    echo '.DS_Store' > .gitignore
    git add .gitignore
    to_remove="${to_remove} .gitignore"
  fi
  if [ -z "$to_remove" ] && git diff --staged --quiet 2>/dev/null; then
    echo "  No cruft to remove"
    cd - >/dev/null
    rm -rf "$TMPD/clone"
    continue
  fi
  git commit -m "chore: remove cruft (.DS_Store, PR_DESCRIPTION, Chart.lock, charts); ensure .gitignore has .DS_Store"
  git push origin "$BRANCH"
  gh pr create --base "$default_branch" --head "$BRANCH" --title "chore: remove cruft and add .DS_Store to .gitignore" --body "Remove files that should not be in the repo: .DS_Store (and ensure .gitignore), PR_DESCRIPTION.md (use only as PR body), Chart.lock, charts/*.tgz. All commits are by the repo owner (no bot/Cursor)."
  cd - >/dev/null
  rm -rf "$TMPD/clone"
done
echo "Done."
