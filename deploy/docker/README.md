# Plex Linker — app and image (Chainguard Python)

Application code and the Dockerfile live in this directory. Image base: **`cgr.dev/chainguard/python`**.

## Build

From repo root:

```bash
docker build -f deploy/docker/Dockerfile deploy/docker -t jb6magic/plex-linker:3.0
```

From this directory:

```bash
docker build -t jb6magic/plex-linker:3.0 .
```

## Run

Example with env vars (no compose file):

```bash
docker run -d --name plex-linker -p 8080:8080 \
  -e SONARR_0_URL=http://sonarr:8989 \
  -e SONARR_0_API_PATH=/api/v3 \
  -e SONARR_0_API_KEY=your-key \
  -e RADARR_0_URL=http://radarr:7878 \
  -e RADARR_0_API_PATH=/api/v3 \
  -e RADARR_0_API_KEY=your-key \
  -e PLEX_URL=http://plex:32400 \
  -e PLEX_API_KEY=your-key \
  -e DATABASE_URL=sqlite:////app/data/plex_linker.db \
  -v /path/to/media:/media \
  jb6magic/plex-linker:3.0
```

- **Health:** http://localhost:8080/health  
- **UI (when `DATABASE_URL` set):** http://localhost:8080/

Env vars (override in container): `PLEX_LINKER`, `LOGS`, `CONFIG_ARCHIVES`, `DATABASE_URL`, `MEDIA_ROOT`, `DOCKER_MEDIA_PATH`, `SONARR_0_URL`, `SONARR_0_API_PATH`, `SONARR_0_API_KEY`, `RADARR_0_*`, `PLEX_URL`, `PLEX_API_KEY`, `PLEX_LINKER_SCAN_INTERVAL_MINUTES`, `TZ`. See main repo README and `docs/WHAT-IT-DOES.md`.
