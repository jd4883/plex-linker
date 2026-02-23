# Deploy Plex Linker

Application code and Docker build live in **docker/**; Helm chart in **helm/**.

| Path | Use case |
|------|----------|
| **docker/** | App source and Dockerfile (Chainguard Python). Build and run: see **docker/README.md**. |
| **helm/** | Kubernetes: Helm chart with optional media mount, secrets, External Secrets. |

Both expect API keys (Sonarr, Radarr, Plex) and optional `DATABASE_URL`. With a database, the app serves a web UI for link rules. See the main repo README and `docs/WHAT-IT-DOES.md` for behavior and config.
