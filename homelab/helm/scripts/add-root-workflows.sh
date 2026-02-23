#!/usr/bin/env bash
# Add release-on-merge and release-notes workflows to root .github/workflows for charts
# tracked in the monorepo. Run from workspace root.
# Usage: bash homelab/helm/scripts/add-root-workflows.sh
set -e
REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
GITHUB="$REPO_ROOT/.github/workflows"
mkdir -p "$GITHUB"

# Charts tracked in monorepo (path, tag_prefix, helm_repos for lint)
charts=(
  "gotify:gotify-v:bjw-s,vquie"
  "mealie:mealie-v:bjw-s,vquie"
  "one-pace-plex-assistant:one-pace-plex-assistant-v:"
  "organizr-tab-controller:organizr-tab-controller-v:bjw-s,vquie"
  "paperless-ngx:paperless-ngx-v:bjw-s,vquie"
  "plex-prefer-non-forced-subs:plex-prefer-non-forced-subs-v:"
  "postgresql-backup-to-minio:postgresql-backup-to-minio-v:bjw-s,vquie"
  "prometheus:prometheus-v:bjw-s,vquie"
  "tautulli:tautulli-v:bjw-s,vquie"
)

for chart_spec in "${charts[@]}"; do
  chart="${chart_spec%%:*}"
  rest="${chart_spec#*:}"
  tag_prefix="${rest%%:*}"
  helm_repos="${rest#*:}"
  path="homelab/helm/$chart"
  wf_name="Release $chart chart on merge to main"

  # Skip if already exists (unpackerr is manual)
  [[ -f "$GITHUB/release-on-merge-$chart.yml" ]] && continue

  helm_repos_cmd=""
  if [[ -n "$helm_repos" ]]; then
    for hr in ${helm_repos//,/ }; do
      case "$hr" in
        bjw-s) helm_repos_cmd+="helm repo add bjw-s https://bjw-s-labs.github.io/helm-charts
          " ;;
        vquie) helm_repos_cmd+="helm repo add vquie https://vquie.github.io/helm-charts
          " ;;
      esac
    done
  fi

  cat > "$GITHUB/release-on-merge-$chart.yml" << EOF
# Auto-release $chart chart on merge to main. Chart at $path.

name: $wf_name

on:
  push:
    branches: [main]
    paths:
      - '$path/**'

concurrency: release-$chart

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Helm
        uses: azure/setup-helm@v4
        with:
          version: "v3.14.0"
      - name: Lint chart
        run: |
          cd $path
          $helm_repos_cmd
          helm dependency update .
          helm lint .

  release:
    runs-on: ubuntu-latest
    needs: lint
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Release on merge (create tag and release)
        uses: expectedbehaviors/github-actions/.github/actions/release-on-merge@main
        with:
          github_token: \${{ secrets.GITHUB_TOKEN }}
          tag_prefix: "$tag_prefix"
EOF

  cat > "$GITHUB/release-notes-$chart.yml" << EOF
# Release notes (OpenAI) for $chart. Requires OPENAI_API_KEY.

name: Release notes ($chart)

on:
  release:
    types: [published]
  workflow_run:
    workflows: ["$wf_name"]
    types: [completed]
    branches: [main]
  workflow_dispatch:
    inputs:
      release_tag:
        description: 'Release tag (e.g. ${tag_prefix}1.0.0). Default: latest.'
        required: false

jobs:
  update-release-notes:
    runs-on: ubuntu-latest
    if: |
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'release' && startsWith(github.event.release.tag_name, '$tag_prefix')) ||
      (github.event_name == 'workflow_run' && github.event.workflow_run.conclusion == 'success')
    permissions:
      contents: write
      pull-requests: read
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Resolve release tag ($tag_prefix*)
        id: tag
        env:
          GH_TOKEN: \${{ secrets.GITHUB_TOKEN }}
        run: |
          if [ "\${{ github.event_name }}" = "release" ]; then
            echo "tag=\${{ github.event.release.tag_name }}" >> \$GITHUB_OUTPUT
          elif [ -n "\${{ github.event.inputs.release_tag }}" ]; then
            echo "tag=\${{ github.event.inputs.release_tag }}" >> \$GITHUB_OUTPUT
          else
            TAG=\$(gh api "repos/\${{ github.repository }}/releases?per_page=20" -q '[.[] | select(.tag_name | startswith("$tag_prefix")) | .tag_name][0]')
            [ -z "\$TAG" ] || [ "\$TAG" = "null" ] && exit 1
            echo "tag=\$TAG" >> \$GITHUB_OUTPUT
          fi
        shell: bash
      - name: Update release notes from PR (OpenAI)
        uses: expectedbehaviors/github-actions/.github/actions/release-notes@main
        with:
          openai_api_key: \${{ secrets.OPENAI_API_KEY }}
          github_token: \${{ secrets.GITHUB_TOKEN }}
          release_tag: \${{ steps.tag.outputs.tag }}
EOF

  echo "Added root workflows for $chart"
done

# Submodules: atlantis, oauth2-proxy, plex
for sub in atlantis oauth2-proxy plex; do
  path="homelab/helm/$sub"
  [[ -f "$GITHUB/release-on-merge-$sub.yml" ]] && continue
  # Submodule workflows - path is just the submodule dir
  echo "Skipping $sub (submodule - add manually if needed)"
done

echo "Done."
