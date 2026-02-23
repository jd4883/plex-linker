#!/usr/bin/env bash
# Remove cruft (Chart.lock, requirements.lock, charts/*.tgz, PR_DESCRIPTION*.md) from tracking
# and ensure .gitignore. Run from workspace root. Does NOT create PRs.
# Usage: bash homelab/helm/scripts/remove-cruft-local.sh
set -euo pipefail
HELM="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$HELM/../.." && pwd)"
GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-Jacob Dresdale}"
GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-jd4883@users.noreply.github.com}"
export GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME" GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"

do_repo() {
  local dir="$1"
  local rel="${dir#$REPO_ROOT/}"
  [[ -e "$dir/.git" ]] || return 0
  (cd "$dir" && git rev-parse --show-toplevel 2>/dev/null) | grep -q . || return 0
  [[ "$(cd "$dir" && pwd)" == "$(cd "$dir" && git rev-parse --show-toplevel)" ]] || return 0

  (
    cd "$dir"
    git config user.name "$GIT_AUTHOR_NAME" 2>/dev/null || true
    git config user.email "$GIT_AUTHOR_EMAIL" 2>/dev/null || true
    changed=0
    # Remove from tracking
    for f in Chart.lock requirements.lock; do
      [[ -f "$f" ]] && git ls-files --error-unmatch "$f" 2>/dev/null && { git rm --cached "$f" 2>/dev/null; changed=1; } || true
    done
    # helm/ subdir
    [[ -f helm/Chart.lock ]] && git ls-files --error-unmatch helm/Chart.lock 2>/dev/null && { git rm --cached helm/Chart.lock 2>/dev/null; changed=1; } || true
    [[ -f helm/requirements.lock ]] && git ls-files --error-unmatch helm/requirements.lock 2>/dev/null && { git rm --cached helm/requirements.lock 2>/dev/null; changed=1; } || true
    # charts/*.tgz only (not charts/ with subchart dirs like cert-manager/charts/cert-manager/)
    if [[ -d charts ]]; then
      for tgz in charts/*.tgz; do
        [[ -f "$tgz" ]] && git ls-files --error-unmatch "$tgz" 2>/dev/null && { git rm --cached "$tgz" 2>/dev/null; changed=1; } || true
      done
    fi
    if [[ -d helm/charts ]]; then
      for tgz in helm/charts/*.tgz; do
        [[ -f "$tgz" ]] && git ls-files --error-unmatch "$tgz" 2>/dev/null && { git rm --cached "$tgz" 2>/dev/null; changed=1; } || true
      done
    fi
    # redis/operator/charts/*.tgz, postgresql/*/charts/*.tgz (helm dep output)
    for sub in redis/operator/charts postgresql/operator/charts postgresql/cluster/charts; do
      if [[ -d "$sub" ]]; then
        for tgz in "$sub"/*.tgz; do
          [[ -f "$tgz" ]] && git ls-files --error-unmatch "$tgz" 2>/dev/null && { git rm --cached "$tgz" 2>/dev/null; changed=1; } || true
        done
      fi
    done
    # PR_DESCRIPTION
    for f in PR_DESCRIPTION.md PR_DESCRIPTION*.md; do
      [[ -f "$f" ]] && git ls-files --error-unmatch "$f" 2>/dev/null && { git rm --cached "$f" 2>/dev/null; changed=1; } || true
    done
    # Ensure .gitignore (no duplicates)
    [[ -f .gitignore ]] || touch .gitignore
    for entry in ".DS_Store" "charts/" "Chart.lock" "PR_DESCRIPTION*.md" "requirements.lock"; do
      grep -qF "$entry" .gitignore 2>/dev/null || echo "$entry" >> .gitignore
    done
    # helm/ subdir charts
    [[ -d helm ]] && { grep -qF "helm/charts/" .gitignore 2>/dev/null || echo "helm/charts/" >> .gitignore; grep -qF "helm/Chart.lock" .gitignore 2>/dev/null || echo "helm/Chart.lock" >> .gitignore; grep -qF "helm/requirements.lock" .gitignore 2>/dev/null || echo "helm/requirements.lock" >> .gitignore; } || true
    [[ -f .gitignore ]] && git add .gitignore 2>/dev/null
    if [[ $changed -eq 1 ]] || ! git diff --staged --quiet 2>/dev/null; then
      git add .gitignore 2>/dev/null
      git status -s
      git commit -m "chore: remove cruft (Chart.lock, requirements.lock, charts/*.tgz, PR_DESCRIPTION); ensure .gitignore" 2>/dev/null && echo "  $rel: committed cruft removal" || echo "  $rel: no changes"
    else
      echo "  $rel: clean"
    fi
  )
}

echo "=== Removing cruft from chart repos ==="
for d in "$HELM"/atlantis "$HELM"/audiobookshelf "$HELM"/bazarr "$HELM"/longhorn "$HELM"/external-secrets "$HELM"/external-services "$HELM"/gaps "$HELM"/harbor "$HELM"/home-assistant "$HELM"/immich "$HELM"/ipmi-fan-control "$HELM"/kavita "$HELM"/komga "$HELM"/kubernetes-dashboard "$HELM"/minio "$HELM"/mylar "$HELM"/nextcloud "$HELM"/nvidia-device-plugin "$HELM"/oauth2-proxy "$HELM"/ombi "$HELM"/onepassword-secrets "$HELM"/organizr "$HELM"/plex-autoskip "$HELM"/plex-linker "$HELM"/plex "$HELM"/portainer "$HELM"/postgresql "$HELM"/qbittorrent "$HELM"/reloader "$HELM"/sabnzbd "$HELM"/tautulli "$HELM"/tunnel-interface "$HELM"/gotify "$HELM"/mealie "$HELM"/paperless-ngx "$HELM"/prometheus "$HELM"/unpackerr "$HELM"/one-pace-plex-assistant "$HELM"/organizr-tab-controller "$HELM"/plex-prefer-non-forced-subs "$HELM"/postgresql-backup-to-minio "$HELM"/lidarr "$HELM"/prowlarr "$HELM"/radarr "$HELM"/readarr "$HELM"/sonarr; do
  [[ -d "$d" ]] && do_repo "$d"
done
for d in "$HELM"/core/argocd "$HELM"/core/cert-manager "$HELM"/core/external-dns "$HELM"/core/kubernetes-replicator "$HELM"/core/nginx "$HELM"/core/onepassword-connect "$HELM"/core/purelb; do
  [[ -d "$d" ]] && do_repo "$d"
done
echo "Done."
