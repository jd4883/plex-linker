#!/usr/bin/env bash
# Create the homelab-prometheus GitHub repo (if missing), push chart content from homelab/helm/prometheus, and open a PR.
# Argo CD config points to git@github.com:jd4883/homelab-prometheus.git with path "." — this script populates that repo.
#
# Run with 1Password so you get prompted for creds (no need to be logged in to gh):
#   From repo root: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-prometheus-chart-repo.sh
# homelab/.env.gh must contain: GH_TOKEN=op://Vault/Item/field
set -euo pipefail
HELM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HELM_DIR/../.." && pwd)"
REPO_OWNER="${GITHUB_OWNER:-jd4883}"
REPO_FULL="${REPO_OWNER}/homelab-prometheus"
BRANCH="${BRANCH:-feature/initial-helm-chart}"
CHART_SOURCE="$HELM_DIR/prometheus"

if [ -z "${GH_TOKEN:-}" ]; then
  echo "GH_TOKEN is not set. Run with: GH_HOST=github.com op run --env-file=homelab/.env.gh -- $0"
  exit 1
fi

if [ ! -d "$CHART_SOURCE" ] || [ ! -f "$CHART_SOURCE/Chart.yaml" ]; then
  echo "Chart not found at $CHART_SOURCE (expected homelab/helm/prometheus with Chart.yaml)."
  exit 1
fi

_gh_url() { echo "https://x-access-token:${GH_TOKEN}@github.com/${1}.git"; }

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

if ! gh repo view "$REPO_FULL" &>/dev/null; then
  echo "Creating repo $REPO_FULL..."
  gh repo create "$REPO_FULL" --public --description "Prometheus + Grafana (kube-prometheus-stack). HA; observability namespace; 1Password Grafana admin." --add-readme
fi

echo "Cloning $REPO_FULL..."
git clone "$(_gh_url "$REPO_FULL")" "$tmpdir"

(
  cd "$tmpdir"
  git config user.email "${REPO_OWNER}@users.noreply.github.com"
  git config user.name "${REPO_OWNER}"
  git fetch origin "$BRANCH" 2>/dev/null && git checkout -b "$BRANCH" "origin/$BRANCH" 2>/dev/null || git checkout -b "$BRANCH"
  rm -f README.md
  if command -v rsync &>/dev/null; then
    rsync -a --exclude='.git' --exclude='PR_DESCRIPTION*.md' --exclude='Chart.lock' "$CHART_SOURCE"/ .
  else
    tar cf - -C "$CHART_SOURCE" . | tar xf -
    rm -rf .git 2>/dev/null || true
    rm -f PR_DESCRIPTION.md PR_DESCRIPTION*.md Chart.lock 2>/dev/null || true
  fi
  git add -A
  if git diff --staged --quiet; then
    echo "No changes for prometheus chart."
    exit 0
  fi
  GIT_AUTHOR_EMAIL="${REPO_OWNER}@users.noreply.github.com" GIT_COMMITTER_EMAIL="${REPO_OWNER}@users.noreply.github.com" \
    git commit -m "feat: initial Prometheus/Grafana Helm chart (kube-prometheus-stack, HA, 1Password)"
  git push -u origin "$BRANCH"
  if gh pr view --repo "$REPO_FULL" --head "$BRANCH" &>/dev/null; then
    echo "PR already exists: https://github.com/$REPO_FULL/pulls"
  else
    gh pr create --base main --head "$BRANCH" --title "Initial Prometheus/Grafana Helm chart" --body "kube-prometheus-stack wrapper: HA (2 replicas), observability namespace, Longhorn HDD, Grafana admin from 1Password (externalSecrets.yaml), cert-manager TLS, nginx global auth."
    echo "PR: https://github.com/$REPO_FULL/pulls"
  fi
)

echo "Done. After merging the PR, Argo CD (observability project) will sync from $REPO_FULL with path \".\"."
