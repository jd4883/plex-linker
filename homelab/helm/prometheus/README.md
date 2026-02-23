# Prometheus (kube-prometheus-stack)

Helm chart wrapping **kube-prometheus-stack** (Prometheus Operator) with Prometheus, Alertmanager, Grafana, node-exporter, and kube-state-metrics. Configured for **HA**: multiple replicas, PDBs, soft pod anti-affinity, **Longhorn HDD** storage (metrics do not require SSD). **Namespace: observability.** Grafana uses **anonymous auth** behind **nginx global auth**; TLS via **cert-manager** (passive). **Managed by Argo CD** when enabled.

---

## Chart contents

- **Prometheus Operator:** Manages Prometheus, Alertmanager, ServiceMonitors, PrometheusRules.
- **Prometheus:** 2 replicas, 15d retention, Longhorn HDD 50Gi, PDB, soft anti-affinity.
- **Alertmanager:** 2 replicas, per-replica services for HA, Longhorn HDD 10Gi, PDB, soft anti-affinity.
- **Grafana:** 2 replicas, Longhorn HDD 10Gi, ingress (nginx), **anonymous auth** (login form disabled; nginx global auth protects UI), TLS from cert-manager.
- **Node exporter / kube-state-metrics:** Enabled (DaemonSet / Deployment).
- **Secrets:** Grafana admin from 1Password (item **grafana**, fields **username** + **password**) → secret **grafana-admin** for Terraform/API.
- **Ingress:** Grafana only; cert-manager annotation for TLS (ClusterIssuer).

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **Namespace** | **observability** (or override on install). |
| **StorageClass** | **hdd** (Longhorn HDD; mechanical is fine for metrics). Ensure Longhorn has an `hdd` StorageClass (e.g. from `longhorn/values/volumes.yaml`). |
| **cert-manager** | ClusterIssuer (e.g. `letsencrypt-prod`) for Grafana ingress TLS. Set `kube-prometheus-stack.grafana.ingress.annotations["cert-manager.io/cluster-issuer"]` if different. |
| **nginx** | Ingress controller with **global auth**; Grafana is protected by nginx, not Grafana login. |

---

## 1Password — Grafana admin (required for Terraform / API)

The chart syncs Grafana admin credentials from 1Password into the **grafana-admin** secret so the Grafana API can be used by Terraform (dashboards, datasources, etc.). The UI remains anonymous behind nginx global auth.

### Create this 1Password item

| What | Value |
|------|--------|
| **Item name** | **grafana** (or set `externalSecrets.grafana.itemTitle` to match your item title) |
| **Vault** | Any vault that 1Password Connect can read (e.g. **Kubernetes** or **Monitoring**) |
| **Item type** | Login or Secure Note; any type with two custom fields is fine |

### Required fields (exact labels)

| Field label in 1Password | Purpose | Example |
|--------------------------|---------|--------|
| **username** | Grafana admin username (API and future login) | `admin` or your choice |
| **password** | Grafana admin password | Strong password (see below) |

Field names are case-sensitive. The chart maps them to the Kubernetes secret keys `admin-user` and `admin-password` that the Grafana Helm chart expects. If you use different 1Password property names, set `externalSecrets.grafana.usernameProperty` and `externalSecrets.grafana.passwordProperty` in values.

### Password length and complexity

- **Grafana minimum:** **4 characters** (no complexity enforced by default).
- **Recommended for API/Terraform:** **At least 16 characters**, with mixed case, numbers, and symbols, so the credential is safe for automation.
- **If you enable Grafana strong password policy later** (`auth.basic.password_policy = true`): then the password must have at least 12 characters, one special character, one number, one lowercase, and one uppercase.

Create the **grafana** item with **username** and **password** before deploying (or before first sync). External Secrets Operator will create the **grafana-admin** secret in the **observability** namespace; Reloader will restart Grafana pods when the secret changes.

### Optional: Alertmanager

| 1Password item | Purpose |
|----------------|---------|
| **alertmanager** (or **monitoring**) | SMTP credentials or **slack_webhook_url** for Alertmanager receivers. Create when you configure alerting. |

---

## Setup and configuration

1. Ensure **Longhorn** has an **hdd** StorageClass (or change `storageClassName` in values to your mechanical tier).
2. Create namespace: `kubectl create namespace observability`.
3. Set **cert-manager** ClusterIssuer in Grafana ingress annotations if not `letsencrypt-prod` (see Key values).
4. Grafana host: default `grafana.expectedbehaviors.com`; change `kube-prometheus-stack.grafana.ingress.hosts` if needed.
5. Create the **grafana** 1Password item (username + password) before first deploy so the grafana-admin secret exists; see 1Password section above.

---

## Key values

| Area | Where in values | What to set |
|------|------------------|-------------|
| **Namespace** | Install/Argo: `-n observability` | Default namespace for this stack. |
| **Grafana ingress** | `kube-prometheus-stack.grafana.ingress` | `hosts`, `annotations["cert-manager.io/cluster-issuer"]` (default `letsencrypt-prod`), `tls[0].secretName`. |
| **Grafana auth** | `kube-prometheus-stack.grafana.grafana.ini` | Currently anonymous + `disable_login_form`; nginx global auth. For future login: set `existingSecret` and disable anonymous. |
| **Storage** | `prometheusSpec.storageSpec`, `alertmanagerSpec.storage`, `grafana.persistence` | `storageClassName: hdd`, sizes 50Gi / 10Gi / 10Gi. |
| **Prometheus retention** | `kube-prometheus-stack.prometheus.prometheusSpec.retention` | Default `15d`. |

---

## Render & validation

> `helm dependency update && helm template prometheus . -f values.yaml -n observability`

Chart lints and templates successfully. Use the same value file and namespace in Argo CD.

---

## Argo CD

Application is typically defined in the central Argo CD config. Use **path** to this chart, **namespace** **observability**, and value file `values.yaml`. Ensure the **observability** project/namespace exists and is allowed to create PVCs (Longhorn **hdd**).

---

## Terraform (Grafana dashboards / provisioning)

**You need auth for Terraform.** The Grafana Terraform provider (dashboards, datasources, folders, etc.) talks to the Grafana **API**, which requires authentication (admin user or service-account token). With **anonymous-only** and no admin credentials, the API is not usable by Terraform.

**Recommended approach:** Keep the **UI** as-is (anonymous + no login form, nginx global auth), but give Grafana **admin credentials from a secret** so the API can be used:

1. Create the **grafana** 1Password item with fields **username** and **password** (see 1Password section).
2. Add External Secrets (or onepassworditem) to sync it into the **observability** namespace (e.g. secret name `grafana-admin`).
3. In values set `kube-prometheus-stack.grafana.existingSecret: grafana-admin` (and the key the Grafana chart expects, e.g. `admin-password`).
4. Leave `grafana.ini.auth.anonymous.enabled: true` and `auth.disable_login_form: true` so the **browser** still sees anonymous-only; nginx continues to protect the UI.
5. Terraform (or any automation) uses the **same admin credentials** (or a Grafana service-account token created with that admin) to call the Grafana API and manage dashboards.

So: **no login form for users**, but **API auth for Terraform**. If you prefer zero admin credentials, Terraform cannot manage Grafana; you’d manage dashboards manually or via Grafana’s config-based provisioning (ConfigMaps) only.

---

## Roadmap (auth)

- **Now:** Grafana UI protected by **nginx global auth** only; Grafana anonymous auth, login form disabled. Same idea can apply to Nextcloud (global auth in front, minimal app-level auth). For **Terraform** dashboard provisioning, set admin via `existingSecret` (API-only; see above).
- **Later:** Add Grafana (and optionally Nextcloud) login: e.g. **LDAP tied to GitHub** (or OAuth) so you can invite others to view dashboards. When you do, create the **grafana** 1Password item, sync via External Secrets, set `grafana.existingSecret`, and turn off anonymous / re-enable login form in `grafana.ini`.

---

## How it all goes together (checklist)

| Piece | Status / action |
|-------|------------------|
| **Chart** | `homelab/helm/prometheus` (values under `kube-prometheus-stack`). |
| **Namespace** | **observability** — create if not present (`kubectl create ns observability`). |
| **StorageClass** | Longhorn **hdd** — must exist (e.g. from `longhorn/values/volumes.yaml`). |
| **Argo CD** | **observability** project + **prometheus** application in `config.yaml` — points at this chart’s repo/path; destination namespace **observability**. |
| **cert-manager** | ClusterIssuer (e.g. `letsencrypt-prod`) for Grafana ingress TLS; annotation on ingress. |
| **nginx** | Global auth enabled; Grafana ingress is protected by nginx. |
| **Grafana auth** | Anonymous + no login form for UI. For Terraform: set admin via `existingSecret` (API-only). |
| **1Password** | **grafana** item (username + password) required; synced to **grafana-admin** for Terraform/API. |

If the chart lives in a **monorepo** (e.g. this `home` repo) instead of `homelab-prometheus`, set the Argo CD application `sourceRepo` to that repo and `path: homelab/helm/prometheus`.

---

## Next steps

- [ ] Create namespace **observability** if not present.
- [ ] Ensure StorageClass **hdd** exists (Longhorn).
- [ ] Confirm cert-manager ClusterIssuer name and set on Grafana ingress if not `letsencrypt-prod`.
- [ ] Create 1Password item **grafana** with fields **username** and **password** (see 1Password section above).
- [ ] Add Application to Argo CD (namespace **observability**, path to this chart, `values.yaml`).
- [ ] Optional: configure Alertmanager receivers (Slack/email) and reference secrets when ready.
