# Unpackerr

Unpackerr runs as a daemon that extracts completed downloads for Radarr, Sonarr, Lidarr, and Readarr, and (with the **unstable** image) **splits single-file FLAC+CUE albums** for Lidarr so they can be imported as separate tracks. This chart wraps the [bjw-s app-template](https://github.com/bjw-s-labs/helm-charts/tree/main/charts/other/app-template) and uses the **same download paths** as the Lidarr chart so extraction and CUE splitting see the same files. **Managed by Argo CD** (when the Application is enabled).

---

## Chart contents

- **App:** Unpackerr (image `golift/unpackerr`, tag `unstable` for CUE splitting; see [Unpackerr #141](https://github.com/Unpackerr/unpackerr/issues/141) and [unstable builds](https://unstable.golift.io/unpackerr)).
- **Secrets:** Kubernetes secret **`unpackerr`** (envFrom) from 1Password via **onepassworditem** (chart dependency) or central **onepassword-secrets**. 1Password item `vaults/Kubernetes/items/unpackerr`; field names = secret keys (e.g. `UN_LIDARR_0_API_KEY`, `UN_RADARR_0_API_KEY`).
- **Reloader:** Optional annotation `secret.reloader.stakater.com/reload: "unpackerr"` so the pod restarts when the secret changes.
- **Persistence:** Config PVC (`/config`) and shared download PVCs (same as Lidarr: qbittorrent-*-downloads, sabnzbd-downloads) mounted under `/downloads`.

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **Secret `unpackerr`** | Same namespace as release. Chart creates **OnePasswordItem** CR from item `vaults/Kubernetes/items/unpackerr` (onepassworditem); or add **unpackerr** to **onepassword-secrets** values for central sync. Secret keys = env var names: `UN_LIDARR_0_API_KEY`, `UN_RADARR_0_API_KEY`, etc. |
| **Download PVCs** | Same as Lidarr: `qbittorrent-anime-public-downloads`, `qbittorrent-anime-private-downloads`, `qbittorrent-private-downloads`, `qbittorrent-public-downloads`, `sabnzbd-downloads`. Must exist in release namespace (e.g. replicated into `unpackerr`). |
| **Namespace** | **`unpackerr`** (Argo CD project name = namespace). *arr URLs in values use in-cluster DNS: `lidarr.lidarr.svc.cluster.local`, `radarr.radarr.svc.cluster.local`, etc. |
| **Lidarr (and *arrs)** | Unpackerr polls *arr APIs at URLs in values (defaults: `http://lidarr.lidarr.svc.cluster.local:8686`, etc.). Ensure *arr apps are deployed in their project namespaces (lidarr, radarr, sonarr, readarr). |

---

## Setup and configuration

1. **1Password item** `vaults/Kubernetes/items/unpackerr`: add fields whose **names** are the env var names (e.g. `UN_LIDARR_0_API_KEY`, `UN_RADARR_0_API_KEY`). Values = API keys from each *arr (Settings → General). The chart’s **onepassworditem** dependency creates a OnePasswordItem CR so the operator syncs this to secret **`unpackerr`** in the release namespace. Alternatively, add **unpackerr** to **onepassword-secrets** values for central sync.
2. **Download PVCs** must exist in namespace **unpackerr** (same names as qBittorrent/SABnzbd; use Kubernetes Replicator or create them). Adjust `unpackerr.persistence.downloads-*` in values if your claim names differ.
3. **URLs** in values default to `lidarr.lidarr.svc.cluster.local`, `radarr.radarr.svc.cluster.local`, etc. (Argo CD project = namespace). Override if your *arr services use different namespaces or names.
4. **CUE splitting:** Requires image tag **unstable** (default). Set `unpackerr.controllers.main.defaultContainerOptions.image.tag` to a stable version (e.g. `0.14.0`) if you do not need FLAC+CUE splitting.

---

## Key values

| Area | Where | What to set |
|------|--------|-------------|
| **Lidarr** | `unpackerr.controllers.main.containers.main.env` | `UN_LIDARR_0_URL`, `UN_LIDARR_0_PATHS_0`, `UN_LIDARR_0_SPLIT_FLAC` (defaults: in-cluster URL, `/downloads`, `true`). |
| **API keys** | Secret **`unpackerr`** | `UN_LIDARR_0_API_KEY` (required for Lidarr); `UN_RADARR_0_API_KEY`, etc., for other apps. |
| **Image** | `unpackerr.controllers.main.defaultContainerOptions.image` | `tag: unstable` for CUE splitting; use a version tag for stable-only. |
| **Config PVC** | `unpackerr.persistence.config` | `size`, `storageClass`; disable if you do not need persistent config. |
| **Download mounts** | `unpackerr.persistence.downloads-*` | `existingClaim` must match your qBittorrent/SABnzbd PVC names. |

---

## Render & validation

> `helm dependency update && helm template unpackerr . -f values.yaml -n unpackerr`

Chart lints and templates successfully. Run from the chart directory (`homelab/helm/unpackerr`).

---

## Argo CD

The **unpackerr** project is defined in `homelab/helm/core/argocd/terraform/argocd-config/configs/config.yaml` (monorepo):

- **path:** `homelab/helm/unpackerr`
- **sourceRepo:** `git@github.com:jd4883/home.git` (or the repo that contains homelab/)
- **namespace:** `unpackerr` (project name = destination namespace)

Ensure the **`unpackerr`** secret (from 1Password) and download PVCs exist in namespace **unpackerr** before sync. Add **unpackerr** to **onepassword-secrets** values so the secret is synced into the unpackerr namespace.

---

## Next steps

- [ ] Create secret **`unpackerr`** with `UN_LIDARR_0_API_KEY` (and other *arr API keys if used).
- [ ] Create or confirm download PVCs (same as Lidarr).
- [ ] Deploy with `helm install` or Argo CD; confirm Unpackerr pod is running and logs show polling Lidarr.
- [ ] For CUE splitting: use image tag **unstable**; after a FLAC+CUE download completes, Unpackerr should split and Lidarr can import tracks. See [Lidarr issue #515](https://github.com/Lidarr/Lidarr/issues/515) and [Unpackerr #141](https://github.com/Unpackerr/unpackerr/issues/141). The Lidarr chart README in this repo also documents CUE splitting and Unpackerr.
