#!/usr/bin/env bash
# Add release-on-merge and release-notes workflows to a chart directory in the workspace.
# Usage: ./scripts/add-workflows-to-chart-dir.sh <chart_name>
# Example: ./scripts/add-workflows-to-chart-dir.sh qbittorrent
set -e
HELM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CHART_NAME="${1:?Usage: $0 <chart_name>}"
CHART_DIR="$HELM_DIR/$CHART_NAME"
# Tag prefix: chart name + -v (e.g. qbittorrent-v, paperless-ngx-v)
TAG_PREFIX="${CHART_NAME}-v"
# Workflow name suffix for display (e.g. "qbittorrent chart")
WF_NAME="$CHART_NAME"
RELEASE_WORKFLOW_NAME="Release $WF_NAME chart on merge to main"

mkdir -p "$CHART_DIR/.github/workflows"

cat > "$CHART_DIR/.github/workflows/release-on-merge-${CHART_NAME}.yml" << EOF
name: $RELEASE_WORKFLOW_NAME

on:
  push:
    branches: [main]
    paths:
      - 'Chart.yaml'
      - 'values.yaml'
      - 'values/**'
      - 'README.md'
      - '.helmignore'
      - 'templates/**'

concurrency: release-${CHART_NAME}

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
          tag_prefix: "${TAG_PREFIX}"
EOF

cat > "$CHART_DIR/.github/workflows/release-notes-${CHART_NAME}.yml" << EOF
name: Release notes ($CHART_NAME)

on:
  release:
    types: [published]
  workflow_run:
    workflows: ["$RELEASE_WORKFLOW_NAME"]
    types: [completed]
    branches: [main]
  workflow_dispatch:
    inputs:
      release_tag:
        description: 'Release tag (e.g. ${TAG_PREFIX}1.0.0). Default: latest.'
        required: false

jobs:
  update-release-notes:
    runs-on: ubuntu-latest
    if: |
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'release' && startsWith(github.event.release.tag_name, '${TAG_PREFIX}')) ||
      (github.event_name == 'workflow_run' && github.event.workflow_run.conclusion == 'success')
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Resolve release tag (${TAG_PREFIX}*)
        id: tag
        env:
          GH_TOKEN: \${{ secrets.GITHUB_TOKEN }}
        run: |
          if [ "\${{ github.event_name }}" = "release" ]; then
            echo "tag=\${{ github.event.release.tag_name }}" >> \$GITHUB_OUTPUT
          elif [ -n "\${{ github.event.inputs.release_tag }}" ]; then
            echo "tag=\${{ github.event.inputs.release_tag }}" >> \$GITHUB_OUTPUT
          else
            TAG=\$(gh api "repos/\${{ github.repository }}/releases?per_page=20" -q '[.[] | select(.tag_name | startswith("${TAG_PREFIX}")) | .tag_name][0]')
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

echo "Added .github/workflows for $CHART_NAME (tag_prefix: ${TAG_PREFIX})"
