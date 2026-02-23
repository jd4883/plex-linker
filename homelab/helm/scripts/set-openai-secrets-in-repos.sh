#!/usr/bin/env bash
# Set OPENAI_API_KEY secret in all repos that have release-notes workflows.
# Uses 1Password CLI to inject the key; gh secret set to set it per repo.
# Run: GH_HOST=github.com op run --env-file=homelab/.env.gh -- bash homelab/helm/scripts/set-openai-secrets-in-repos.sh
set -e
: "${OPENAI_API_KEY:?OPENAI_API_KEY required. Run with: op run --env-file=homelab/.env.gh -- $0}"
: "${GH_TOKEN:?GH_TOKEN required. Run with: op run --env-file=homelab/.env.gh -- $0}"

GH=${GH:-gh}

# Repos that have release-notes workflows (use OPENAI_API_KEY)
REPOS_WITH_RELEASE_NOTES=(
  "jd4883/homelab-atlantis"
  "jd4883/tanzu-bazarr"
  "jd4883/harbor"
  "jd4883/homelab-immich"
  "jd4883/longhorn"
  "jd4883/homelab-nextcloud"
  "jd4883/homelab-k8s-dashboard"
  "jd4883/postgresql"
  "jd4883/prometheus"
  "jd4883/redis"
  "jd4883/tanzu-plex-linker"
  "jd4883/homelab-unpackerr"
  "jd4883/homelab-mealie"
  "jd4883/homelab-paperless-ngx"
  "jd4883/homelab-gotify"
  "jd4883/homelab-postgresql-backup-to-minio"
  "jd4883/homelab-cert-manager"
  "jd4883/homelab-external-dns"
  "jd4883/homelab-kubernetes-replicator"
  "jd4883/homelab-nginx"
  "jd4883/homelab-onepassword-connect"
  "jd4883/homelab-purelb"
  "jd4883/homelab-audiobookshelf"
  "jd4883/homelab-external-secrets"
  "jd4883/homelab-external-services"
  "jd4883/homelab-gaps"
  "jd4883/homelab-home-assistant"
  "jd4883/homelab-ipmi-fan-control"
  "jd4883/homelab-kavita"
  "jd4883/homelab-komga"
  "jd4883/homelab-minio"
  "jd4883/homelab-mylar"
  "jd4883/homelab-ombi"
  "jd4883/homelab-organizr"
  "jd4883/homelab-portainer"
  "jd4883/homelab-qbittorrent"
  "jd4883/homelab-reloader"
  "jd4883/homelab-sabnzbd"
  "jd4883/homelab-tautulli"
  "jd4883/homelab-tunnel-interface"
  "jd4883/nvidia-k8s-device-plugin"
  "jd4883/onepassword-secrets"
  "jd4883/tanzu-oauth2-proxy"
  "jd4883/tanzu-plex"
  "jd4883/homelab-organizr-tab-controller"
  "jd4883/one-pace-plex-assistant-helm-chart"
  "jd4883/plex-prefer-non-forced-subs-helm-chart"
  "jd4883/tanzu-lidarr"
  "jd4883/tanzu-prowlarr"
  "jd4883/tanzu-radarr"
  "jd4883/tanzu-readarr"
  "jd4883/tanzu-sonarr"
)

# Optional: expectedbehaviors/plex-autoskip-helm-chart (different org; skip if no access)
for repo in "${REPOS_WITH_RELEASE_NOTES[@]}"; do
  echo "Setting OPENAI_API_KEY for $repo..."
  echo -n "$OPENAI_API_KEY" | $GH secret set OPENAI_API_KEY --repo "$repo" || echo "  (failed)"
done
echo "Done."
