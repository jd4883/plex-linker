# Homelab Helm charts — audit report

**Date:** 2026-02-21 (session)

---

## 1. Fixes applied this session

### Cursor rules and “home” wording

- **New rule:** `homelab/.cursor/rules/workspace-home-is-folder-not-repo.mdc` — Workspace path may be named “home”; that is a folder name only. Do not refer to a GitHub repo named “home”; use the actual repo (e.g. chart repo or monorepo) for context.
- **Updated rules:** `skip-repo-automation-home-homelab.mdc`, `pr-via-onepassword-gh.mdc` — Replaced “home repo” with “workspace / monorepo that contains homelab/”.
- **Script:** `create-or-update-prs.sh` — Example repo in comments/errors now `jd4883/homelab-plex` (not “home”).
- **Docs:** `prometheus/README.md`, `unpackerr/README.md`, `unpackerr/CHANGELOG.md`, `unpackerr/PR_DESCRIPTION.md`, `github-actions/README.md`, `README-CRONJOB-REPOS.md` — “home repo” → “monorepo” or “workspace root” / “repo that contains homelab/”.

### Release automation

- **create-initial-releases.sh** — Unpackerr added to the chart list so initial release can be created for the unpackerr chart.

---

## 2. Charts with uncommitted or untracked changes

From `git status homelab/helm homelab/helm/core`:

| Status   | Path |
|----------|------|
| Modified | `homelab/helm/README-PR-SCRIPT.md`, `create-or-update-prs.sh`, `prometheus/README.md`, `unpackerr/CHANGELOG.md`, `unpackerr/README.md` |
| Modified (submodule?) | `homelab/helm/atlantis`, `oauth2-proxy`, `plex` |
| Untracked | Many chart dirs: `audiobookshelf/`, `bazarr/`, `core/` (argocd, cert-manager, external-dns, …), `external-secrets/`, `harbor/`, `immich/`, `unpackerr/` (if not yet added), … |

**Recommendation:** Commit the fixes from this session (cursor rules, script, docs, create-initial-releases). For charts that are “untracked,” they are either new and should be added in a feature branch and PR, or they live in a separate repo and this workspace is a copy — ensure the source of truth repo has all changes and a PR. No automated push/PR was run from this workspace (per cursor rules).

---

## 3. Repo descriptions (GitHub)

Each GitHub repo that hosts a chart should have a short, professional **description** (e.g. `gh repo edit owner/repo --description "..."`). Use 1Password for `gh`:  
`GH_HOST=github.com op run --env-file=homelab/.env.gh -- gh repo edit OWNER/REPO --description "One-line description"`

Suggested descriptions (from Argo CD `config.yaml` or chart purpose):

| Repo | Suggested description |
|------|------------------------|
| jd4883/homelab-prometheus | Prometheus + Grafana (kube-prometheus-stack). HA; observability namespace; 1Password Grafana admin. |
| jd4883/homelab-k8s-dashboard | Kubernetes Dashboard; skip-login / Okta bypass options. |
| jd4883/homelab-reloader | Reloader — restarts pods on ConfigMap/Secret changes. |
| jd4883/homelab-oauth2-proxy | OAuth2 Proxy for ingress auth (e.g. GitHub OIDC). |
| jd4883/homelab-harbor | Harbor container registry. |
| jd4883/homelab-longhorn | Longhorn distributed block storage. |
| jd4883/homelab-plex | Plex Media Server + CronJob subcharts. |
| jd4883/homelab-atlantis | Atlantis for Terraform PR automation. |
| jd4883/homelab-audiobookshelf | Audiobookshelf — self-hosted audiobook and podcast server. |
| jd4883/homelab-immich | Immich photo/video backup (official chart + external Postgres). |
| jd4883/homelab-nextcloud | Nextcloud (official chart + external Postgres/Redis). |
| jd4883/homelab-kubernetes-dashboard | Kubernetes Dashboard Helm chart. |
| (monorepo) | If the repo that contains homelab/ is a single repo, set its description to something like: Homelab config: Helm charts, Argo CD, Terraform, GitHub Actions. |

Add rows for other `sourceRepo` values from `config.yaml` (homelab-qbittorrent, homelab-sabnzbd, homelab-minio, homelab-organizr, homelab-komga, homelab-mylar, homelab-prowlarr, homelab-portainer, homelab-nginx, homelab-external-dns, homelab-cert-manager, homelab-purelb, homelab-onepassword-connect, homelab-onepassword-secrets, homelab-external-secrets, homelab-kubernetes-replicator, homelab-home-assistant, homelab-tunnel-interface, homelab-ipmi-fan-control, homelab-external-services, jd4883/postgresql, jd4883/redis, jd4883/longhorn, jd4883/nvidia-k8s-device-plugin) and set descriptions accordingly.

---

## 4. Release notes and GitHub Actions

- **Charts with release-on-merge + release-notes workflows (in this workspace):** atlantis, audiobookshelf, harbor, immich, kubernetes-dashboard, longhorn, nextcloud, oauth2-proxy, plex, postgresql, redis, unpackerr. (Plus plex-autoskip.)
- **create-initial-releases.sh** now includes **unpackerr** so an initial release can be created for that chart.
- **Separate chart repos** (e.g. homelab-prometheus, homelab-plex): Each should have its own `.github/workflows/` for release-on-merge and release-notes if they are the source of truth for that chart. The monorepo workflows apply only to charts whose code lives in this repo.

**Recommendation:** For any chart that has a workflow here but no release yet, run (from repo root, with 1Password):  
`GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/github-actions/scripts/create-initial-releases.sh`  
Then trigger the corresponding release-notes workflow from the Actions tab or by merging a PR.

---

## 5. Documentation (per chart)

- **CHART_STANDARD.md** and **README-STANDARD.md** define the minimum bar: Chart.yaml (name, version, description), values top comment, README with Chart contents, Requirements, Key values, Render & validation, Argo CD (if applicable), Next steps.
- Charts that already have a README matching this structure: e.g. unpackerr, prometheus, nextcloud, atlantis, plex (see HELM_REVIEW.md for flat vs nested layout).
- **Recommendation:** For each chart in `homelab/helm` and `homelab/helm/core`, ensure a README exists and includes at least: title + one-line, Chart contents, Requirements, Key values, Render command, Argo CD (if used), Next steps. Add or update READMEs in the same PR as chart changes.

---

## 6. Cursor rules and broken code

- Cursor rules under `homelab/.cursor/rules/` are aligned with: no “home” as a repo name; PRs via 1Password where applicable; skip push/PR automation for this workspace; feature-branch and PR description standards.
- No functional chart code was changed in this session; only docs, scripts, and cursor rules. If you see linter or template errors in a chart, run `helm lint` and `helm template` from that chart directory and fix before merging.

---

## Summary

| Item | Status |
|------|--------|
| Cursor rules: “home” is folder, not repo | Fixed; new rule + doc/script wording updates |
| Charts with uncommitted changes | Listed above; commit fixes and open/update PRs per your workflow |
| Repo descriptions on GitHub | Table of suggested descriptions; run `gh repo edit` with 1Password |
| Release notes + GH Actions | Workflows present for 12+ charts; unpackerr added to create-initial-releases.sh |
| Per-chart documentation | Standard defined; audit each chart README against CHART_STANDARD / README-STANDARD |
| Functionally broken code | No chart logic changed this session |
