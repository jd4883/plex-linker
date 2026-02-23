#!/usr/bin/env bash
# Add workflow files to chart repos using GitHub Contents API (no git push / workflow scope needed for API).
# Usage: GH_HOST=github.com op run --env-file=homelab/.env.gh -- bash ./homelab/helm/scripts/push-workflows-via-api.sh
set -e
HELM_DIR="${HELM_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
REPO_ROOT="${REPO_ROOT:-$(cd "$HELM_DIR/../.." && pwd)}"
[ -z "${GH_TOKEN}" ] && echo "GH_TOKEN required" && exit 1

# repo:chart (chart = dir under helm/)
REPOS=(
  "jd4883/homelab-unpackerr:unpackerr"
  "jd4883/homelab-prometheus:prometheus"
  "jd4883/homelab-mealie:mealie"
  "jd4883/homelab-paperless-ngx:paperless-ngx"
  "jd4883/homelab-gotify:gotify"
  "jd4883/homelab-postgresql-backup-to-minio:postgresql-backup-to-minio"
)

for entry in "${REPOS[@]}"; do
  repo="${entry%%:*}"
  chart="${entry##*:}"
  src="$REPO_ROOT/homelab/helm/$chart/.github/workflows"
  [ ! -d "$src" ] && echo "Skip $repo: no $src" && continue
  echo "=== $repo ==="
  default_branch=$(gh api "repos/$repo" -q .default_branch 2>/dev/null) || default_branch=main
  for f in "$src"/*.yml; do
    [ -f "$f" ] || continue
    name=$(basename "$f")
    path=".github/workflows/$name"
    content=$(base64 < "$f" | tr -d '\n')
    sha=$(gh api "repos/$repo/contents/$path" -q .sha 2>/dev/null || true)
    if [ -n "$sha" ]; then
      echo "  Update $name"
      gh api -X PUT "repos/$repo/contents/$path" -f message="chore: add/update $name" -f content="$content" -f branch="$default_branch" -f sha="$sha" >/dev/null
    else
      echo "  Create $name"
      gh api -X PUT "repos/$repo/contents/$path" -f message="chore: add $name" -f content="$content" -f branch="$default_branch" >/dev/null
    fi
  done
done
echo "Done."
