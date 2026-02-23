# What Plex Linker Does

## Purpose

Sync **TV specials** that live as **movies** in Radarr into **show** paths that Sonarr and Plex expect, by creating **symlinks** so one file is shared instead of duplicating data.

Typical use: anime (or other) specials are easier to find in Radarr/TMDB; you want them to appear under the right show in Sonarr and Plex. The linker creates the symlink from the movie file to the show's specials path and tells Sonarr/Radarr to refresh.

## Architecture (v3 — flat module layout)

All Python lives in `deploy/docker/` as flat modules:

| Module | Role |
|--------|------|
| `main.py` | CLI entrypoint: `serve` (web + background job) or one-shot |
| `app.py` | FastAPI app: health, web UI, REST API for rules/settings |
| `config.py` | `Settings` frozen dataclass — reads all env vars once |
| `db.py` | SQLite CRUD for link rules and settings |
| `api_clients.py` | `SonarrClient` and `RadarrClient` with shared `_ArrClient` base |
| `linker.py` | Core link job: iterate rules, match Radarr movies, create symlinks, refresh Sonarr/Radarr |
| `yaml_config.py` | Legacy YAML config (when `DATABASE_URL` is unset) |

## Config: UI + database (default) or YAML (legacy)

- **Database (default):** Set `DATABASE_URL` (e.g. `sqlite:////app/data/plex_linker.db`). The app serves a **web UI** at `/` to manage link rules and uses the DB for rules and settings. No YAML files needed.
- **YAML (legacy):** Unset `DATABASE_URL` and provide `config_files/media_collection_parsed_last_run.yaml` and `config_files/variables.yaml` (Movie Directories, Show Directories, Movie Extensions).

## Link job flow (one run)

1. **Guard**: If `MEDIA_ROOT` is not set or not a directory, no-op.
2. **Lock**: Create `pid.lock`; skip if already locked.
3. **Clean**: Remove broken symlinks under the media root.
4. **Load data**: From DB or YAML — get `movies_dict` and settings.
5. **Fetch Radarr library**: `GET /api/v3/movie` — full movie list.
6. **Per movie rule**:
   - Find matching Radarr movie by TMDB ID.
   - Extract file path, quality, and extension from Radarr metadata.
   - **Per show** in the rule's `Shows`:
     - Sonarr lookup series by title → series ID, path, type (anime detection).
     - Find matching Season 0 episode → episode title.
     - Build destination path: `{show_path}/Season {season}/{title} - S{season}E{ep} - {episode_title} {quality}{ext}`.
     - Create relative symlink from movie file to show episode path (`os.symlink` with `os.path.relpath`).
     - Sonarr `RescanSeries` + `RefreshSeries`.
   - Radarr `RescanMovie`.
7. **YAML persist** (legacy only): Archive previous YAML, write updated dict.
8. **Unlock**: Remove `pid.lock`.

## Serve mode

FastAPI on port **8080** (uvicorn):

- **GET /health** — `200 ok`
- **GET /** — web UI (when `DATABASE_URL` set) or info page
- **GET/POST/DELETE /api/rules** — link rules CRUD
- **GET/PUT /api/settings/{key}** — settings CRUD

A background thread runs the link job on an interval (default 15 min).

## What it does *not* do

- Does not move or copy files; only creates symlinks.
- Does not scrape or discover rules automatically; rules come from YAML or the DB/UI.
- Plex API is not integrated; Sonarr/Radarr refresh is what makes new links visible.
