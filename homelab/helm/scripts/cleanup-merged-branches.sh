#!/usr/bin/env bash
# In each chart repo (and personal_projects/docker) under the workspace: list branches merged into main,
# then optionally delete them locally and on remote. Run from workspace root.
# Usage:
#   bash homelab/helm/scripts/cleanup-merged-branches.sh           # list only
#   DELETE=1 bash homelab/helm/scripts/cleanup-merged-branches.sh # delete local + remote
set -euo pipefail
HELM="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$HELM/../.." && pwd)"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"

do_repo() {
  local dir="$1"
  [[ -e "$dir/.git" ]] || return 0
  (cd "$dir" && git rev-parse --show-toplevel 2>/dev/null) | grep -q . || return 0
  local rel="${dir#$REPO_ROOT/}"
  echo "=== $rel ==="
  (
    cd "$dir"
    git fetch origin 2>/dev/null || true
    base=main
    for b in main master; do
      git show-ref -q "refs/remotes/origin/$b" 2>/dev/null && { base="$b"; break; }
    done
    merged=$(git branch --merged "origin/$base" 2>/dev/null | sed 's/^[* ]*//' | grep -v "^$base$" || true)
    if [ -z "$merged" ]; then
      echo "  No merged branches to clean."
      return 0
    fi
    echo "$merged" | while read -r br; do
      [ -z "$br" ] || echo "  merged: $br"
    done
    if [ "${DELETE:-0}" = "1" ]; then
      echo "$merged" | while read -r br; do
        [ -z "$br" ] || { git branch -d "$br" 2>/dev/null || true; git push origin --delete "$br" 2>/dev/null || true; }
      done
    fi
  )
  echo ""
}

for d in "$HELM"/atlantis "$HELM"/audiobookshelf "$HELM"/bazarr "$HELM"/longhorn "$HELM"/external-secrets "$HELM"/external-services "$HELM"/gaps "$HELM"/harbor "$HELM"/home-assistant "$HELM"/immich "$HELM"/plex "$HELM"/portainer "$HELM"/postgresql "$HELM"/sabnzbd "$HELM"/core/argocd "$HELM"/core/cert-manager; do
  [[ -d "$d" ]] && do_repo "$d"
done
# Repo root if it's plex-linker
(cd "$REPO_ROOT" && git rev-parse --show-toplevel 2>/dev/null) | grep -q . && do_repo "$REPO_ROOT"
echo "Done. To delete merged branches run: DELETE=1 $0"
