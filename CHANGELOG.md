# Changelog

All notable changes to Plex Linker are documented here.

## [3.0.0] - 2026-02-23

### Added

- **Database-backed configuration** — SQLite by default (like Sonarr/Radarr); PostgreSQL supported via `DATABASE_URL`. No YAML config files.
- **Web UI and REST API** — Manage link rules at `/`; CRUD at `/api/rules` and `/api/settings/{key}`.
- **Helm chart** — `deploy/helm` for Kubernetes; optional media mount, supports 1Password and External Secrets.
- **Serve mode** — `plex-linker serve` runs the web app and a background link job on a configurable interval (default 15 min).

### Changed

- **Complete rewrite** — Flat module layout (6 Python files), `Settings` dataclass, shared `_ArrClient` base for Sonarr/Radarr.
- **Pure-Python symlinks** — Uses `os.symlink` and `os.path.relpath`; no shelling out to `ln`.
- **Chainguard Python image** — `cgr.dev/chainguard/python` for minimal, secure runtime.
- **Post-link refresh** — Sonarr `RescanSeries`/`RefreshSeries` and Radarr `RescanMovie` after creating or fixing links.

### Removed

- YAML configuration; all state in database.
- Legacy Python package structure and sub-packages.

---

[3.0.0]: https://github.com/jd4883/plex-linker/releases/tag/v3.0.0
