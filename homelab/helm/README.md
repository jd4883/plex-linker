# Homelab Helm charts

Helm charts and Argo CD–deployed applications for the homelab.

**Repo layout (canonical):** The path `homelab/helm` is where chart repos live. **Each chart is its own repo** (no monorepo). Pattern: `jd4883/homelab-<chart>`. **`homelab/helm/core`** is one repo with **submodules** (each submodule is its own repo; see `core/.gitmodules`). The workspace folder may be named "home" — that is a folder name only, not a GitHub repo.

---

## Standard and quality

- **Start here:** [**CHART_STANDARD.md**](./CHART_STANDARD.md) — minimum working baseline for every chart (artifacts, PR descriptions, deployment safety). Use it so charts are deployed **consistently** and we **don’t brick functionality**.
- **READMEs:** [README-STANDARD.md](./README-STANDARD.md) — structure and template for chart READMEs.
- **Design and ops:** [HELM_REVIEW.md](./HELM_REVIEW.md) — Argo CD mapping, shared volumes, Atlantis, security/ops/performance.

New or updated charts should meet CHART_STANDARD.md and use the pre-merge checklist there before merge.

**Conventions for chart READMEs:** Each chart README should include (1) an **Argo CD** section with an example `Application` manifest (repo/path/namespace adjusted for that chart), and (2) where the chart uses persistent volumes, a note that **volumes are defined in Longhorn** (PVCs are created in Longhorn or via bootstrap, not necessarily by the chart).
