#!/usr/bin/env bash
# Switch to main and pull when current branch is merged. No PR creation.
# Run from workspace root: bash homelab/helm/scripts/update-when-merged.sh
set -euo pipefail
HELM="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$HELM/../.." && pwd)"

do_repo() {
  local dir="$1"
  local rel="${dir#$REPO_ROOT/}"
  [[ -e "$dir/.git" ]] || return 0
  (cd "$dir" && git rev-parse --show-toplevel 2>/dev/null) | grep -q . || return 0
  [[ "$(cd "$dir" && pwd)" == "$(cd "$dir" && git rev-parse --show-toplevel)" ]] || return 0

  (
    cd "$dir"
    git fetch origin 2>/dev/null || true
    base=main
    for b in main master; do
      git show-ref -q "refs/remotes/origin/$b" 2>/dev/null && { base="$b"; break; }
    done
    current=$(git branch --show-current 2>/dev/null)
    if [[ -n "$current" ]] && [[ "$current" != "$base" ]]; then
      merged=$(git branch --merged "origin/$base" 2>/dev/null | sed 's/^[* ]*//' | grep -v "^$base$" || true)
      if echo "$merged" | grep -q "^${current}$"; then
        git checkout "$base" 2>/dev/null && git pull origin "$base" 2>/dev/null && echo "  $rel: switched to $base (was merged)"
      else
        echo "  $rel: on $current (not merged)"
      fi
    elif [[ "$current" == "$base" ]]; then
      git pull origin "$base" 2>/dev/null && echo "  $rel: pulled $base"
    fi
  )
}

echo "=== Updating repos when branch is merged ==="
for d in "$HELM"/atlantis "$HELM"/audiobookshelf "$HELM"/bazarr "$HELM"/longhorn "$HELM"/external-secrets "$HELM"/external-services "$HELM"/gaps "$HELM"/harbor "$HELM"/home-assistant "$HELM"/immich "$HELM"/ipmi-fan-control "$HELM"/kavita "$HELM"/komga "$HELM"/kubernetes-dashboard "$HELM"/minio "$HELM"/mylar "$HELM"/nextcloud "$HELM"/nvidia-device-plugin "$HELM"/oauth2-proxy "$HELM"/ombi "$HELM"/onepassword-secrets "$HELM"/organizr "$HELM"/plex-autoskip "$HELM"/plex-linker "$HELM"/plex "$HELM"/portainer "$HELM"/postgresql "$HELM"/qbittorrent "$HELM"/reloader "$HELM"/sabnzbd "$HELM"/tautulli "$HELM"/tunnel-interface "$HELM"/gotify "$HELM"/mealie "$HELM"/paperless-ngx "$HELM"/prometheus "$HELM"/unpackerr "$HELM"/one-pace-plex-assistant "$HELM"/organizr-tab-controller "$HELM"/plex-prefer-non-forced-subs "$HELM"/postgresql-backup-to-minio "$HELM"/lidarr "$HELM"/prowlarr "$HELM"/radarr "$HELM"/readarr "$HELM"/sonarr; do
  [[ -d "$d" ]] && do_repo "$d"
done
for d in "$HELM"/core/argocd "$HELM"/core/cert-manager "$HELM"/core/external-dns "$HELM"/core/kubernetes-replicator "$HELM"/core/nginx "$HELM"/core/onepassword-connect "$HELM"/core/purelb; do
  [[ -d "$d" ]] && do_repo "$d"
done
do_repo "$REPO_ROOT"
echo "Done."
