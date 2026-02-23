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

From this directory:

```bash
helm dependency update
helm install tautulli . -n media-server --create-namespace
```

### Upgrade

```bash
helm upgrade tautulli . -n media-server
```

### Uninstall

```bash
helm uninstall tautulli -n media-server
# PVCs are retained; delete manually if desired.
kubectl delete pvc -n media-server -l app.kubernetes.io/instance=tautulli
```

---

## Values layout

All app-template options are nested under the `tautulli` key in `values.yaml` (subchart alias matches chart name). The rest comes from [app-template / common-library](https://bjw-s-labs.github.io/helm-charts/docs/common-library/) defaults.

| Key | Purpose |
|-----|--------|
| `tautulli.controllers.tautulli` | Deployment strategy, annotations (e.g. Reloader). |
| `tautulli.containers.app` | Image, env, probes, resources, securityContext. |
| `tautulli.defaultPodOptions.securityContext` | runAsUser/fsGroup (568 for Plex ecosystem). |
| `tautulli.service.app` | Service port (8181). |
| `tautulli.ingress.main` | Host(s) `stats.expectedbehaviors.com`, `tautulli.expectedbehaviors.com`; path, TLS, className; external-dns annotation. |
| `tautulli.persistence` | config/cache/logs volumes and mounts. |

Override with `-f my-values.yaml` or `--set` when installing/upgrading.

---

## Upgrading the bjw-s app-template

The chart pins app-template in `Chart.yaml` (e.g. `4.6.2`). To upgrade:

1. Check [app-template upgrade instructions](https://bjw-s-labs.github.io/helm-charts/docs/app-template/upgrade-instructions/).
2. Bump the `version` under `dependencies` in `Chart.yaml`.
3. Run `helm dependency update`.
4. Run `helm upgrade` as needed.

---

## Troubleshooting

- **`helm template` reports "No containers enabled for controller (tautulli)":** Known quirk with app-template 4.6.2 and the tautulli-alias values layout. `helm install` / `helm upgrade` work correctly; use them or Argo CD to deploy.
- **Dependency update fails:** Run `helm repo add bjw-s https://bjw-s-labs.github.io/helm-charts/` and `helm repo update`.
- **Probe failures:** Tautulli serves `/status` on port 8181. If you change port or path, adjust `probes.*.spec.httpGet` in `values.yaml`.
- **Permission errors on volumes:** Values use runAsUser/fsGroup 568. For NFS/media GID (e.g. 65539), add `supplementalGroups` under `defaultPodOptions.securityContext` (see comments in `values.yaml`).
