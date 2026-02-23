# Plex Linker — Docker image (Chainguard Python)

Application code and the Dockerfile live in this directory. Image base: **`cgr.dev/chainguard/python`**.

## Files

| File | Purpose |
|------|---------|
| `main.py` | Entrypoint: `serve` (FastAPI + background job) or one-shot link run |
| `app.py` | FastAPI app: `/health`, web UI at `/`, REST API at `/api/rules` and `/api/settings/{key}` |
| `config.py` | `Settings` frozen dataclass — all env vars in one place |
| `db.py` | SQLAlchemy-based CRUD for link rules and settings (SQLite or PostgreSQL) |
| `api_clients.py` | `SonarrClient` and `RadarrClient` with shared `_ArrClient` base |
| `linker.py` | Core link job: Radarr movie -> Sonarr show symlinks |

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

### SQLite (default, no external DB needed)

```bash
docker run -d --name plex-linker -p 8080:8080 \
  -e SONARR_0_URL=http://sonarr:8989 \
  -e SONARR_0_API_KEY=your-key \
  -e RADARR_0_URL=http://radarr:7878 \
  -e RADARR_0_API_KEY=your-key \
  -e MEDIA_ROOT=/media \
  -v /path/to/media:/media \
  -v plex-linker-data:/app/data \
  jb6magic/plex-linker:3.0
```

### PostgreSQL

```bash
docker run -d --name plex-linker -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@postgres-host:5432/plex_linker \
  -e SONARR_0_URL=http://sonarr:8989 \
  -e SONARR_0_API_KEY=your-key \
  -e RADARR_0_URL=http://radarr:7878 \
  -e RADARR_0_API_KEY=your-key \
  -e MEDIA_ROOT=/media \
  -v /path/to/media:/media \
  jb6magic/plex-linker:3.0
```

- **Health:** http://localhost:8080/health
- **UI:** http://localhost:8080/

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:////app/data/plex_linker.db` | SQLite path or PostgreSQL URL |
| `SONARR_0_URL` | — | Sonarr base URL |
| `SONARR_0_API_PATH` | `/api/v3` | Sonarr API path |
| `SONARR_0_API_KEY` | — | Sonarr API key |
| `RADARR_0_URL` | — | Radarr base URL |
| `RADARR_0_API_PATH` | `/api/v3` | Radarr API path |
| `RADARR_0_API_KEY` | — | Radarr API key |
| `PLEX_URL` | — | Plex server URL |
| `PLEX_API_KEY` | — | Plex API token |
| `MEDIA_ROOT` | — | Media library root path |
| `DOCKER_MEDIA_PATH` | — | Alias for `MEDIA_ROOT` inside container |
| `SONARR_ROOT_PATH_PREFIX` | `/` | Prefix to strip from Sonarr series paths |
| `PLEX_LINKER_SCAN_INTERVAL_MINUTES` | `15` | Background link-job interval |
| `TZ` | `UTC` | Container timezone |

See the main repo README and `docs/WHAT-IT-DOES.md` for behavior details.
