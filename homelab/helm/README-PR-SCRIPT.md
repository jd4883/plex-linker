# Create/update PRs with 1Password

**Script:** `create-or-update-prs.sh`

Use this to open or update a PR for the current branch using 1Password for `GH_TOKEN` (no raw credentials). After a successful run, the script removes the PR body file and `RECENT_CHARTS_PR_ASSESSMENT.md` (ephemeral).

## Always use 1Password for GitHub auth

- **Any** command that needs GitHub auth (e.g. `git push`, `gh pr create`, `gh auth status`) must be run with 1Password so `GH_TOKEN` is injected:
  - `GH_HOST=github.com op run --env-file=homelab/.env.gh -- <command>`
- Example push (run from the **repo** you’re working on, e.g. plex chart repo):  
  `GH_HOST=github.com op run --env-file=homelab/.env.gh -- git push origin <branch>`
- **Repo context:** The workspace path may be named “home” — that is a folder name, not a GitHub repo. When working on the **plex** chart, the repo is the plex chart repo (e.g. `jd4883/homelab-plex` / `jd4883/tanzu-plex`), not “home”.

## Prerequisites

- **homelab/.env.gh** with `GH_TOKEN=op://Vault/Item/field`
- **Repo:** Either add `git remote origin` pointing at your GitHub repo, or set `HOMELAB_REPO=owner/repo` (e.g. `jd4883/homelab-plex` for the plex chart) when running.
- Branch pushed to the remote (for `gh pr create` to work).

## Run (1Password may prompt)

From workspace root (path may be named “home”; use the repo that matches your branch):

```bash
HOMELAB_REPO=owner/repo GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-or-update-prs.sh
```

If the repo has a remote: `GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-or-update-prs.sh`

## Branch → PR body mapping

The script uses `PR_DESCRIPTION.md` under the chart that matches the current branch. Supported branches (edit script to add more):

- `feature/kubernetes-dashboard-latest-okta` → `kubernetes-dashboard/PR_DESCRIPTION.md`
- `feature/organizr-tab-controller-in-helm` → `organizr-tab-controller/PR_DESCRIPTION.md`

Recreate the appropriate `PR_DESCRIPTION.md` (from CHART_STANDARD / pr-description-standard) before running if you need a PR body again. **Do not commit** PR body files — they are in `.gitignore`; use them only as the PR description when creating/updating the PR.
