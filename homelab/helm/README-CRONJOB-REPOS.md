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

## Create the two repos and open PRs (1Password prompts for creds)

No need to be logged in to `gh`. Use 1Password CLI so it prompts you for credentials each time:

**From repo root:**
```bash
GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-cronjob-chart-repos.sh
```

- **homelab/.env.gh** must contain: `GH_TOKEN=op://VaultName/ItemName/field_name` (1Password reference). When you run the command, 1Password will prompt you to sign in if needed and inject the token.
- The script will: create the two GitHub repos (if missing), clone via HTTPS using the token, copy the chart files, push to branch `feature/initial-helm-chart`, and open a PR in each repo.

Override owner or branch if needed:
```bash
GITHUB_OWNER=yourorg BRANCH=feature/initial GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-cronjob-chart-repos.sh
```

**Commit and PR in the home repo** (after pushing your branch and creating the two chart repos):
```bash
GH_HOST=github.com op run --env-file=homelab/.env.gh -- gh pr create --base main --head feature/secrets-immich-harbor-longhorn --title "Plex CronJob charts + repo script" --body "Add one-pace-plex-assistant and plex-prefer-non-forced-subs charts; script uses op run for creds; design doc."
```
