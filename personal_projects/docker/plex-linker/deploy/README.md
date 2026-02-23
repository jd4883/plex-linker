# Deploy Plex Linker

Application code and Docker build live in **docker/**; Helm chart in **helm/**.

| Path | Use case |
|------|----------|
| **docker/** | App source and Dockerfile (Chainguard Python). Build and run: see **docker/README.md**. |
| **helm/** | Kubernetes: Helm chart with optional media mount, secrets, External Secrets. |

Both expect API keys (Sonarr, Radarr) and `DATABASE_URL` (SQLite by default; PostgreSQL supported). The app serves a web UI for link rules at `/`. See the main repo README and `docs/WHAT-IT-DOES.md` for behavior and config.
