# Homelab Helm charts

Helm charts and Argo CD–deployed applications for the homelab.

**Repo layout (canonical):** The path `homelab/helm` is where chart repos live. **Each chart is its own repo** (no monorepo). Pattern: `jd4883/homelab-<chart>`. **`homelab/helm/core`** is one repo with **submodules** (each submodule is its own repo; see `core/.gitmodules`). The workspace folder may be named "home" — that is a folder name only, not a GitHub repo.

---

## Standard and quality

- **Start here:** [**CHART_STANDARD.md**](./CHART_STANDARD.md) — minimum working baseline for every chart (artifacts, PR descriptions, deployment safety). Use it so charts are deployed **consistently** and we **don’t brick functionality**.
- **READMEs:** [README-STANDARD.md](./README-STANDARD.md) — structure and template for chart READMEs.
- **Design and ops:** [HELM_REVIEW.md](./HELM_REVIEW.md) — Argo CD mapping, shared volumes, Atlantis, security/ops/performance.

New or updated charts should meet CHART_STANDARD.md and use the pre-merge checklist there before merge.

**Conventions for chart READMEs:** Each chart README should include (1) an **Argo CD** section with an example `Application` manifest (repo/path/namespace adjusted for that chart), and (2) where the chart uses persistent volumes, a note that **volumes are defined in Longhorn** (PVCs are created in Longhorn or via bootstrap, not necessarily by the chart).

---

## Scripts and automation

- **Repo descriptions:** `./set-repo-descriptions.sh` (run with `GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/set-repo-descriptions.sh`).
- **Create new chart repo + PR:** `./create-chart-repo.sh <chart_name>` (e.g. `mealie`). Uses existing `jd4883/onepassword-secrets`; do **not** create `homelab-onepassword-secrets`.
- **Duplicate repo:** Argo config points **onepassword-secrets** to `jd4883/onepassword-secrets`. If `jd4883/homelab-onepassword-secrets` was created by mistake, delete it manually (GitHub → Settings → Delete repository); the API requires `delete_repo` scope.
- **GitHub Actions (workflows):** Release-on-merge and release-notes workflows live under each chart’s `.github/workflows/` in the workspace. To add them to the chart repo: use a token with **workflow** scope and push, or copy the files into the repo via the GitHub UI. `update-open-prs-and-push-workflows.sh` updates open PR bodies from `PR_DESCRIPTION.md` and can push workflows when the token has workflow scope. **Repos that still need workflows** (copy from workspace into the repo's `.github/workflows/`): `homelab-unpackerr` ← `helm/unpackerr/.github/workflows/`, `homelab-prometheus` ← `helm/prometheus/.github/workflows/`, `homelab-mealie` ← `helm/mealie/.github/workflows/`, `homelab-paperless-ngx` ← `helm/paperless-ngx/.github/workflows/`, `homelab-gotify` ← `helm/gotify/.github/workflows/`, `homelab-postgresql-backup-to-minio` ← `helm/postgresql-backup-to-minio/.github/workflows/`, `longhorn` ← `helm/longhorn/.github/workflows/`. Every chart dir in the workspace has release-on-merge and release-notes workflows. To push them to the six repos that don't yet have workflows on GitHub (homelab-unpackerr, homelab-prometheus, homelab-mealie, homelab-paperless-ngx, homelab-gotify, homelab-postgresql-backup-to-minio), run **`op run --env-file=homelab/.env.gh -- bash ./homelab/helm/scripts/sync-workflows-to-main.sh`**. If the push is rejected, add the two workflow files from `homelab/helm/<chart>/.github/workflows/` via the GitHub web UI (Add file → Create new file). To add workflows to a new chart dir: `./scripts/add-workflows-to-chart-dir.sh <chart_name>`.
- **PR_DESCRIPTION.md:** Used only as the PR body (do not commit). Charts are gitignored for `PR_DESCRIPTION*.md`; create scripts exclude them when copying into a new repo.
- **Chart.lock:** Never committed. Run `helm dependency update` locally or in CI; `homelab/.gitignore` and create scripts exclude `Chart.lock`.
- **Release notes:** Summaries only, not verbatim PR text. See [RELEASE-NOTES-STANDARD.md](./RELEASE-NOTES-STANDARD.md) for format and consistency across repos.
- **After merging a chart PR:** In that chart repo's clone run `git checkout main && git pull`, then delete the merged branch locally (`git branch -d feature/...`) and on remote if desired (`git push origin --delete feature/...`).
- **Audit chart repos:** `./scripts/audit-chart-repos.sh` — workflows present, unwanted files (Chart.lock, charts/, PR_DESCRIPTION.md), merged branches in longhorn clone.
- **Remove cruft via PR:** `bash ./scripts/remove-cruft-prs.sh` — creates PRs to remove PR_DESCRIPTION.md, Chart.lock, charts/, and .DS_Store; ensures .gitignore has .DS_Store. All commits use author Jacob Dresdale (no Cursor/bot). For workspace chart repos: **`bash ./scripts/sync-repos-cruft-and-prs.sh`** (with `op run --env-file=homelab/.env.gh`) — switches to main where the current branch is merged, creates `chore/cruft-dsstore-and-consistency` with .DS_Store in .gitignore, cruft removal, and consistent workflows; then push and open PR per repo.
- **Workflow file edits:** Commit and push workflow changes; do not pre-validate token scope. Fix access (e.g. workflow scope) after content is in git so all repos stay consistent.
- **Author identity:** Scripts that make commits set `user.name` / `user.email` to Jacob Dresdale / jd4883@users.noreply.github.com so you remain the sole contributor in these repos (no Cursor or bot in git history).
