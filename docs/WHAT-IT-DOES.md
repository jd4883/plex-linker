# What Plex Linker Does

## Purpose

Sync **TV specials** that live as **movies** in Radarr into **show** paths that Sonarr and Plex expect, by creating **symlinks** so one file is shared instead of duplicating data.

Typical use: anime (or other) specials are easier to find in Radarr/TMDB; you want them to appear under the right show in Sonarr and Plex. The linker creates the symlink from the movie file to the show’s specials path and tells Sonarr/Radarr to refresh.

## Config: UI + database (default) or YAML (legacy)

- **Database (default):** Set `DATABASE_URL` (e.g. `sqlite:////app/data/plex_linker.db`). The app serves a **web UI** at `/` to manage link rules and uses the DB for rules and settings. No YAML files needed.
- **YAML (legacy):** Unset `DATABASE_URL` and provide `config_files/media_collection_parsed_last_run.yaml` and `config_files/variables.yaml` (Movie Directories, Show Directories, Movie Extensions).

## Current flow (single link job run)

1. **Config**
   - **Media path:** `MEDIA_ROOT` / `DOCKER_MEDIA_PATH` must be set and point at a directory. If not set or not a directory, the link job **no-ops** and exits.
   - **Link rules:** From DB (when `DATABASE_URL` is set) or from YAML file.

2. **Load state**
   - Build **movies_dict**: map of movie display name → `{ "Movie DB ID": tmdb_id, "Shows": { show_name: { "Episode", "Season", "Episode ID", "seriesId", "tvdbId", ... } } }`.
   - Load **paths:** Movie Directories, Show Directories, Movie Extensions (from YAML or DB settings).

3. **APIs**
   - **Sonarr:** Base URL = `SONARR_0_URL` + `SONARR_0_API_PATH` (e.g. `/api/v3`). Used to: lookup series, get episodes by series id, get episode file, then **RescanSeries** and **RefreshSeries** after linking.
   - **Radarr:** Base URL = `RADARR_0_URL` + `RADARR_0_API_PATH`. Used to: get movie library, then **RescanMovie** after linking.

4. **Per-movie / per-show**
   - For each movie in **movies_dict**, build a **Movie** (Radarr metadata) and for each show in its **Shows**:
     - **Sonarr** lookup series by title → get series id and paths.
     - Get episodes for that series (season 0 specials).
     - Match episode/season to the rule → get target path and episode file id.
     - **Symlink** the movie file to the show’s special path (e.g. `Show Name/Season 00/Show Name - S00E01 - Title.mkv`).
     - Call Sonarr **RescanSeries** and **RefreshSeries** for that series.
   - After processing all shows for that movie, call Radarr **RescanMovie** for that movie.

5. **Cleanup**
   - Remove broken symlinks under media root (`find . -xtype l -delete`).
   - **YAML mode only:** Write updated **movies_dict** back to `media_collection_parsed_last_run.yaml`. **DB mode:** No YAML write; rules stay in the DB.

6. **Serve mode**
   - Process listens on port **8080** (FastAPI + uvicorn):
     - **GET /health** — returns 200 for liveness/readiness.
     - **GET /** — when `DATABASE_URL` is set: web UI to list/add/delete link rules; otherwise a short message.
     - **GET/POST/DELETE /api/rules** — when DB is set: list, add, delete link rules.
     - **GET/PUT /api/settings/{key}** — when DB is set: read/write settings (e.g. Movie Directories, Show Directories, Movie Extensions).
   - A **background thread** runs the link job on an interval (default 15 minutes).

## What it does *not* do

- Does not move or copy files; only creates symlinks.
- Does not scrape or discover rules automatically; rules come from YAML or the DB/UI.
- Plex API is stubbed; no Plex library refresh or watch-state sync yet (Sonarr/Radarr refresh is what makes new links visible).

## Config summary

| Source | Purpose |
|--------|--------|
| Env / Secret | `SONARR_0_URL`, `SONARR_0_API_PATH`, `SONARR_0_API_KEY`, same for Radarr; `PLEX_URL`, `PLEX_API_KEY`; `MEDIA_ROOT`/`DOCKER_MEDIA_PATH`; `DATABASE_URL` (default in image: SQLite at `/app/data/plex_linker.db`). |
| Database (default) | Link rules and settings; web UI at `/` and REST API at `/api/rules`, `/api/settings/{key}`. When using DB, add settings "Movie Directories", "Show Directories", "Movie Extensions" (lists) via API or seed manually. |
| YAML (legacy) | When `DATABASE_URL` is unset: `variables.yaml` and `media_collection_parsed_last_run.yaml` as before. |
