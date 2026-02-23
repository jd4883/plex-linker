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
| `db.py` | SQLAlchemy-based CRUD for link rules and settings (SQLite or PostgreSQL) |
| `api_clients.py` | `SonarrClient` and `RadarrClient` with shared `_ArrClient` base |
| `linker.py` | Core link job: iterate rules, match Radarr movies, create symlinks, refresh Sonarr/Radarr |

## Database

All state lives in a database. Set `DATABASE_URL`:

- **SQLite (default):** `sqlite:////app/data/plex_linker.db` — no external database required.
- **PostgreSQL:** `postgresql://user:pass@host:5432/plex_linker` — uses the pure-Python `pg8000` driver (auto-rewritten to `postgresql+pg8000://` internally).

Tables are created automatically on first run. The web UI at `/` and the REST API at `/api/rules` manage link rules. Settings (like "Movie Directories") can be managed via `/api/settings/{key}`.

## Link job flow (one run)

1. **Guard**: If `MEDIA_ROOT` is not set or not a directory, no-op. If `DATABASE_URL` is not set, error.
2. **Lock**: Create `pid.lock`; skip if already locked.
3. **Clean**: Remove broken symlinks under the media root.
4. **Load rules**: `db.get_movies_dict()` — link rules from the database.
5. **Fetch Radarr library**: `GET /api/v3/movie` — full movie list.
6. **Per movie rule**:
   - Find matching Radarr movie by TMDB ID.
   - Extract file path, quality, and extension from Radarr metadata.
   - **Per show** in the rule's `Shows`:
     - Sonarr lookup series by title -> series ID, path, type (anime detection).
     - Find matching Season 0 episode -> episode title.
     - Build destination path: `{show_path}/Season {season}/{title} - S{season}E{ep} - {episode_title} {quality}{ext}`.
     - Create relative symlink from movie file to show episode path (`os.symlink` with `os.path.relpath`).
     - Sonarr `RescanSeries` + `RefreshSeries`.
   - Radarr `RescanMovie`.
7. **Unlock**: Remove `pid.lock`.

## Serve mode

FastAPI on port **8080** (uvicorn):

- **GET /health** — `200 ok`
- **GET /** — web UI to list/add/delete link rules
- **GET/POST/DELETE /api/rules** — link rules CRUD
- **GET/PUT /api/settings/{key}** — settings CRUD

A background thread runs the link job on an interval (default 15 min).

## What it does *not* do

- Does not move or copy files; only creates symlinks.
- Does not scrape or discover rules automatically; rules come from the DB/UI.
- Plex API is not integrated; Sonarr/Radarr refresh is what makes new links visible.
