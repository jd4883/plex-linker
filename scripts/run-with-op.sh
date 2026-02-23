#!/usr/bin/env bash
# Run from repo root to push and create PR. 1Password will prompt in this terminal.
#   ./scripts/run-with-op.sh
# Or with env file: GH_HOST=github.com op run --env-file=/path/to/.env.gh -- bash scripts/push-and-pr.sh
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
ENV_GH="${PLEX_LINKER_GH_ENV:-homelab/.env.gh}"
if [[ -f "$ENV_GH" ]]; then
  exec env GH_HOST=github.com op run --env-file="$ENV_GH" -- bash "$ROOT/scripts/push-and-pr.sh"
fi
echo "GH_TOKEN not set and $ENV_GH not found. Run: GH_HOST=github.com op run --env-file=<path-to-env.gh> -- bash scripts/push-and-pr.sh"
exit 1
