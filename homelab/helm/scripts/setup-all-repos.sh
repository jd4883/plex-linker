#!/usr/bin/env bash
# Master setup: gitignore consistency, repo descriptions, OPENAI_API_KEY secrets.
# Run from workspace root: GH_HOST=github.com op run --env-file=homelab/.env.gh -- bash homelab/helm/scripts/setup-all-repos.sh
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

echo "=== 1. Ensure .gitignore consistency ==="
bash "$SCRIPT_DIR/ensure-gitignore-consistency.sh"

echo ""
echo "=== 2. Set repo descriptions ==="
bash "$SCRIPT_DIR/../set-repo-descriptions.sh"

echo ""
echo "=== 3. Set OPENAI_API_KEY in repos with release-notes ==="
bash "$SCRIPT_DIR/set-openai-secrets-in-repos.sh"

echo ""
echo "Done. Next: commit workflow/gitignore changes and run sync-repos-cruft-and-prs.sh to push and open PRs."
