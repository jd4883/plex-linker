# Gotify (homelab)

Gotify — self-hosted push notification server with REST API and WebSocket. Uses **bjw-s app-template**. **Managed by Argo CD.** Auth via **OIDC at ingress** (nginx + oauth2-proxy) so the app is not publicly open.

---

## Chart contents

- **App:** Gotify (gotify/server) via bjw-s app-template; port 80.
- **Secrets:** None required for basic run. Optional: secret for `GOTIFY_DEFAULTUSER_PASS` to set default admin password.
- **Ingress:** Host/path and TLS; enable OIDC at ingress.
- **Persistence:** Single PVC for `/app/data` (SQLite DB, app config).

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **PVC** | Chart creates **data** PVC (default 1Gi); or set `existingClaim`. |
| **Namespace** | e.g. `gotify`; create or use Argo CD project. |
| **OIDC** | Configure nginx ingress auth (oauth2-proxy) for this host. |

---

## Setup and configuration

1. **OIDC:** Enable auth at ingress (e.g. `nginx.ingress.kubernetes.io/enable-global-auth: "true"` or auth-url to oauth2-proxy). Same pattern as Mealie and Paperless-ngx (see **homelab/helm/oauth2-proxy** and edge ingress config).
2. **First run:** Default admin user is `admin`; set password on first login or provide `GOTIFY_DEFAULTUSER_PASS` via a Kubernetes secret (e.g. from 1Password) and add `envFrom: - secretRef: name: gotify-secrets` to the container.
3. **API tokens:** Create applications in the Gotify UI; use the token in scripts, Home Assistant, or CI/CD to send notifications (e.g. `curl -X POST "https://gotify.expectedbehaviors.com/message?token=..." -d "title=Alert&message=..."`).

---

## Key values

| Area | Where | What to set |
|------|--------|-------------|
| Persistence | `gotify.persistence.data` | size, storageClass, or existingClaim. |
| Ingress | `gotify.ingress.main.hosts` | Host and TLS for your domain. |
| Default password | Optional secret `gotify-secrets` with key `GOTIFY_DEFAULTUSER_PASS` | Set via envFrom if desired. |

---

## Render & validation

> `helm template gotify . -f values.yaml -n gotify`

Chart lints and templates successfully. Run `helm dependency update` first.

---

## Argo CD

Application is defined in **config.yaml** (Argo CD Terraform). Project **gotify** points at this chart. Namespace typically `gotify`.

---

## Next steps

- [ ] Enable OIDC at ingress for this host.
- [ ] Deploy; log in and create applications/tokens for notifications.
- [ ] Integrate with scripts, Home Assistant, or Argo CD notifications (e.g. Gotify notifier).
