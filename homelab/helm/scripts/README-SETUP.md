# Helm Chart Repos Setup

Scripts for GitHub Actions, secrets, descriptions, and consistency across homelab/helm and homelab/helm/core chart repos.

## Quick run (1Password auth)

From workspace root:

```bash
GH_HOST=github.com op run --env-file=homelab/.env.gh -- bash homelab/helm/scripts/setup-all-repos.sh
```

This runs:
1. **ensure-gitignore-consistency.sh** — Adds `.DS_Store`, `charts/`, `Chart.lock`, `PR_DESCRIPTION*.md` to `.gitignore` where missing
2. **set-repo-descriptions.sh** — Sets GitHub repo descriptions for all chart repos
3. **set-openai-secrets-in-repos.sh** — Sets `OPENAI_API_KEY` secret in all repos with release-notes workflows (reads from 1Password `op://Homelab/OpenAI/api_key`)

## Individual scripts

| Script | Purpose |
|--------|---------|
| `add-workflows-to-chart-dir.sh <chart_name>` | Add release-on-merge + release-notes workflows to a flat chart dir |
| `add-workflows-helm-subdir.sh <chart_name>` | Add workflows for charts with `helm/` subdir (lidarr, prowlarr, radarr, readarr, sonarr) |
| `ensure-gitignore-consistency.sh` | Standard .gitignore entries across all charts |
| `set-openai-secrets-in-repos.sh` | `gh secret set OPENAI_API_KEY` for repos with release-notes |
| `sync-repos-cruft-and-prs.sh` | Switch to main when merged; create chore PR for cruft + workflows |

## Prerequisites

- **1Password CLI** (`op`) — `op run` injects `GH_TOKEN` and `OPENAI_API_KEY` from `homelab/.env.gh`
- **gh** — GitHub CLI for `gh secret set`, `gh repo edit`
- **homelab/.env.gh** — Must contain:
  - `GH_TOKEN=op://Personal/GitHub/GITHUB_TOKEN`
  - `OPENAI_API_KEY=op://Homelab/OpenAI/api_key`

## Workflow coverage

All chart dirs under `homelab/helm` and `homelab/helm/core` now have:
- **release-on-merge** — Lint + release on push to main (chart changes)
- **release-notes** — OpenAI-summarized release body from merged PR (requires `OPENAI_API_KEY`)

Release-notes workflows include `pull-requests: read` and `contents: write` permissions.

## Push changes

After running setup, commit workflow and .gitignore changes, then:

```bash
GH_HOST=github.com op run --env-file=homelab/.env.gh -- bash homelab/helm/scripts/sync-repos-cruft-and-prs.sh
```

This pushes to each repo and opens PRs for the chore branch.
