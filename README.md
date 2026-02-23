# Plex Linker

Sync TV specials from movies into show paths so Sonarr/Radarr and Plex share one file (links instead of duplicates). Useful when specials are easier to find via Radarr than Sonarr (e.g. anime specials in TMDB).

**Docker image:** `docker pull jb6magic/plex-linker:3.0` (built from **deploy/docker/** using Chainguard Python: `cgr.dev/chainguard/python`)

## v3 behavior

- **Web UI + database** — By default the app uses a SQLite DB and serves a web UI at `/` to manage link rules (movie → show mappings). No raw YAML config required. Set `DATABASE_URL` to override (e.g. another path or Postgres); unset to fall back to YAML.
- **Optional media mount** — If no media path is configured, the link job no-ops until you add a mount.
- **Serve mode** — `python3 main.py serve` runs FastAPI on `:8080`: `/health`, `/` (UI when DB is set), `/api/rules` and `/api/settings/{key}`. A background thread runs the link job on an interval (default 15 minutes).
- **Post-link refresh** — Sonarr/Radarr are refreshed after linking (RescanSeries/RefreshSeries, RescanMovie/RefreshMovie).

See **`docs/WHAT-IT-DOES.md`** for an exact description of the flow and config.

## Deploy

- **Application code and image:** All app source and the Dockerfile live in **`deploy/docker/`**. The image is built with Chainguard Python (`cgr.dev/chainguard/python`). Build: `docker build -f deploy/docker/Dockerfile deploy/docker`. Run: see **`deploy/docker/README.md`** for `docker run` examples and env vars.
- **Helm** (`deploy/helm/`): Kubernetes chart; uses the same image.

See **`deploy/README.md`** for a short overview.

- **Secrets / env:** `SONARR_0_API_KEY`, `SONARR_0_URL`, `SONARR_0_API_PATH` (default `/api/v3`); same for Radarr; `PLEX_API_KEY`, `PLEX_URL`. Optional `DATABASE_URL` (image default: `sqlite:////app/data/plex_linker.db`).
- **Media:** Set `MEDIA_ROOT` / `DOCKER_MEDIA_PATH` (e.g. via Helm `media.mountPath`) so the link job can run.

When using the **database**, add settings via API if needed: `PUT /api/settings/Movie Directories` with a JSON list of paths, and similarly for "Show Directories" and "Movie Extensions". The UI at `/` manages **link rules** only.

## Config (legacy YAML)

If `DATABASE_URL` is unset, the app reads link rules and paths from YAML under `config_files/` (see `docs/WHAT-IT-DOES.md`). Structure: movie title → `Movie DB ID` and `Shows` (show name → Episode, Season, etc.).

## One-shot / cron

```bash
docker run --rm -e MEDIA_ROOT=/media -e DOCKER_MEDIA_PATH=/media \
  -e SONARR_0_API_KEY=... -e RADARR_0_API_KEY=... -e PLEX_API_KEY=... \
  -v /path/to/media:/media \
  jb6magic/plex-linker:3.0 python3 main.py
```

Or run the image default: `python3 main.py serve` (web app + background link job).

## Development

- `python3 main.py` — run link job once.
- `python3 main.py serve --host 0.0.0.0 --port 8080` — web app and background link job.
- Set `DATABASE_URL=sqlite:////tmp/plex_linker.db` (or leave unset to use YAML). Set `MEDIA_ROOT` / `DOCKER_MEDIA_PATH` and Sonarr/Radarr/Plex env for the link job.
