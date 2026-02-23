#!/usr/bin/env bash
# Ensure .gitignore has standard entries: .DS_Store, charts/, Chart.lock, PR_DESCRIPTION*.md
# For charts with helm/ subdir: helm/charts/, helm/Chart.lock
# Run from workspace root: bash homelab/helm/scripts/ensure-gitignore-consistency.sh
set -e
HELM="$(cd "$(dirname "$0")/.." && pwd)"

ensure_entries() {
  local dir="$1"
  local has_helm="$2"
  local gi="$dir/.gitignore"
  mkdir -p "$dir"
  [[ -f "$gi" ]] || touch "$gi"
  local entries=(".DS_Store" "charts/" "Chart.lock" "PR_DESCRIPTION*.md")
  if [[ "$has_helm" == "1" ]]; then
    entries+=("helm/charts/" "helm/Chart.lock")
  fi
  for entry in "${entries[@]}"; do
    grep -qF "$entry" "$gi" 2>/dev/null || echo "$entry" >> "$gi"
  done
}

# Flat charts
for d in "$HELM"/atlantis "$HELM"/audiobookshelf "$HELM"/bazarr "$HELM"/longhorn "$HELM"/external-secrets \
  "$HELM"/external-services "$HELM"/gaps "$HELM"/harbor "$HELM"/home-assistant "$HELM"/immich \
  "$HELM"/ipmi-fan-control "$HELM"/kavita "$HELM"/komga "$HELM"/kubernetes-dashboard "$HELM"/minio \
  "$HELM"/mylar "$HELM"/nextcloud "$HELM"/nvidia-device-plugin "$HELM"/oauth2-proxy "$HELM"/ombi \
  "$HELM"/onepassword-secrets "$HELM"/organizr "$HELM"/plex-autoskip "$HELM"/plex-linker "$HELM"/plex \
  "$HELM"/portainer "$HELM"/postgresql "$HELM"/qbittorrent "$HELM"/reloader "$HELM"/sabnzbd \
  "$HELM"/tautulli "$HELM"/tunnel-interface "$HELM"/unpackerr "$HELM"/prometheus "$HELM"/mealie \
  "$HELM"/paperless-ngx "$HELM"/gotify "$HELM"/postgresql-backup-to-minio; do
  [[ -d "$d" ]] || continue
  has_helm=0
  [[ -d "$d/helm" ]] && has_helm=1
  ensure_entries "$d" "$has_helm"
  echo "  $d"
done

# Core submodules
for d in "$HELM"/core/argocd "$HELM"/core/cert-manager "$HELM"/core/external-dns \
  "$HELM"/core/kubernetes-replicator "$HELM"/core/nginx "$HELM"/core/onepassword-connect "$HELM"/core/purelb; do
  [[ -d "$d" ]] || continue
  ensure_entries "$d" 0
  echo "  $d"
done

echo "Done."
