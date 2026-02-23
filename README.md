# Plex Linker

Sync TV specials from movies into show paths so Sonarr/Radarr and Plex share one file (symlinks instead of duplicates). Useful when specials are easier to find via Radarr than Sonarr (e.g. anime specials in TMDB).

**Docker image:** `docker pull jb6magic/plex-linker:3.0` (Chainguard Python: `cgr.dev/chainguard/python`)

## v3 highlights

- **Database-backed** — SQLite by default (like Sonarr/Radarr); switch to PostgreSQL by changing `DATABASE_URL`. Web UI at `/` to manage link rules. No YAML config files.
- **Flat module layout** — 6 Python files, no sub-packages. See **`docs/WHAT-IT-DOES.md`** for the full architecture.
- **`os.symlink`** — pure-Python relative symlinks; no shelling out to `ln`.
- **`Settings` dataclass** — frozen, `@lru_cache`d config from env vars; single source of truth.
- **Shared API client base** — `SonarrClient` and `RadarrClient` extend `_ArrClient`; no duplicated HTTP code.
- **SQLAlchemy** — same schema works on SQLite and PostgreSQL; `pg8000` pure-Python driver for Postgres.

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

Optional: `DATABASE_URL` (default `sqlite:////app/data/plex_linker.db`; set `postgresql://user:pass@host/db` for Postgres), `PLEX_URL`, `PLEX_API_KEY`, `SONARR_ROOT_PATH_PREFIX`, `PLEX_LINKER_SCAN_INTERVAL_MINUTES`. Full list in **`deploy/docker/README.md`**.

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

Set `DATABASE_URL=sqlite:////tmp/plex_linker.db` and `MEDIA_ROOT` plus Sonarr/Radarr env for the link job.
