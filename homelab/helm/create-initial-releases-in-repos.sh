#!/usr/bin/env bash
# Create initial GitHub releases **in each chart repo** (not in the workspace repo).
# Run from repo root with: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-initial-releases-in-repos.sh [--dry-run]
set -euo pipefail
REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$REPO_ROOT"
DRY_RUN=false
[[ "${1:-}" = "--dry-run" ]] && DRY_RUN=true

# repo_full | tag_prefix | path to Chart.yaml (from repo root)
CHARTS=(
  "jd4883/homelab-unpackerr|unpackerr-v|homelab/helm/unpackerr/Chart.yaml"
  "jd4883/homelab-prometheus|prometheus-v|homelab/helm/prometheus/Chart.yaml"
  "jd4883/homelab-mealie|mealie-v|homelab/helm/mealie/Chart.yaml"
  "jd4883/homelab-paperless-ngx|paperless-ngx-v|homelab/helm/paperless-ngx/Chart.yaml"
  "jd4883/homelab-gotify|gotify-v|homelab/helm/gotify/Chart.yaml"
  "jd4883/homelab-postgresql-backup-to-minio|postgresql-backup-to-minio-v|homelab/helm/postgresql-backup-to-minio/Chart.yaml"
)

get_version_from_chart() {
  local chart_path="$1"
  [[ ! -f "$chart_path" ]] && echo "" && return
  awk '/^version:/ { gsub(/^[ \t"]+|[ \t"]+$/, "", $2); gsub(/^v/, "", $2); print $2 }' "$chart_path"
}

get_description_from_chart() {
  local chart_path="$1"
  [[ ! -f "$chart_path" ]] && echo "Helm chart release." && return
  local d
  d=$(awk '/^description:/ { $1=""; gsub(/^[ \t"]+|[ \t"]+$/,""); print; exit }' "$chart_path")
  [[ -n "${d:-}" ]] && echo "$d" || echo "Helm chart release."
}

for entry in "${CHARTS[@]}"; do
  IFS='|' read -r repo_full tag_prefix chart_path <<< "$entry"
  if [[ ! -f "$chart_path" ]]; then
    echo "[SKIP] $repo_full: Chart not found at $chart_path"
    continue
  fi
  version=$(get_version_from_chart "$chart_path")
  if [[ -z "$version" ]]; then
    echo "[SKIP] $repo_full: No version in $chart_path"
    continue
  fi
  # Normalize: ensure tag has 'v' before version (tag_prefix may already end with v)
  if [[ "$tag_prefix" == *-v ]]; then
    tag="${tag_prefix}${version}"
  else
    tag="${tag_prefix}v${version}"
  fi
  if gh release view "$tag" --repo "$repo_full" &>/dev/null; then
    echo "[OK] $repo_full $tag — release exists"
    continue
  fi
  notes=$(get_description_from_chart "$chart_path")
  notes="## $tag

$notes

*Initial release. Future releases will be created automatically on merge to main (see repo workflows).*"
  echo "[CREATE] $repo_full $tag"
  if [[ "$DRY_RUN" = true ]]; then
    echo "  (dry-run) would: gh release create $tag --repo $repo_full --notes \"...\" --latest"
    continue
  fi
  gh release create "$tag" --repo "$repo_full" --notes "$notes" --latest
  echo "  Created."
done
echo "Done."
