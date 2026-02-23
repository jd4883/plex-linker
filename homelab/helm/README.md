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
- **GitHub Actions (workflows):** Release-on-merge and release-notes workflows live under each chart’s `.github/workflows/` in the workspace. To add them to the chart repo: use a token with **workflow** scope and push, or copy the files into the repo via the GitHub UI. `update-open-prs-and-push-workflows.sh` updates open PR bodies from `PR_DESCRIPTION.md` and can push workflows when the token has workflow scope.
- **PR_DESCRIPTION.md:** Used only as the PR body (do not commit). Charts are gitignored for `PR_DESCRIPTION*.md`; create scripts exclude them when copying into a new repo.
- **Chart.lock:** Never committed. Run `helm dependency update` locally or in CI; `homelab/.gitignore` and create scripts exclude `Chart.lock`.
