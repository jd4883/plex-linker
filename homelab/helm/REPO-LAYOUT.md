# Repo layout (canonical — do not forget between contexts)

- **Workspace path** may be named **home** (e.g. `~/Documents/Repositories/home`). That is a **folder name only**, not a GitHub repo. There is no repo named "home" or "jd4883/home".

- **`homelab/helm`** is the path where chart repos live. **Each chart is its own repo.** There is no monorepo. Naming: `jd4883/homelab-<chart>` (e.g. `jd4883/homelab-unpackerr`, `jd4883/homelab-mealie`, `jd4883/homelab-prometheus`). When working on a chart, the repo is that chart’s repo; Argo CD `config.yaml` uses `sourceRepo: git@github.com:jd4883/homelab-<chart>.git` and `path: "."`.

- **`homelab/helm/core`** is **one repo** (e.g. homelab-core) that contains **submodules**. Each submodule is its own repo. See `homelab/helm/core/.gitmodules`: cert-manager, external-dns, kubernetes-replicator, nginx, onepassword-connect, purelb, argocd.

- Scripts and automation: use the chart’s repo (e.g. `HOMELAB_REPO=jd4883/homelab-unpackerr`), never "home" or a monorepo.
