# Plex Linker Helm chart (v3)

Deploy Plex Linker with optional media mount. When `media.mountPath` is empty, the app runs without a media volume and the link job no-ops until you add a mount.

## Media configuration

**Single root (movies and TV under one path):**
```yaml
media:
  mountPath: /media
  existingClaim: ""   # or set to your PVC name
  volumeSpec:
    nfs:
      server: 172.16.11.246
      path: /mnt/media
```

**Separate TV/movies (use existingClaim or volumeSpec for the path that contains both):**
```yaml
media:
  mountPath: /media
  existingClaim: media-pvc
```

Then configure Sonarr/Radarr root paths and `DOCKER_MEDIA_PATH` / `MEDIA_ROOT` to match (e.g. `/media`).

## Install

```bash
helm install plex-linker ./deploy/helm -n plex-linker --create-namespace -f my-values.yaml
```

Create a Secret with API keys and `DATABASE_URL` (or use External Secrets / 1Password). See chart values for `secrets.existingSecret` and `secrets.externalSecrets`.
