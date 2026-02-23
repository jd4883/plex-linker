# Mealie (homelab)

Mealie — self-hosted recipe manager with meal planning, shopping lists, and API. Uses **bjw-s app-template**. **Managed by Argo CD.** Auth is handled at the ingress via **OIDC** (nginx + oauth2-proxy or nginx auth) so the app itself is not exposed without login.

---

## Chart contents

- **App:** Mealie (ghcr.io/mealie-recipes/mealie) via bjw-s app-template; port 9000.
- **Secrets:** None required for basic run; Mealie stores users in its own SQLite DB. Optional: External Secrets for env if you add them later.
- **Ingress:** Host/path and TLS as in values; **OIDC** should be enabled at ingress (see below).
- **Persistence:** Single PVC for `/app/data` (recipes, DB, uploads).

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **PVC** | Chart creates a **data** PVC (default 10Gi); or set `existingClaim` to use an existing one. |
| **Namespace** | e.g. `mealie`; create or use Argo CD project. |
| **OIDC / Auth** | Configure nginx ingress to require auth (oauth2-proxy or nginx auth snippet) so Mealie is not publicly open. See **Auth (OIDC) via nginx** below. |

---

## Setup and configuration

1. **Base URL:** Set `mealie.controllers.main.containers.main.env.BASE_URL` to your public URL (e.g. `https://mealie.expectedbehaviors.com`) so links and API docs work.
2. **Auth (OIDC) via nginx:** Mealie does not enforce auth by default. Use one of:
   - **oauth2-proxy (global auth):** In your nginx ingress config (or oauth2-proxy sidecar), enable global auth for the Mealie host so unauthenticated requests are redirected to the IdP. Set ingress annotation `nginx.ingress.kubernetes.io/enable-global-auth: "true"` if your edge uses that pattern (see [oauth2-proxy](https://github.com/oauth2-proxy/oauth2-proxy) and your homelab **oauth2-proxy** chart).
   - **nginx auth-url:** Use `nginx.ingress.kubernetes.io/auth-url` and `auth-signin` to point at your auth service (e.g. oauth2-proxy `https://auth.expectedbehaviors.com/oauth2/auth` and `/oauth2/start`). Same pattern as other apps in this homelab that sit behind OIDC.
3. **First user:** With signup disabled (`ALLOW_SIGNUP: "false"`), create the first user via the app’s initial setup flow (or enable signup temporarily, create user, then disable).
4. **API tokens:** For automation (e.g. grocery list sync), create API tokens in Mealie at **User profile → API tokens**. Use these in scripts or integrations (e.g. Home Assistant).

---

## Key values

| Area | Where | What to set |
|------|--------|-------------|
| Base URL | `mealie.controllers.main.containers.main.env.BASE_URL` | Public URL (e.g. `https://mealie.expectedbehaviors.com`). |
| Signup | `mealie.controllers.main.containers.main.env.ALLOW_SIGNUP` | `false` (recommended); set `true` only temporarily for first user. |
| Persistence | `mealie.persistence.data` | `size`, `storageClass`, or `existingClaim`. |
| Ingress | `mealie.ingress.main.hosts` | Host and TLS secret for your domain. |
| OIDC | Ingress annotations or nginx config | See **Auth (OIDC) via nginx** above. |

---

## Render & validation

> `helm template mealie . -f values.yaml -n mealie`

Chart lints and templates successfully. Run `helm dependency update` first.

---

## Argo CD

Application is defined in **config.yaml** (Argo CD Terraform). Project **mealie** points at this chart (repo/path as configured). Namespace typically `mealie`.

---

## Next steps

- [ ] Set **BASE_URL** and create **data** PVC (or existingClaim).
- [ ] Configure **OIDC at ingress** (oauth2-proxy or nginx auth) so Mealie is not public.
- [ ] Deploy; create first user; create API tokens for automation if needed.
- [ ] Optionally pin image tag for reproducibility.
