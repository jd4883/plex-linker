# Plex Linker — Docker image (Chainguard Python)

Application code and the Dockerfile live in this directory. Image base: **`cgr.dev/chainguard/python`**.

## Files

| File | Purpose |
|------|---------|
| `main.py` | Entrypoint: `serve` (FastAPI + background job) or one-shot link run |
| `app.py` | FastAPI app: `/health`, web UI at `/`, REST API at `/api/rules` and `/api/settings/{key}` |
| `config.py` | `Settings` frozen dataclass — all env vars in one place |
| `db.py` | SQLite CRUD for link rules and settings |
| `api_clients.py` | `SonarrClient` and `RadarrClient` with shared `_ArrClient` base |
| `linker.py` | Core link job: Radarr movie → Sonarr show symlinks |
| `yaml_config.py` | Legacy YAML config reader/writer (when `DATABASE_URL` is unset) |

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

```bash
docker run -d --name plex-linker -p 8080:8080 \
  -e SONARR_0_URL=http://sonarr:8989 \
  -e SONARR_0_API_KEY=your-key \
  -e RADARR_0_URL=http://radarr:7878 \
  -e RADARR_0_API_KEY=your-key \
  -e PLEX_URL=http://plex:32400 \
  -e PLEX_API_KEY=your-key \
  -e DATABASE_URL=sqlite:////app/data/plex_linker.db \
  -v /path/to/media:/media \
  -e MEDIA_ROOT=/media \
  jb6magic/plex-linker:3.0
```

- **Health:** http://localhost:8080/health
- **UI:** http://localhost:8080/ (when `DATABASE_URL` is set)

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SONARR_0_URL` | — | Sonarr base URL |
| `SONARR_0_API_PATH` | `/api/v3` | Sonarr API path |
| `SONARR_0_API_KEY` | — | Sonarr API key |
| `RADARR_0_URL` | — | Radarr base URL |
| `RADARR_0_API_PATH` | `/api/v3` | Radarr API path |
| `RADARR_0_API_KEY` | — | Radarr API key |
| `PLEX_URL` | — | Plex server URL |
| `PLEX_API_KEY` | — | Plex API token |
| `DATABASE_URL` | `sqlite:////app/data/plex_linker.db` | SQLite (or unset for legacy YAML) |
| `MEDIA_ROOT` | — | Media library root path |
| `DOCKER_MEDIA_PATH` | — | Alias for `MEDIA_ROOT` inside container |
| `SONARR_ROOT_PATH_PREFIX` | `/` | Prefix to strip from Sonarr series paths |
| `PLEX_LINKER_SCAN_INTERVAL_MINUTES` | `15` | Background link-job interval |
| `TZ` | `UTC` | Container timezone |

See the main repo README and `docs/WHAT-IT-DOES.md` for behavior details.
