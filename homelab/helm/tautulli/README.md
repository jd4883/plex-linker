# Tautulli Helm Chart

Tautulli (Plex statistics and monitoring) deployed via the [bjw-s app-template](https://bjw-s-labs.github.io/helm-charts/docs/app-template/) chart. Thin wrapper with Tautulli-specific defaults. **Managed by Argo CD** when deployed from repo.

---

## Chart contents

- **App:** Tautulli container (strategy Recreate, custom probes on `/status`, runAsUser/fsGroup 568).
- **Secrets:** None in chart; optional Reloader annotation for ConfigMap/Secret roll.
- **Persistence:** Config via **existingClaim** `tautulli-config`; cache/logs emptyDir.
- **Ingress:** Optional; values include host examples and external-dns annotation.

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **PVC** `tautulli-config` | Create in Longhorn (e.g. 1Gi, RWO); config volume. |
| **Namespace** | e.g. `media-server` (or `--create-namespace`). |
| bjw-s Helm repo | For dependency; `helm repo add bjw-s https://bjw-s-labs.github.io/helm-charts`. |

---

## Persistence

Config uses **existingClaim** `tautulli-config`. **Volumes are defined in Longhorn** — create the PVC `tautulli-config` there (e.g. 1Gi, RWO). Cache and logs use emptyDir.

## Argo CD

Deploy via Argo CD. Example Application (adjust repo/path/namespace to your layout):

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: tautulli
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/jd4883/homelab-tautulli
    path: .
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: media-server
  syncPolicy:
    automated: { prune: true, selfHeal: true }
```

## Usage

From this directory:

```bash
helm dependency update
helm install tautulli . -n media-server --create-namespace
```

---

## Render & validation

> `helm template tautulli . -f values.yaml -n media-server`

*(Note: app-template 4.6.2 may report "No containers enabled" for `helm template` with alias layout; `helm install` / Argo CD work correctly.)*

---

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

## Next steps

- [ ] Create PVC `tautulli-config` in Longhorn (namespace `media-server` or target ns).
- [ ] Run `helm dependency update` then install or deploy via Argo CD.
- [ ] Set ingress host and TLS if exposing; override TZ if needed.

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
- **TZ:** Set to `US/Pacific` in values; override to match your homelab.
