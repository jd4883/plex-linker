# Plex Linker v3 — bjw-s chart, optional media, release automation, post-link refresh

---

## TL;DR

- **Helm:** Added `deploy/helm` (v3.0.0) with optional media: no default mount so the app runs and the link job no-ops until user adds `media.mountPath` and a volume.
- **App:** Link job returns early when `MEDIA_ROOT`/`DOCKER_MEDIA_PATH` is unset or not a directory; after create/fix link we call Sonarr RescanSeries, Radarr RescanMovie (and Plex partial refresh by path when implemented).
- **CI:** Release on merge to main (initial_version 3.0.0), Docker build/push to jb6magic/plex-linker, release-notes workflow for release body.
- **Behavior:** Equivalent to before when media is configured; safe to deploy without media.

## Summary

| Area | Change |
|------|--------|
| **Chart** | New `deploy/helm` with Chart 3.0.0, optional `media.mountPath` / volume |
| **Media** | No default media; examples in `deploy/helm/README.md` (single root, PVC) |
| **Link** | Early return if no media root; Sonarr/Radarr refresh after link; Sonarr uses `seriesId` for RescanSeries/RefreshSeries |
| **Release** | release-on-merge (3.0.0), docker-build-push, release-notes workflows |

## Render & validation

- `helm dependency update deploy/helm` (no deps) — OK
- `helm template plex-linker deploy/helm -f deploy/helm/values.yaml` — renders Deployment, Service; with `media.mountPath: ""` no volume/volumeMount
- With `media.mountPath: /media` and `volumeSpec` or `existingClaim` — volume and MEDIA_ROOT env set

## Supporting evidence

<details>
<summary>Deployment (no media) — no volumeMount, no MEDIA_ROOT</summary>

```yaml
# values: media.mountPath: ""
env:
  - name: TZ
    value: "US/Pacific"
  # no MEDIA_ROOT
volumeMounts: []   # none
volumes: []       # none
```

</details>

<details>
<summary>Deployment (with media) — volume and MEDIA_ROOT</summary>

```yaml
env:
  - name: MEDIA_ROOT
    value: "/media"
  - name: DOCKER_MEDIA_PATH
    value: "/media"
volumeMounts:
  - name: media
    mountPath: /media
volumes:
  - name: media
    emptyDir: {}  # or PVC / volumeSpec
```

</details>

## Why safe & correct

- No credentials in values or rendered manifests (secretRef only).
- Optional media: app and link job already handle missing path; we only formalize early exit and conditional mount.
- Refresh calls are best-effort (try/except); Radarr RescanMovie uses `movieId`; Sonarr uses `seriesId`.

## How to test

1. From repo root: `helm template plex-linker deploy/helm -f deploy/helm/values.yaml`
2. Set `media.mountPath: /media` and a volume, then `helm upgrade --install plex-linker deploy/helm -n plex-linker --create-namespace -f my-values.yaml` (with Secret for API keys and DATABASE_URL).

## Post-merge

- Tag v3.0.0 and GitHub Release will be created by release-on-merge.
- Docker image will be built and pushed by docker-build-push.
- Release notes workflow will fill the release body from the merged PR.
