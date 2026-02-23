#!/usr/bin/env bash
# In each chart repo (and personal_projects/docker) under the workspace: create chore PR to remove
# .DS_Store from tracking, ensure .gitignore has .DS_Store, and remove other cruft. All commits use
# author Jacob Dresdale so you remain the sole contributor (no Cursor/bot).
# Run from workspace root: GH_HOST=github.com op run --env-file=homelab/.env.gh -- bash homelab/helm/scripts/chore-cruft-dsstore-prs.sh
# Requires: GH_TOKEN with repo (and workflow if pushing workflow dirs).
set -euo pipefail
export GH_HOST=github.com
HELM="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$HELM/../.." && pwd)"
BRANCH="${BRANCH:-chore/remove-cruft-dsstore}"
GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-Jacob Dresdale}"
GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-jd4883@users.noreply.github.com}"
export GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME" GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"

[ -n "${GH_TOKEN:-}" ] || { echo "GH_TOKEN required. Run with: op run --env-file=homelab/.env.gh -- $0"; exit 1; }

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
    default_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    for b in main master; do
      git show-ref -q "refs/remotes/origin/$b" 2>/dev/null && { default_branch="$b"; break; }
    done
    git checkout "$default_branch" 2>/dev/null || return 0
    git pull origin "$default_branch" 2>/dev/null || true
    git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"

    to_remove=""
    # .DS_Store
    while IFS= read -r f; do
      [[ -z "$f" ]] || { git rm --cached "$f" 2>/dev/null && to_remove="${to_remove} .DS_Store"; }
    done < <(git ls-files 2>/dev/null | grep '\.DS_Store$' || true)
    if [[ -f .gitignore ]]; then
      grep -q '^\.DS_Store$' .gitignore || { echo '.DS_Store' >> .gitignore; to_remove="${to_remove} .gitignore"; }
    else
      echo '.DS_Store' > .gitignore
      to_remove="${to_remove} .gitignore"
    fi
    [[ -f .gitignore ]] && git add .gitignore 2>/dev/null

    # Other cruft
    [[ -f PR_DESCRIPTION.md ]] && git rm PR_DESCRIPTION.md 2>/dev/null && to_remove="${to_remove} PR_DESCRIPTION.md"
    [[ -f Chart.lock ]] && git rm Chart.lock 2>/dev/null && to_remove="${to_remove} Chart.lock"
    [[ -d charts ]] && ls charts/*.tgz 1>/dev/null 2>&1 && git rm -rf charts/ 2>/dev/null && to_remove="${to_remove} charts/"

    git add -A 2>/dev/null
    git diff --staged --quiet && { echo "  No cruft to remove."; return 0; }
    git commit -m "chore: remove cruft (.DS_Store, ensure .gitignore); PR_DESCRIPTION/Chart.lock/charts if present"
    repo_slug=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null) || true
    if [[ -n "$repo_slug" ]]; then
      git push "https://x-access-token:${GH_TOKEN}@github.com/${repo_slug}.git" "$BRANCH" 2>/dev/null || { echo "  Push failed (token scope?)."; return 0; }
      gh pr create --base "$default_branch" --head "$BRANCH" --title "chore: remove cruft and add .DS_Store to .gitignore" --body "Remove .DS_Store from tracking and ensure .gitignore contains .DS_Store. Remove PR_DESCRIPTION.md, Chart.lock, charts/*.tgz if present. All commits by repo owner (no bot)." 2>/dev/null || echo "  PR may already exist."
    else
      echo "  Push manually and create PR."
    fi
  )
  echo ""
}

# homelab/helm chart repos (own repo each)
for d in "$HELM"/atlantis "$HELM"/audiobookshelf "$HELM"/bazarr "$HELM"/longhorn "$HELM"/external-secrets "$HELM"/external-services "$HELM"/gaps "$HELM"/harbor "$HELM"/home-assistant "$HELM"/immich "$HELM"/ipmi-fan-control "$HELM"/kavita "$HELM"/komga "$HELM"/kubernetes-dashboard "$HELM"/minio "$HELM"/mylar "$HELM"/nextcloud "$HELM"/nvidia-device-plugin "$HELM"/oauth2-proxy "$HELM"/ombi "$HELM"/onepassword-secrets "$HELM"/organizr "$HELM"/plex-autoskip "$HELM"/plex-linker "$HELM"/plex "$HELM"/portainer "$HELM"/postgresql "$HELM"/qbittorrent "$HELM"/reloader "$HELM"/sabnzbd "$HELM"/tautulli "$HELM"/tunnel-interface; do
  [[ -d "$d" ]] && do_repo "$d"
done
for d in "$HELM"/core/argocd "$HELM"/core/cert-manager "$HELM"/core/external-dns "$HELM"/core/kubernetes-replicator "$HELM"/core/nginx "$HELM"/core/onepassword-connect "$HELM"/core/purelb; do
  [[ -d "$d" ]] && do_repo "$d"
done
# personal_projects/docker (if they are separate repos; plex-linker root may be the workspace)
for d in "$REPO_ROOT/personal_projects/docker/ptp-freeleech"; do
  [[ -d "$d" ]] && [[ -e "$d/.git" ]] && do_repo "$d"
done
echo "Done."
