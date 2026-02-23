# Homelab Helm — Chart design, ArgoCD, volumes, Atlantis & improvements

Review of chart setups, design and consistency, documentation, ArgoCD mapping, shared volumes, repo unification (Atlantis), and security/operational/performance improvements. The **minimum working standard** for every chart (artifacts, PRs, deployment safety) is **CHART_STANDARD.md**; this doc expands on design choices, volume sharing, and ops.

---

## 1. Chart layout and consistency

### 1.1 Directory patterns

| Pattern | Charts | Notes |
|--------|--------|--------|
| **Flat** (Chart.yaml at chart root) | oauth2-proxy, plex-autoskip, plex, longhorn, organizr, sabnzbd, immich, mylar, komga, kavita, gaps, audiobookshelf, home-assistant, reloader, nvidia-device-plugin, qbittorrent, external-secrets, onepassword-secrets, minio, bazarr, plex-linker, portainer, purelb, kubernetes-replicator, nginx, onepassword-connect, mealie, paperless-ngx, gotify | Single dir with Chart.yaml, values.yaml, optional templates/ |
| **Nested `helm/`** | nextcloud, atlantis, external-dns, prowlarr, radarr, readarr, sonarr, lidarr | Chart lives under `chart-name/helm/`; Argo CD `path` is often `helm` |

**Recommendation:** Keep existing patterns; when adding new charts, prefer **nested `helm/`** for charts that also ship Terraform (e.g. *arr) so repo layout is `chart/helm/` + `chart/terraform/`. Document the chosen pattern in README-STANDARD.md.

### 1.2 Chart.yaml and README bar

Per README-STANDARD.md and REVIEW_CONSISTENCY.md, every chart should have:

- **Chart.yaml:** `description`, `appVersion` (or note "N/A"), `keywords`, `home`, `sources` where applicable.
- **values.yaml:** Top comment (one-line summary + “See README for setup”).
- **README:** Title + one-line, Chart contents (bullets), Requirements table, Key values table, Render & validation (exact `helm template` command), Argo CD section if applicable, Next steps.

**Gaps:** Several charts still lack full Chart.yaml metadata or README “Chart contents”; apply the same bar as oauth2-proxy/plex-autoskip styling pass across all charts.

### 1.3 Anti-affinity and HA

- **Multi-replica charts** (nextcloud, nginx, external-dns, kubernetes-replicator, external-secrets, reloader): Use `preferredDuringSchedulingIgnoredDuringExecution` podAntiAffinity so replicas spread across nodes.
- **plex-autoskip / plex (skip subchart):** Anti-affinity added when replicas > 1; plex skip uses podAffinity (colocate with Plex) + podAntiAffinity (spread skip pods).
- **sabnzbd ↔ qbittorrent:** Hard anti-affinity so they do not share a node (I/O contention); qbittorrent instances use soft anti-affinity to spread.

**Recommendation:** For any new stateful or I/O-heavy chart, document in README whether single-replica is intentional or HA is supported and what affinity is set.

---

## 2. ArgoCD mapping

### 2.1 Where it lives

- **Single source of truth:** `homelab/helm/core/argocd/terraform/argocd-config/configs/config.yaml`
- **Terraform:** `homelab/helm/core/argocd/terraform/argocd-config/` (modules/project) creates Argo CD Projects and Applications from that YAML. No Application/ApplicationSet manifests in git; all mapping is Terraform-driven.
- **Path logic:** For each application, `path` is either the explicit `path` in config or `{default_path_prefix}/{project_name}/{chart}`. Each app points to a **separate git repo** (`sourceRepo`); the path is inside that repo (e.g. `helm` for external-dns, atlantis, prowlarr; `.` for flat charts).

### 2.2 Chart ↔ ArgoCD alignment

**Charts with Applications (deployed):**  
cluster-tools (kubernetes-dashboard, reloader, kubernetes-replicator, external-secrets, onepassword-connect, onepassword-secrets), portainer, audiobookshelf, cert-manager (cert-manager, certificates), edge (purelb, nginx, external-dns, oauth2-proxy), external-services (ipmi-fan-control, external-services-dns), home-assistant, kube-system (tunnel-interface), komga, mylar, prowlarr, qbittorrent, sabnzbd, nvidia (nvidia-device-plugin), organizr, atlantis, longhorn.

**Charts/projects with no Application (applications: [] or commented):**  
kavita, lidarr, radarr, readarr, sonarr, plex, immich, nextcloud, gaps, ombi, tautulli, minio.

**Recommendations:**

- **Document intent:** In config.yaml, keep comments for “NOT READY” (e.g. immich, nextcloud) and for disabled apps (e.g. plex, *arr) so it’s clear whether they’re off by choice or pending dependencies.
- **Plex:** When you enable plex, ensure `path` matches the repo layout. If the plex repo is flat, use `path: "."`; if it moves to `plex/helm`, use `path: helm`. Same for plex-autoskip if ever deployed as a standalone app.
- **Single source of repo paths:** Consider a small table in README or in this doc: “Repo layout → path” (e.g. `homelab-oauth2-proxy` → `.`, `homelab-external-dns` → `helm`) so new charts are added consistently.

---

## 3. Shared volumes (Plex ecosystem and others)

### 3.1 Intended sharing

| Consumer | Shared PVCs / volumes | Notes |
|----------|------------------------|--------|
| **plex + autoscan** (subchart) | Same media PVCs (e.g. `plex-movies-anime`, `plex-anime-one-pace`, `plex-tv-*`, etc.) | Autoscan and Plex use identical `existingClaim` names and paths; safe as long as both are in same umbrella chart or same namespace and PVCs exist. |
| **plex one-pace-plex-assistant** (in plex chart) | `plex-anime-one-pace`, `sabnzbd-downloads` | Same namespace; PVCs must exist and be created once (e.g. by storage layer or bootstrap). |
| **plex-autoskip** (standalone) | Own config PVC only | Optional: override to use `existingClaim: plex-config` if you want one config volume; document RWO and single-writer. |
| **plex-linker** | `plex-linker-config`; media via NFS | No shared PVC with Plex media. |

### 3.2 Practices for shared volumes

- **Single writer:** For any PVC shared between apps, ensure only one workload writes (e.g. Plex writes config; autoscan/one-pace read or write only where designed). Avoid multiple pods writing to the same path.
- **Access mode:** Shared media PVCs are typically ReadOnlyMany or ReadWriteOnce with one writer; document in each chart README which PVCs are shared and with whom.
- **Naming:** Use stable, explicit names (e.g. `plex-config`, `plex-movies-anime`) in values and document them in the umbrella chart (plex) README so operators know what to create and what is shared.
- **Bootstrap:** Document in a single place (e.g. plex README or ops runbook) which PVCs must exist before deploying Plex/autoscan/one-pace and who creates them (Terraform, manual, or Longhorn/StorageClass).

**Recommendation:** Add a short “Shared volumes” subsection to `homelab/helm/plex/README.md` that references this table and the “single writer / access mode” rules.

---

## 4. Atlantis and Terraform repo unification

### 4.1 Current state

- **Root `atlantis.yaml`** (repo root): All active Terraform is configured here:
  - **Argo CD:** `helm-argocd-config` → `homelab/helm/core/argocd/terraform/argocd-config`
  - **external-dns:** `helm-external-dns` → `homelab/helm/core/external-dns/terraform`
  - **\*arr Terraform (configuration):** prowlarr, lidarr, sonarr, radarr, readarr each have a project pointing at `homelab/helm/<chart>/terraform`; configuration for all of them is driven via this single atlantis.yaml.
  - **Other:** `homelab-networking`, `homelab-secrets-terraform-identity-generator`
- **homelab/domain-mgmt/atlantis.yaml:** Project `digitalocean_root_records`, dir `terraform/root-records` (domain-mgmt may be a separate repo or submodule).
- **docker-kubernetes-terraform:** One atlantis.yaml under `production/instantiations/dns/digital_ocean/root_records/`.

**Not in Atlantis (archived/unused):** The following Terraform dirs are no longer used; they can stay in git, be archived, or deleted locally. No Atlantis projects are defined for them:

- `homelab/terraform/avi/`
- `homelab/terraform/kubernetes-cluster/`
- `homelab/vmware-vcenter/`
- `homelab/vmware-tanzu-cluster/`
- `homelab/vmware-vcf/`

---

## 5. Security improvements

- **Secrets:** Continue using 1Password / External Secrets; avoid plain values in values.yaml. Document required 1Password items and ClusterExternalSecret/Secret names in each chart README.
- **RBAC:** Charts that create ServiceAccounts (e.g. external-dns, reloader) should use least-privilege roles; audit any cluster-admin or broad permissions.
- **Pod security:** Many namespaces use `pod-security.kubernetes.io/enforce: privileged` for legacy or device access. Plan a path to restricted/baseline where possible (e.g. isolate GPU/workloads that need privileged in dedicated namespaces).
- **Images:** Prefer digest-based or pinned tags in values; document in README. Consider a policy (e.g. OPA/Gatekeeper or image scanner) to block untrusted registries or outdated bases.
- **Network:** Use NetworkPolicies where feasible (e.g. restrict ingress to only oauth2-proxy or nginx, limit egress to needed endpoints). Document in chart README if a chart assumes a default “allow all” and what would be needed to lock it down.

---

## 6. Operational improvements

- **Health and sync:** Ensure every deployed app has correct `ignoreDifferences` where Argo CD diff is noisy (e.g. Secret data, volumeClaimTemplates, env from downward API). Keep `syncPolicy.automated.selfHeal` disabled only where intentional (e.g. qbittorrent) and document why.
- **Backups:** Document which namespaces/PVCs need backup (e.g. plex config, *arr configs, nextcloud data) and whether Velero or another mechanism is in use.
- **Dependencies:** In config.yaml and READMEs, document ordering where needed (e.g. cert-manager → certificates → ingress; onepassword-connect before apps that use 1Password).
- **Runbooks:** Link or add a one-pager for “new chart onboarding”: create repo, add to config.yaml with correct path/sourceRepo, add Atlantis project if Terraform, update this review doc.

---

## 7. Performance improvements

- **Node placement:** Affinity/anti-affinity are already used for HA and to separate sabnzbd/qbittorrent; extend to other I/O-heavy or GPU workloads so they don’t crowd the same node.
- **Resources:** Set requests/limits on all charts; avoid unbounded CPU/memory so the scheduler and autoscaler can work. Document in README or values comments for large apps (e.g. Plex, nextcloud).
- **Storage:** Use appropriate StorageClasses (e.g. Longhorn for HA, local or fast SSD where latency matters). Document in chart README which StorageClass or PVC names are expected.
- **Helm:** For charts with many value files, keep `value_files` in Argo CD minimal and override only what’s needed; avoid duplicating large blocks so `helm template` stays fast and diffs clear.

---

## 8. Summary checklist

| Area | Action |
|------|--------|
| **Charts** | Meet **CHART_STANDARD.md** (Chart.yaml, values comment, README per README-STANDARD; PR bar; deployment safety). |
| **ArgoCD** | Keep config.yaml as single source; document path vs repo layout; add “Shared volumes” to plex README. |
| **Volumes** | Document shared PVCs and single-writer rules; ensure bootstrap/PVC creation is documented. |
| **Atlantis** | Active Terraform (Argo CD, external-dns, *arr, homelab-networking, secrets) in root atlantis.yaml; unused dirs (avi, kubernetes-cluster, vmware-*) left out. |
| **Security** | 1Password/External Secrets; audit RBAC and pod security; pin images; consider NetworkPolicies. |
| **Ops** | ignoreDifferences, backup strategy, dependency order, runbook for new charts. |
| **Performance** | Affinity, resource requests/limits, StorageClass expectations. |

This document should be updated when adding new charts, new Terraform roots, or when changing shared-volume or ArgoCD layout.
