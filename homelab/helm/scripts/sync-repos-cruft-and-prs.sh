#!/usr/bin/env bash
# Sync homelab/helm chart repos: switch to main when current branch is merged; create chore PR for
# cruft (.DS_Store, .gitignore) and consistent GitHub Actions. Author: Jacob Dresdale (no Cursor/bot).
# Run from workspace root: GH_HOST=github.com op run --env-file=homelab/.env.gh -- bash homelab/helm/scripts/sync-repos-cruft-and-prs.sh
set -euo pipefail
export GH_HOST=github.com
HELM="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$HELM/../.." && pwd)"
BRANCH="${BRANCH:-chore/cruft-dsstore-and-consistency}"
GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-Jacob Dresdale}"
GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-jd4883@users.noreply.github.com}"
export GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME" GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"

# With GH_TOKEN: push and create PRs. Without: local commits only.

do_repo() {
  local dir="$1"
  local rel="${dir#$REPO_ROOT/}"
  [[ -e "$dir/.git" ]] || return 0
  (cd "$dir" && git rev-parse --show-toplevel 2>/dev/null) | grep -q . || return 0
  [[ "$(cd "$dir" && pwd)" == "$(cd "$dir" && git rev-parse --show-toplevel)" ]] || return 0

  echo "=== $rel ==="
  (
    set +e
    cd "$dir"
    git config user.name "$GIT_AUTHOR_NAME"
    git config user.email "$GIT_AUTHOR_EMAIL"
    git fetch origin 2>/dev/null || true
    base=main
    for b in main master; do
      git show-ref -q "refs/remotes/origin/$b" 2>/dev/null && { base="$b"; break; }
    done
    current=$(git branch --show-current 2>/dev/null)
    # If current branch is merged into origin/main, switch to main and pull
    if [[ -n "$current" ]] && [[ "$current" != "$base" ]]; then
      merged=$(git branch --merged "origin/$base" 2>/dev/null | sed 's/^[* ]*//' | grep -v "^$base$" || true)
      if echo "$merged" | grep -q "^${current}$"; then
        git checkout "$base" 2>/dev/null && git pull origin "$base" 2>/dev/null && echo "  Switched to $base (branch was merged)."
      else
        git stash push -m "sync-repos-stash" 2>/dev/null || true
        git checkout "$base" 2>/dev/null && git pull origin "$base" 2>/dev/null || true
      fi
    elif [[ "$current" == "$base" ]]; then
      git pull origin "$base" 2>/dev/null || true
    fi
    [[ "$(git branch --show-current)" == "$base" ]] || true

    git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
    # Remove tracked .DS_Store
    while IFS= read -r f; do
      [[ -z "$f" ]] || git rm --cached "$f" 2>/dev/null || true
    done < <(git ls-files 2>/dev/null | grep '\.DS_Store$' || true)
    # Ensure .gitignore has .DS_Store
    if [[ -f .gitignore ]]; then
      grep -q '^\.DS_Store$' .gitignore || echo '.DS_Store' >> .gitignore
    else
      echo '.DS_Store' > .gitignore
    fi
    [[ -f .gitignore ]] && git add .gitignore 2>/dev/null
    [[ -f PR_DESCRIPTION.md ]] && git rm PR_DESCRIPTION.md 2>/dev/null || true
    [[ -f Chart.lock ]] && git rm Chart.lock 2>/dev/null || true
    [[ -d charts ]] && ls charts/*.tgz 1>/dev/null 2>&1 && git rm -rf charts/ 2>/dev/null || true
    # Stage only intended files (do not re-add cruft)
    git add .gitignore .github/ 2>/dev/null || true
    git reset HEAD Chart.lock charts/ PR_DESCRIPTION.md requirements.lock 2>/dev/null || true
    git status -s
    if ! git diff --staged --quiet 2>/dev/null; then
      git commit -m "chore: .DS_Store in .gitignore, remove cruft; consistent workflows"
    else
      echo "  No new changes to commit."
    fi
    # Push and create PR when we have commits to push (new or existing chore branch)
    if [[ -n "${GH_TOKEN:-}" ]]; then
      revs=$(git rev-list "origin/$BRANCH"..HEAD 2>/dev/null | wc -l)
      [[ -z "$revs" ]] && revs=0
      if [[ "$revs" -gt 0 ]] || ! git show-ref -q "refs/remotes/origin/$BRANCH" 2>/dev/null; then
        repo_slug=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null) || true
        if [[ -n "$repo_slug" ]]; then
          git push "https://x-access-token:${GH_TOKEN}@github.com/${repo_slug}.git" "$BRANCH" 2>/dev/null && echo "  Pushed." || { echo "  Push failed (token scope?)."; return 0; }
          gh pr create --base "$base" --head "$BRANCH" --title "chore: cruft and .DS_Store gitignore; workflow consistency" --body "Remove .DS_Store from tracking and ensure .gitignore. Remove PR_DESCRIPTION.md, Chart.lock, charts/*.tgz if present. Align GitHub Actions (release-notes permissions). All commits by repo owner." 2>/dev/null || echo "  PR may already exist."
        fi
      else
        echo "  Already up to date with origin/$BRANCH."
      fi
    else
      echo "  Run with GH_TOKEN (op run --env-file=homelab/.env.gh) to push and create PR."
    fi
  )
  echo ""
}

# All chart repos (own repo each)
for d in "$HELM"/atlantis "$HELM"/audiobookshelf "$HELM"/bazarr "$HELM"/longhorn "$HELM"/external-secrets "$HELM"/external-services "$HELM"/gaps "$HELM"/harbor "$HELM"/home-assistant "$HELM"/immich "$HELM"/ipmi-fan-control "$HELM"/kavita "$HELM"/komga "$HELM"/kubernetes-dashboard "$HELM"/minio "$HELM"/mylar "$HELM"/nextcloud "$HELM"/nvidia-device-plugin "$HELM"/oauth2-proxy "$HELM"/ombi "$HELM"/onepassword-secrets "$HELM"/organizr "$HELM"/plex-autoskip "$HELM"/plex-linker "$HELM"/plex "$HELM"/portainer "$HELM"/postgresql "$HELM"/qbittorrent "$HELM"/reloader "$HELM"/sabnzbd "$HELM"/tautulli "$HELM"/tunnel-interface; do
  [[ -d "$d" ]] && do_repo "$d"
done
for d in "$HELM"/core/argocd "$HELM"/core/cert-manager "$HELM"/core/external-dns "$HELM"/core/kubernetes-replicator "$HELM"/core/nginx "$HELM"/core/onepassword-connect "$HELM"/core/purelb; do
  [[ -d "$d" ]] && do_repo "$d"
done
echo "Done."
