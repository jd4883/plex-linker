# Create/update PRs with 1Password

**Script:** `create-or-update-prs.sh`

Use this to open or update a PR for the current branch using 1Password for `GH_TOKEN` (no raw credentials). After a successful run, the script removes the PR body file and `RECENT_CHARTS_PR_ASSESSMENT.md` (ephemeral).

## Prerequisites

- **homelab/.env.gh** with `GH_TOKEN=op://Vault/Item/field`
- **Repo:** Either add `git remote origin` pointing at your GitHub repo, or set `HOMELAB_REPO=owner/repo` (e.g. `jd4883/homelab`) when running.
- Branch pushed to the remote (for `gh pr create` to work).

## Run (1Password may prompt)

From repo root:

```bash
HOMELAB_REPO=owner/repo GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-or-update-prs.sh
```

If the repo has a remote: `GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-or-update-prs.sh`

## Branch → PR body mapping

The script uses `PR_DESCRIPTION.md` under the chart that matches the current branch. Supported branches (edit script to add more):

- `feature/kubernetes-dashboard-latest-okta` → `kubernetes-dashboard/PR_DESCRIPTION.md`
- `feature/organizr-tab-controller-in-helm` → `organizr-tab-controller/PR_DESCRIPTION.md`

Recreate the appropriate `PR_DESCRIPTION.md` (from CHART_STANDARD / pr-description-standard) before running if you need a PR body again. **Do not commit** PR body files — they are in `.gitignore`; use them only as the PR description when creating/updating the PR.
