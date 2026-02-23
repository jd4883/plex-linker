# plex-prefer-non-forced-subs (Helm chart)

Generic CronJob chart for [plex-prefer-non-forced-subs](https://github.com/jb6magic/plex-prefer-non-forced-subs). **Does not create secrets** — deploy in a namespace that already has the Secret.

**Instantiation:** Use this chart when you have the secret in a common namespace (e.g. Plex namespace); pass `existingSecret` and `env.plexUrl` via values.

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **Secret** | Kubernetes Secret with app-required keys (e.g. Plex token). Create via 1Password/onepassworditem or ExternalSecret in the same namespace. |

---

## Key values

| Area | Where | What to set |
|------|--------|-------------|
| Secret | `existingSecret` | Name of the Secret in this namespace. |
| Plex URL | `env.plexUrl` | e.g. `http://plex.plex:32400`. |
| Schedule | `schedule` | Cron (default `15 */3 * * *`). |

---

## Render & validation

> `helm template plex-prefer-non-forced-subs . -f values.yaml -n plex`
