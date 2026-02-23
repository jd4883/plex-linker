# Plex Linker

Sync TV specials from movies into show paths so Sonarr/Radarr and Plex share one file (symlinks instead of duplicates). Useful when specials are easier to find via Radarr than Sonarr (e.g. anime specials in TMDB).

**Docker image:** `docker pull jb6magic/plex-linker:3.0` (Chainguard Python: `cgr.dev/chainguard/python`)

## v3 highlights

- **Flat module layout** — 7 Python files, no sub-packages. See **`docs/WHAT-IT-DOES.md`** for the full architecture.
- **Web UI + database** — SQLite DB by default; web UI at `/` to manage link rules. Unset `DATABASE_URL` to fall back to legacy YAML.
- **`os.symlink`** — pure-Python relative symlinks; no shelling out to `ln`.
- **`Settings` dataclass** — frozen, `@lru_cache`d config from env vars; single source of truth.
- **Shared API client base** — `SonarrClient` and `RadarrClient` extend `_ArrClient`; no duplicated HTTP code.
- **Proper logging** — `logging.getLogger(__name__)` throughout; no custom messaging layers.

## Deploy

- **Docker** (`deploy/docker/`): App source, Dockerfile, and `docker run` examples. See **`deploy/docker/README.md`**.
- **Helm** (`deploy/helm/`): Kubernetes chart; uses the same image.

See **`deploy/README.md`** for a short overview.

### Required env vars

| Variable | Example |
|----------|---------|
| `SONARR_0_URL` | `http://sonarr:8989` |
| `SONARR_0_API_KEY` | `your-key` |
| `RADARR_0_URL` | `http://radarr:7878` |
| `RADARR_0_API_KEY` | `your-key` |
| `MEDIA_ROOT` | `/media` |

Optional: `DATABASE_URL` (default `sqlite:////app/data/plex_linker.db`), `PLEX_URL`, `PLEX_API_KEY`, `SONARR_ROOT_PATH_PREFIX`, `PLEX_LINKER_SCAN_INTERVAL_MINUTES`. Full list in **`deploy/docker/README.md`**.

## One-shot / cron

```bash
docker run --rm \
  -e MEDIA_ROOT=/media -e SONARR_0_API_KEY=... -e RADARR_0_API_KEY=... \
  -e SONARR_0_URL=http://sonarr:8989 -e RADARR_0_URL=http://radarr:7878 \
  -v /path/to/media:/media \
  jb6magic/plex-linker:3.0 python3 main.py
```

Default CMD is `python3 main.py serve` (web app + background link job on a 15-minute interval).

## Development

```bash
cd deploy/docker
pip install -r requirements.txt

# one-shot link job
python3 main.py

# web app + background job
python3 main.py serve --host 0.0.0.0 --port 8080
```

Set `DATABASE_URL=sqlite:////tmp/plex_linker.db` (or unset for YAML). Set `MEDIA_ROOT` and Sonarr/Radarr env for the link job.

## Config (legacy YAML)

When `DATABASE_URL` is unset, link rules and settings come from YAML files under `config_files/`. See **`docs/WHAT-IT-DOES.md`** for the format.
