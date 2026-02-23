# Changelog

All notable changes to the Unpackerr Helm chart are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-22

### Added

- Initial chart: Unpackerr daemon for *arr stack (Radarr, Sonarr, Lidarr, Readarr).
- bjw-s app-template wrapper with same download path layout as Lidarr (qbittorrent-*-downloads, sabnzbd-downloads).
- FLAC+CUE splitting for Lidarr via `UN_LIDARR_0_SPLIT_FLAC` (requires `golift/unpackerr:unstable`).
- **onepassworditem** dependency: 1Password item `vaults/Kubernetes/items/unpackerr` → secret **unpackerr** (envFrom).
- *arr URLs default to in-cluster DNS by project namespace: `lidarr.lidarr.svc.cluster.local`, `radarr.radarr.svc.cluster.local`, etc.
- Reloader annotation for secret changes; config PVC; webserver metrics on port 5656 for startup probe.
- Argo CD project **unpackerr** in central config (path `"."`, sourceRepo `jd4883/homelab-unpackerr`).
- **onepassword-secrets** values updated to include **unpackerr** namespace for central 1Password sync.
- GitHub Actions: `release-on-merge-unpackerr` and `release-notes-unpackerr` for automated releases and release notes.

### Documentation

- README: requirements, 1Password item field names, namespace unpackerr, Argo CD path, CUE splitting references (Lidarr #515, Unpackerr #141).

[1.0.0]: See releases in the repo that contains homelab/helm/unpackerr (tag: unpackerr-v1.0.0).
