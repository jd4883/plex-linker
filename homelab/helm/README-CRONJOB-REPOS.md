# CronJob chart repos and Plex design

## Design: secrets in Plex chart

The **Plex chart** is the place that **instantiates** the secrets for the two CronJob apps (one-pace-plex-assistant, plex-prefer-non-forced-subs) via **1Password (onepassworditem)**. The CronJob charts themselves are generic and only expect an existing Secret in the same namespace.

- **1Password** — Create items (e.g. `one-pace-plex-assistant`, `plex-prefer-non-forced-subs`) with the keys each app needs.
- **Plex chart** — `onepassworditem.secrets.plex` lists those items; the operator syncs them into Kubernetes Secrets in the release namespace.
- **Subcharts** — They receive `existingSecret: <name>` and mount that Secret. No secret creation in the generic charts.

See `plex/README.md` section **“Design: secrets and CronJob subcharts”**.

---

## Are the new chart dirs committed / in their own repos?

- **In this (home) repo:** The directories `homelab/helm/one-pace-plex-assistant` and `homelab/helm/plex-prefer-non-forced-subs` exist but are **untracked** until you add and commit them. Plex chart changes (deps, values, README) are also uncommitted while you’re on your branch.
- **Separate GitHub repos:** The two charts are **not** yet in their own repos. Use the script below to create the repos and open PRs.

---

## Create the two repos and open PRs (after re-auth)

1. **Re-authenticate GitHub CLI**
   ```bash
   gh auth login -h github.com
   ```
   Then confirm: `gh auth status`

2. **Create repos and push chart content + open PRs**
   ```bash
   cd homelab/helm
   chmod +x create-cronjob-chart-repos.sh
   ./create-cronjob-chart-repos.sh
   ```
   This will:
   - Create `jd4883/one-pace-plex-assistant-helm-chart` and `jd4883/plex-prefer-non-forced-subs-helm-chart` (if they don’t exist).
   - Clone each, copy the chart from `one-pace-plex-assistant/` or `plex-prefer-non-forced-subs/`, push to branch `feature/initial-helm-chart`, and open a PR into `main`.

3. **Commit and PR in the home repo** (new charts + Plex changes)
   ```bash
   git checkout -b feature/plex-cronjob-charts   # or use your current branch
   git add homelab/helm/one-pace-plex-assistant homelab/helm/plex-prefer-non-forced-subs homelab/helm/plex homelab/helm/create-cronjob-chart-repos.sh homelab/helm/README-CRONJOB-REPOS.md
   git status
   git commit -m "feat(plex): extract CronJob charts, instantiate secrets via 1Password in plex"
   git push -u origin feature/plex-cronjob-charts
   gh pr create --base main --head feature/plex-cronjob-charts --title "Plex: CronJob subcharts + secret design" --body "Two generic CronJob charts (one-pace-plex-assistant, plex-prefer-non-forced-subs); Plex instantiates secrets via onepassworditem; script to create their GitHub repos and PRs."
   ```

Override owner or branch if needed:
```bash
GITHUB_OWNER=yourorg BRANCH=feature/initial ./create-cronjob-chart-repos.sh
```
