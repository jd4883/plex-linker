# one-pace-plex-assistant (Helm chart)

Generic CronJob chart for [One Pace Plex Assistant](https://github.com/JakeLunn/one-pace-plex-assistant). **Does not create secrets** — deploy in a namespace that already has the Secret (e.g. created by the Plex chart's onepassworditem or ExternalSecret).

**Instantiation:** Use this chart when you have the secret in a common namespace (e.g. Plex namespace); pass `existingSecret` and PVC claims via values.

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **Secret** | Kubernetes Secret with at least **PLEX_API** (Plex auth token). Create via 1Password/onepassworditem or ExternalSecret in the same namespace. |
| **PVCs** | **one-pace** (e.g. `plex-anime-one-pace`) and **downloads** (e.g. `sabnzbd-downloads`) must exist in the namespace. |

---

## Key values

| Area | Where | What to set |
|------|--------|-------------|
| Secret | `existingSecret` | Name of the Secret in this namespace (e.g. `one-pace-plex-assistant`). |
| Plex URL | `env.plexUrl` | e.g. `http://plex.plex:32400` or `http://plex.<namespace>:32400`. |
| PVCs | `persistence.onePace`, `persistence.downloads` | `existingClaim` and `subPath` to match your layout. |
| Schedule | `schedule` | Cron expression (default `*/15 * * * *`). |

---

## Render & validation

> `helm template one-pace-plex-assistant . -f values.yaml -n plex`

---

## As a dependency (Plex chart)

The Plex chart can include this as a subchart and pass values so the CronJob uses the same namespace and secrets created by Plex (onepassworditem). Example in parent values:

```yaml
one-pace-plex-assistant:
  fullnameOverride: one-pace-plex-assistant
  existingSecret: one-pace-plex-assistant
  env:
    plexUrl: "http://plex.plex:32400"
  persistence:
    onePace:
      existingClaim: plex-anime-one-pace
      subPath: "One Piece [tvdb4-81797]"
    downloads:
      existingClaim: sabnzbd-downloads
      subPath: complete/sonarr
```
