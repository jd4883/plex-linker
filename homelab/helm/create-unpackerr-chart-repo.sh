#!/usr/bin/env bash
# Create jd4883/homelab-unpackerr (if missing), push chart + workflows, open PR.
# Run with 1Password: GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-unpackerr-chart-repo.sh
set -euo pipefail
HELM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HELM_DIR/../.." && pwd)"
REPO_OWNER="${GITHUB_OWNER:-jd4883}"
REPO_FULL="${REPO_OWNER}/homelab-unpackerr"
BRANCH="${BRANCH:-feature/initial-helm-chart}"
CHART_SOURCE="$HELM_DIR/unpackerr"
PR_BODY_FILE="$CHART_SOURCE/PR_DESCRIPTION.md"

if [ -z "${GH_TOKEN:-}" ]; then
  echo "GH_TOKEN is not set. Run with: GH_HOST=github.com op run --env-file=homelab/.env.gh -- $0"
  exit 1
fi

if [ ! -d "$CHART_SOURCE" ] || [ ! -f "$CHART_SOURCE/Chart.yaml" ]; then
  echo "Chart not found at $CHART_SOURCE."
  exit 1
fi

_gh_url() { echo "https://x-access-token:${GH_TOKEN}@github.com/${1}.git"; }

# Workflows: use committed files from chart source if present; else generate into temp dir
WORKFLOWS_DIR=""
if [ -f "$CHART_SOURCE/.github/workflows/release-on-merge-unpackerr.yml" ] && [ -f "$CHART_SOURCE/.github/workflows/release-notes-unpackerr.yml" ]; then
  WORKFLOWS_DIR="$CHART_SOURCE/.github/workflows"
else
  mkdir -p "$HELM_DIR/.unpackerr-repo-workflows"
  WORKFLOWS_DIR="$HELM_DIR/.unpackerr-repo-workflows"
  cat > "$WORKFLOWS_DIR/release-on-merge-unpackerr.yml" << 'WORKFLOW'
name: Release unpackerr chart on merge to main

on:
  push:
    branches: [main]
    paths:
      - 'Chart.yaml'
      - 'values.yaml'
      - 'README.md'
      - '.helmignore'
      - 'templates/**'

concurrency: release-unpackerr

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
          helm repo add bjw-s https://bjw-s-labs.github.io/helm-charts
          helm repo add vquie https://vquie.github.io/helm-charts
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
          github_token: ${{ secrets.GITHUB_TOKEN }}
          tag_prefix: "unpackerr-v"
WORKFLOW

cat > "$WORKFLOWS_DIR/release-notes-unpackerr.yml" << 'WORKFLOW'
name: Release notes (unpackerr)

on:
  release:
    types: [published]
  workflow_run:
    workflows: ["Release unpackerr chart on merge to main"]
    types: [completed]
    branches: [main]
  workflow_dispatch:
    inputs:
      release_tag:
        description: 'Release tag (e.g. unpackerr-v1.0.0). Default: latest.'
        required: false

jobs:
  update-release-notes:
    runs-on: ubuntu-latest
    if: |
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'release' && startsWith(github.event.release.tag_name, 'unpackerr-v')) ||
      (github.event_name == 'workflow_run' && github.event.workflow_run.conclusion == 'success')
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Resolve release tag (unpackerr-v*)
        id: tag
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          if [ "${{ github.event_name }}" = "release" ]; then
            echo "tag=${{ github.event.release.tag_name }}" >> $GITHUB_OUTPUT
          elif [ -n "${{ github.event.inputs.release_tag }}" ]; then
            echo "tag=${{ github.event.inputs.release_tag }}" >> $GITHUB_OUTPUT
          else
            TAG=$(gh api "repos/${{ github.repository }}/releases?per_page=20" -q '[.[] | select(.tag_name | startswith("unpackerr-v")) | .tag_name][0]')
            [ -z "$TAG" ] || [ "$TAG" = "null" ] && exit 1
            echo "tag=$TAG" >> $GITHUB_OUTPUT
          fi
        shell: bash
      - name: Update release notes from PR (OpenAI)
        uses: expectedbehaviors/github-actions/.github/actions/release-notes@main
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          release_tag: ${{ steps.tag.outputs.tag }}
WORKFLOW
fi

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"; [ -d "$HELM_DIR/.unpackerr-repo-workflows" ] && rm -rf "$HELM_DIR/.unpackerr-repo-workflows"' EXIT

if ! gh repo view "$REPO_FULL" &>/dev/null; then
  echo "Creating repo $REPO_FULL..."
  gh repo create "$REPO_FULL" --public --description "Unpackerr for *arr stack. FLAC+CUE splitting (unstable). 1Password, Argo CD." --add-readme
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
  mkdir -p .github/workflows
  # Add workflows only if GH_TOKEN has workflow scope (else push chart first, add workflows in follow-up)
  if [ "${SKIP_WORKFLOWS:-}" != "1" ] && [ -n "$WORKFLOWS_DIR" ]; then
    mkdir -p .github/workflows
    cp "$WORKFLOWS_DIR"/release-on-merge-unpackerr.yml "$WORKFLOWS_DIR"/release-notes-unpackerr.yml .github/workflows/ 2>/dev/null || true
  fi
  git add -A
  if git diff --staged --quiet; then
    echo "No changes for unpackerr chart."
    exit 0
  fi
  git commit -m "feat: Unpackerr Helm chart — bjw-s app-template, 1Password, FLAC+CUE splitting${SKIP_WORKFLOWS:+ (add workflows in follow-up PR)}"
  git push -u origin "$BRANCH" || {
    if git log -1 --name-only --oneline | grep -q '\.github/workflows/'; then
      echo "Push failed (often: token missing 'workflow' scope). Retrying without workflows: SKIP_WORKFLOWS=1"
      git reset --soft HEAD~1
      rm -rf .github/workflows
      git add -A && git commit -m "feat: Unpackerr Helm chart — bjw-s app-template, 1Password, FLAC+CUE splitting"
      git push -u origin "$BRANCH"
    else
      exit 1
    fi
  }
  if gh pr view --repo "$REPO_FULL" --head "$BRANCH" &>/dev/null; then
    echo "PR already exists: https://github.com/$REPO_FULL/pulls"
  else
    if [ -f "$PR_BODY_FILE" ]; then
      gh pr create --base main --head "$BRANCH" --title "Unpackerr chart — CUE splitting, 1Password, Argo CD, release automation" --body-file "$PR_BODY_FILE"
    else
      gh pr create --base main --head "$BRANCH" --title "Unpackerr chart — CUE splitting, 1Password, Argo CD, release automation" --body "Unpackerr Helm chart: bjw-s app-template, onepassworditem, *arr URLs, FLAC+CUE splitting (unstable). Release-on-merge and release-notes workflows included."
    fi
    echo "PR: https://github.com/$REPO_FULL/pulls"
  fi
)

echo "Done. Argo CD (config.yaml) syncs from $REPO_FULL with path \".\"."