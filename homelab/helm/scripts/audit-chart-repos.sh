#!/usr/bin/env bash
# Audit chart repos for: (1) missing workflows, (2) unwanted files (Chart.lock, charts/*.tgz, PR_DESCRIPTION.md),
# (3) merged branches to clean. Uses gh api when GH_TOKEN set; for local clone (longhorn) runs git commands.
# Usage: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/scripts/audit-chart-repos.sh

set -e
HELM_DIR="${HELM_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
REPO_ROOT="${REPO_ROOT:-$(cd "$HELM_DIR/../.." && pwd)}"

REPOS=(
  "jd4883/homelab-unpackerr"
  "jd4883/homelab-prometheus"
  "jd4883/homelab-mealie"
  "jd4883/homelab-paperless-ngx"
  "jd4883/homelab-gotify"
  "jd4883/homelab-postgresql-backup-to-minio"
  "jd4883/longhorn"
  "jd4883/harbor"
  "jd4883/homelab-immich"
  "jd4883/homelab-nextcloud"
)

echo "=== 1. Workflows present? ==="
for repo in "${REPOS[@]}"; do
  count=$(gh api "repos/$repo/contents/.github/workflows" 2>/dev/null | jq -r 'if type == "array" then length else 0 end' 2>/dev/null || echo "0")
  [ "$count" = "0" ] && echo "  $repo: no workflows" || echo "  $repo: $count workflow(s)"
done

echo ""
echo "=== 2. Unwanted files (Chart.lock, charts/*.tgz, PR_DESCRIPTION.md) ==="
for repo in "${REPOS[@]}"; do
  cruft=""
  gh api "repos/$repo/contents/Chart.lock" -q .name 2>/dev/null | grep -q . && cruft="${cruft} Chart.lock" || true
  gh api "repos/$repo/contents/charts" -q .name 2>/dev/null | grep -q . && cruft="${cruft} charts/" || true
  gh api "repos/$repo/contents/PR_DESCRIPTION.md" -q .name 2>/dev/null | grep -q . && cruft="${cruft} PR_DESCRIPTION.md" || true
  [ -n "$cruft" ] && echo "  $repo:$cruft" || echo "  $repo: none"
done

echo ""
echo "=== 3. Merged branches (local longhorn clone) ==="
LONGHORN="$REPO_ROOT/homelab/helm/longhorn"
if [ -d "$LONGHORN/.git" ]; then
  cd "$LONGHORN"
  git fetch origin 2>/dev/null || true
  default=$(git remote show origin 2>/dev/null | awk '/HEAD branch/ { print $3 }') || default=main
  for b in $(git branch | sed 's/^[* ]*//'); do
    [ "$b" = "$default" ] && continue
    if git branch --merged "origin/$default" 2>/dev/null | grep -q "^  $b$"; then
      echo "  longhorn: branch '$b' is merged into $default (safe to delete)"
    fi
  done
  cd - >/dev/null
else
  echo "  (no local longhorn clone at $LONGHORN)"
fi

echo ""
echo "Done. To clean merged branches in longhorn: git branch -d <branch> && git push origin --delete <branch>"
