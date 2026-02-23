# Helm chart (organizr-tab-controller)

Kubernetes deployment for **organizr-tab-controller**. Security-hardened defaults: non-root, no ingress, minimal surface. Based on [bjw-s app-template](https://bjw-s-labs.github.io/helm-charts/docs/app-template/); only the resources the controller needs are enabled.

## What this chart does

- **Deployment** – single controller container (image, env, resources, API key from Secret).
- **Service** – for pod selector/labels (controller does not serve HTTP).
- **RBAC** – ServiceAccount, ClusterRole, ClusterRoleBinding (watch Ingresses, Services, Deployments, StatefulSets, DaemonSets, Leases).
- **HPA** – optional horizontal pod autoscaling (default: **off**; set `hpa.enabled: true` for min 1, max 3).
- **No ingress, no persistence** – controller is cluster-internal and stateless.

## Requirements

- Kubernetes 1.28+
- **Organizr API URL** – set via values or `--set`.
- **Organizr API key** – in a Secret named `organizr-api-key` in the release namespace, with key `api-key` (or override env to use a different secret/key).

---

## Environment variables

The controller reads all settings from environment variables with the `ORGANIZR_` prefix. The chart sets a minimal set by default; override any via `organizr-tab-controller.controllers.main.containers.main.env` in values or `--set`.

| Variable | Required | Default (app) | Description |
|----------|----------|----------------|-------------|
| `ORGANIZR_API_URL` | **Yes** | — | Organizr base URL (e.g. `https://organizr.example.com`). Set on install. |
| `ORGANIZR_API_KEY` | Yes* | — | API key. Chart default: from Secret `organizr-api-key`, key `api-key`. |
| `ORGANIZR_API_KEY_FILE` | No | `/var/run/secrets/organizr/api-key` | Path to file containing API key (e.g. Secret mount). |
| `ORGANIZR_API_VERSION` | No | `v2` | Organizr API version: `v2` or `v1`. |
| `ORGANIZR_API_TIMEOUT` | No | `30` | HTTP timeout in seconds for API calls. |
| `ORGANIZR_SYNC_POLICY` | No | `upsert` | `upsert` (create/update only) or `sync` (create/update/delete). |
| `ORGANIZR_RECONCILE_INTERVAL` | No | `60` | Seconds between full reconciliation sweeps. |
| `ORGANIZR_WATCH_NAMESPACES` | No | (all) | Comma-separated namespaces to watch; empty = all. |
| `ORGANIZR_WATCH_RESOURCE_TYPES` | No | `ingresses,services,deployments,statefulsets,daemonsets` | Resource types to watch for annotations. |
| `ORGANIZR_ENABLE_LEADER_ELECTION` | No | `false` | Enable for HA (multiple replicas); reserved for future use. |
| `ORGANIZR_LEADER_ELECTION_NAMESPACE` | No | `default` | Namespace for leader-election Lease. |
| `ORGANIZR_LEADER_ELECTION_NAME` | No | `organizr-tab-controller-leader` | Name of the leader-election Lease. |
| `ORGANIZR_LOG_LEVEL` | No | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`. |
| `ORGANIZR_LOG_FORMAT` | No | `json` | `json` or `console`. |

*Either `ORGANIZR_API_KEY` (or the Secret referenced by the chart) or a valid file at `ORGANIZR_API_KEY_FILE` is required.

---

## Deploy with Helm

**1. Create namespace and API key secret** (if not already present):

```bash
kubectl create namespace organizr --dry-run=client -o yaml | kubectl apply -f -
kubectl create secret generic organizr-api-key -n organizr \
  --from-literal=api-key="YOUR_ORGANIZR_API_KEY" \
  --dry-run=client -o yaml | kubectl apply -f -
```

**2. Install the chart** (from repo root after `helm dependency update helm/`):

```bash
helm repo add bjw-s https://bjw-s-labs.github.io/helm-charts
helm dependency update helm/

helm install organizr-tab-controller ./helm -n organizr --create-namespace \
  --set organizr-tab-controller.controllers.main.containers.main.env.ORGANIZR_API_URL=https://organizr.example.com
```

**3. Upgrade:**

```bash
helm upgrade organizr-tab-controller ./helm -n organizr \
  --set organizr-tab-controller.controllers.main.containers.main.env.ORGANIZR_API_URL=https://organizr.example.com
```

With a values file (e.g. `my-values.yaml` that sets `organizr-tab-controller.controllers.main.containers.main.env.ORGANIZR_API_URL`):

```bash
helm install organizr-tab-controller ./helm -n organizr --create-namespace -f my-values.yaml
```

---

## Deploy with Argo CD

Use either **Option A** (Git repo + chart path) or **Option B** (Helm repo from GitHub Releases). In both cases, **provide valid credentials** as below; the examples use default chart values and only override what’s required.

### Prerequisites (both options)

1. **Namespace**  
   Create the target namespace if it doesn’t exist (e.g. `organizr`).

2. **Organizr API key**  
   Create a Secret in that namespace with the key the chart expects:
   ```bash
   kubectl create secret generic organizr-api-key -n organizr \
     --from-literal=api-key="YOUR_ORGANIZR_API_KEY"
   ```
   (Or use ExternalSecrets / your secret manager and ensure the secret name and key match.)

3. **Organizr API URL**  
   Set in the Application (see examples). Replace `https://organizr.example.com` with your Organizr base URL.

With that in place, the following examples work with default values.

---

### Option A: Git repo + Helm chart path

Argo CD pulls the repo and renders the chart from the `helm/` directory. Good for tracking a branch or tag; no separate Helm repo needed.

**1. Application manifest** – save as e.g. `argocd-organizr-tab-controller.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: organizr-tab-controller
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/expectedbehaviors/organizr-tab-controller.git
    targetRevision: main
    path: helm
    helm:
      valueFiles:
        - values.yaml
      parameters:
        - name: organizr-tab-controller.controllers.main.containers.main.env.ORGANIZR_API_URL
          value: "https://organizr.example.com"
  destination:
    server: https://kubernetes.default.svc
    namespace: organizr
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**2. Apply:**

```bash
kubectl apply -f argocd-organizr-tab-controller.yaml
```

**3. Optional overrides** (image, log level, etc.) – add under `source.helm.parameters`, for example:

```yaml
        - name: organizr-tab-controller.controllers.main.containers.main.image.tag
          value: "v0.1.0"
        - name: organizr-tab-controller.controllers.main.containers.main.env.ORGANIZR_LOG_LEVEL
          value: "DEBUG"
```

**Private repo:** set `source.repoURL` to your SSH or HTTPS URL and configure Argo CD credentials (Repository credentials or SSH key) so it can clone the repo.

---

### Option B: Helm repo (chart from GitHub Releases)

Use this when you consume the chart from a Helm repo (e.g. one built from GitHub Release assets). The chart is installed by name and version; you still need the same Secret and namespace.

**1. Add the Helm repo** (if your releases are published as a repo, e.g. GitHub Pages):

```bash
helm repo add organizr-tab-controller https://expectedbehaviors.github.io/organizr-tab-controller/
helm repo update
```

**2. Application manifest** – reference the chart and set required values:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: organizr-tab-controller
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://expectedbehaviors.github.io/organizr-tab-controller/
    chart: organizr-tab-controller
    targetRevision: "0.1.0"
    helm:
      values: |
        fullnameOverride: organizr-tab-controller
        rbac:
          create: true
        hpa:
          enabled: false
        organizr-tab-controller:
          global:
            fullnameOverride: organizr-tab-controller
          controllers:
            main:
              containers:
                main:
                  env:
                    ORGANIZR_API_URL: "https://organizr.example.com"
  destination:
    server: https://kubernetes.default.svc
    namespace: organizr
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**3. Apply:**

```bash
kubectl apply -f argocd-organizr-tab-controller-helm-repo.yaml
```

Replace `repoURL` and `targetRevision` with your actual Helm repo URL and chart version. The API key still comes from the `organizr-api-key` Secret (default values); ensure that Secret exists in the `organizr` namespace.

---

## Chart layout

- **Chart.yaml** – bjw-s app-template dependency (alias `organizr-tab-controller`).
- **values.yaml** – security defaults, single controller, no ingress/persistence, HPA off by default, RBAC.
- **templates/** – ServiceAccount, ClusterRole, ClusterRoleBinding (when `rbac.create`), HPA (when `hpa.enabled`).

Full tool docs and annotations: [root README](../README.md).
