# 🔐 Helm: removals, README standards, Mealie/Paperless-ngx/Gotify, Argo CD

## TL;DR

| What | Why safe | Proof |
|------|----------|--------|
| Remove rook-ceph & homelab-omni; add mealie, paperless-ngx, gotify charts; align READMEs to standard; wire Argo CD for new apps | Removals are unused; new charts follow bjw-s app-template; README/Argo CD changes are additive and documented | `helm template` passes for mealie, paperless-ngx, gotify; config.yaml and HELM_REVIEW updated |

## Summary

| Change | Description |
|--------|-------------|
| 🗑️ **Removals** | Removed **rook-ceph** and **homelab-omni** chart directories (not in use). Removed rook-ceph project block from Argo CD config; removed both from set-repo-descriptions.sh and HELM_REVIEW.md. |
| 📖 **README standard** | Updated **bazarr**, **gaps**, **kavita**, **komga**, **mylar** READMEs to README-STANDARD (Chart contents, Requirements, Key values, Render & validation, Argo CD, Next steps). **plex-linker** README rewritten with "Not active" note and placeholder sections. |
| 🍽️ **Mealie** | New chart (bjw-s app-template): recipe manager, meal planning, shopping lists. OIDC via nginx documented; security defaults (ALLOW_SIGNUP=false, non-root). |
| 📄 **Paperless-ngx** | New chart (bjw-s app-template): document management, OCR. External PostgreSQL via secret **paperless-db-credentials**; optional Redis; OIDC at ingress. |
| 🔔 **Gotify** | New chart (bjw-s app-template): self-hosted push notifications (REST API). OIDC at ingress; minimal resources. |
| 🔗 **Argo CD** | Added projects **mealie**, **paperless-ngx**, **gotify** in config.yaml; apps point at this repo with path `homelab/helm/mealie`, `homelab/helm/paperless-ngx`, `homelab/helm/gotify`. |
| 📋 **CHART_STANDARD / HELM_REVIEW** | CHART_STANDARD: build pipeline requirement for publishable subcharts; pre-merge checklist item; reference to after-merge-reconcile rule. HELM_REVIEW: flat-chart list updated (removed rook-ceph, homelab-omni; added mealie, paperless-ngx, gotify). |

## Setup requirements

- **Mealie / Gotify:** Create namespaces (or let Argo CD create); enable OIDC for ingress hosts (oauth2-proxy or nginx auth) when ready.
- **Paperless-ngx:** Create PostgreSQL database and user; create Kubernetes secret **paperless-db-credentials** (hostname, port, username, password, dbname) via 1Password/External Secrets before sync.

## Render & validation

| Check | Result |
|-------|--------|
| `helm template mealie . -f values.yaml -n mealie` | ✅ Pass |
| `helm template paperless-ngx . -f values.yaml -n paperless` | ✅ Pass |
| `helm template gotify . -f values.yaml -n gotify` | ✅ Pass |

(Charts use bjw-s app-template 4.6.2; `helm dependency update` run before template.)

## Why safe & correct

| Change | What we did | Why it's safe | Proof |
|--------|-------------|---------------|-------|
| Removals | Deleted rook-ceph, homelab-omni dirs; removed from config/scripts/docs | Neither chart was deployed (applications commented or absent) | config.yaml no longer references them; HELM_REVIEW updated |
| New charts | Mealie, Paperless-ngx, Gotify follow bjw-s pattern; persistence uses accessMode + readOnly | Same pattern as audiobookshelf/bazarr; schema-compliant | helm template succeeds for all three |
| Argo CD | New projects reference this repo (home) with path homelab/helm/<chart> | No existing apps overwritten; new apps sync only when enabled | config.yaml diff shows additive entries |
| READMEs | Added standard sections; no logic changes | Documentation only | No render impact |

## Next steps

- [ ] **Apply Argo CD config:** The mealie, paperless-ngx, gotify applications reference `path: homelab/helm/<chart>` and `sourceRepo: git@github.com:jd4883/home.git`. If your Argo CD config lives in another repo (e.g. `homelab/helm/core/argocd`), add the three projects and applications there from the same structure (see HELM_REVIEW.md).
- [ ] Apply Argo CD Terraform so new projects (mealie, paperless-ngx, gotify) exist.
- [ ] For each new app: create namespace if needed; configure OIDC at ingress; (Paperless) create DB and secret; sync.
- [ ] **README / chart updates in other repos:** Bazarr, gaps, kavita, komga, mylar, and plex-linker README updates live in their respective chart repos (those dirs are separate git repos); apply the same README-STANDARD there if desired.
- [ ] Optional: move charts to dedicated repos (e.g. jd4883/homelab-mealie) and set sourceRepo/path in config accordingly.
