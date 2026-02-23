# Tautulli Helm Chart

Tautulli (Plex statistics and monitoring) deployed via the [bjw-s app-template](https://bjw-s-labs.github.io/helm-charts/docs/app-template/) chart. This chart is a thin wrapper that pins the app-template version and provides Tautulli-specific defaults aligned with this homelab.

**Why bjw-s app-template:** It is the de facto standard for single-container apps in home-lab Kubernetes; no dedicated Tautulli chart is more specific or better maintained (see [Kubesearch](https://kubesearch.dev/hr/ghcr.io-bjw-s-helm-app-template-tautulli)).

---

## Prerequisites

- Helm 3
- Kubernetes 1.28+
- `media-server` namespace (or use `--create-namespace`)
- bjw-s repo added (for dependency resolution):

```bash
helm repo add bjw-s https://bjw-s-labs.github.io/helm-charts/
helm repo update
```

---

## Usage

From `homelab/helm`:

```bash
cd tautulli
helm dependency update
helm install tautulli . -n media-server --create-namespace
```

From repo root:

```bash
helm dependency update homelab/helm/tautulli
helm install tautulli homelab/helm/tautulli -n media-server --create-namespace
```

### Upgrade

```bash
helm upgrade tautulli homelab/helm/tautulli -n media-server
```

### Uninstall

```bash
helm uninstall tautulli -n media-server
# PVCs are retained; delete manually if desired.
kubectl delete pvc -n media-server -l app.kubernetes.io/instance=tautulli
```

---

## Values layout

All app-template options are nested under the `app-template` key in `values.yaml`. The rest comes from [app-template / common-library](https://bjw-s-labs.github.io/helm-charts/docs/common-library/) defaults.

| Key | Purpose |
|-----|--------|
| `app-template.controllers.tautulli` | Deployment strategy, annotations (e.g. Reloader). |
| `app-template.containers.app` | Image, env, probes, resources, securityContext. |
| `app-template.defaultPodOptions.securityContext` | runAsUser/fsGroup (568 for Plex ecosystem). |
| `app-template.service.app` | Service port (8181). |
| `app-template.ingress.main` | Host(s) `stats.expectedbehaviors.com`, `tautulli.expectedbehaviors.com`; path, TLS, className; external-dns annotation. |
| `app-template.persistence` | config/cache/logs volumes and mounts. |

Override with `-f my-values.yaml` or `--set` when installing/upgrading.

---

## Upgrading the bjw-s app-template

The chart pins app-template in `Chart.yaml` (e.g. `4.6.2`). To upgrade:

1. Check [app-template upgrade instructions](https://bjw-s-labs.github.io/helm-charts/docs/app-template/upgrade-instructions/).
2. Bump the `version` under `dependencies` in `homelab/helm/tautulli/Chart.yaml`.
3. Run `helm dependency update homelab/helm/tautulli`.
4. Run `helm upgrade` as needed.

---

## Troubleshooting

- **Dependency update fails:** Run `helm repo add bjw-s https://bjw-s-labs.github.io/helm-charts/` and `helm repo update`.
- **Probe failures:** Tautulli serves `/status` on port 8181. If you change port or path, adjust `probes.*.spec.httpGet` in `values.yaml`.
- **Permission errors on volumes:** Values use runAsUser/fsGroup 568. For NFS/media GID (e.g. 65539), add `supplementalGroups` under `defaultPodOptions.securityContext` (see comments in `values.yaml`).
