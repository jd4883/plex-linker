# Paperless-ngx (homelab)

Paperless-ngx — document management with OCR, tagging, and search. Uses **bjw-s app-template**; **external PostgreSQL**; auth via **OIDC at ingress**. **Managed by Argo CD.**

---

## Chart contents

- **App:** Paperless-ngx (ghcr.io/paperless-ngx/paperless-ngx) via bjw-s app-template; port 8000.
- **Secrets:** **paperless-db-credentials** (hostname, port, username, password, dbname) from 1Password or External Secrets.
- **Reloader:** Annotation to reload on secret change.
- **Ingress:** Host/path and TLS; enable OIDC at ingress (nginx + oauth2-proxy).
- **Persistence:** **data**, **media**, **consume** PVCs (or existingClaim).

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **PostgreSQL** | External DB (e.g. `postgresql-rw.postgresql.svc.cluster.local`). Create database and user for Paperless. |
| **Secret** | **paperless-db-credentials** with keys: `hostname`, `port`, `username`, `password`, `dbname`. Create via 1Password item + External Secrets or onepassworditem. |
| **Namespace** | e.g. `paperless`; create or use Argo CD project. |
| **OIDC** | Configure nginx ingress auth (oauth2-proxy) for this host. |

---

## Setup and configuration

1. **PostgreSQL:** Create database `paperless` and user; grant privileges. Use the same Postgres cluster as other apps (e.g. postgresql-rw.postgresql.svc.cluster.local).
2. **Secret:** Create 1Password item (e.g. **paperless-db**) with fields: hostname, port, username, password, dbname. Sync to Kubernetes as **paperless-db-credentials** via External Secrets or onepassworditem (see **immich** or **nextcloud** chart README for the same pattern).
3. **OIDC:** Enable auth at ingress (e.g. `nginx.ingress.kubernetes.io/enable-global-auth: "true"` or auth-url to oauth2-proxy) so Paperless is not publicly open.
4. **Redis (optional):** For Celery broker/cache, set env `PAPERLESS_REDIS` (e.g. `redis://redis-master.redis.svc.cluster.local:6379/0`).

---

## Key values

| Area | Where | What to set |
|------|--------|-------------|
| DB secret | `paperless-db-credentials` | Must exist in namespace; keys: hostname, port, username, password, dbname. |
| Persistence | `paperless.persistence.data/media/consume` | size, storageClass, or existingClaim. |
| Ingress | `paperless.ingress.main.hosts` | Host and TLS for your domain. |
| Redis | `paperless.controllers.main.containers.main.env.PAPERLESS_REDIS` | Optional; uncomment and set URL if using Redis. |

---

## Render & validation

> `helm template paperless-ngx . -f values.yaml -n paperless`

Chart lints and templates successfully. Run `helm dependency update` first. Ensure secret **paperless-db-credentials** exists (or mock for template-only).

---

## Argo CD

Application is defined in **config.yaml** (Argo CD Terraform). Project **paperless-ngx** points at this chart. Namespace typically `paperless`.

---

## Next steps

- [ ] Create Postgres database and user; create **paperless-db-credentials** secret.
- [ ] Enable OIDC at ingress for this host.
- [ ] Deploy; run migrations (Paperless does this on first start).
- [ ] Optionally configure Redis and Tika/Gotenberg for advanced features.
