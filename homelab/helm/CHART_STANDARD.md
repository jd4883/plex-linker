# Homelab Helm chart standard — minimum working baseline

This is the **minimum working standard** for all homelab Helm charts. Use it as the bar to aspire to: every chart and every chart PR should meet it so we deploy **more consistently** and **never brick functionality**.

---

## 1. Purpose

- **Consistency** — Same structure (Chart.yaml, values, README, PRs) across charts so reviewers and operators know where to look.
- **Safety** — No merge without render proof; no behavior change without evidence or explicit equivalence; shared volumes and Argo CD path documented so nothing breaks in production.
- **Professional bar** — TL;DR, evidence tables, and a clear “why safe” story in every PR. No “trust me” without proof.

Treat this document as the single source of truth for “what good looks like.” Reference README-STANDARD.md for detailed README structure and the PR description rule for full PR format.

---

## 2. Chart artifacts (minimum bar)

Every chart **must** have the following before it is considered ready for consistent deployment.

| Artifact | Requirement |
|----------|-------------|
| **Chart.yaml** | `name`, `version`, `description` (one line). Prefer also: `appVersion`, `keywords`, `home`, `sources` where applicable (match nextcloud/atlantis/plex-autoskip). |
| **values.yaml** | Top-of-file comment: one-line summary of what the chart does + “See README for setup.” No silent breaking changes to default values without a major version or explicit callout. |
| **README** | Title + one-line; **Chart contents** (bullets: app, secrets, Reloader, ingress); **Requirements** (table: PVCs, secrets, 1Password items, namespace); **Key values** (table); **Render & validation** (exact `helm template` command in a blockquote); **Argo CD** (if applicable); **Next steps**. See README-STANDARD.md for full structure and template. |

**Shared volumes:** If the chart shares PVCs with another chart (e.g. plex + autoscan), the README must state which PVCs are shared and the single-writer rule. See HELM_REVIEW.md §3.

**Layout:** Prefer **nested `helm/`** for charts that also ship Terraform (e.g. *arr). Flat layout is fine for charts without Terraform. Document in README if Argo CD uses `path: helm` vs `path: .`.

**Build pipelines for publishable subcharts:** Charts that are **published as Helm charts consumed by other charts** (e.g. plex subcharts: `plex-autoskip`, `one-pace-plex-assistant`, `plex-prefer-non-forced-subs`) **must** have a **build pipeline** that packages and publishes the chart (e.g. GitHub Actions: `release-on-merge`, `release-notes`, and `helm-publish` workflows). This ensures that when the parent chart (e.g. plex) switches from `repository: file://../...` to a published repo URL, the chart is available and versioned. See `homelab/helm/plex-autoskip/.github/workflows/` and `homelab/helm/one-pace-plex-assistant/.github/workflows/` for the expected set (lint on push, release on merge to main, helm-publish on release).

---

## 3. PR descriptions (minimum bar)

Every chart-related PR **must** use a description that meets this bar (e.g. in **PR_DESCRIPTION.md**; do not commit that file—use it as the PR body).

| Section | Requirement |
|---------|-------------|
| **Title** | Clear; one leading emoji if it fits (e.g. 🌊 plex-autoskip — pod anti-affinity for HA). |
| **TL;DR** | One table row: **What** \| **Why safe** \| **Proof**. One line per column so reviewers get the gist instantly. |
| **Summary** | Table or list with an **icon per change** (🔐 🌊 📖 etc.); one row per logical change. |
| **Setup requirements** | Short list of what deployers need before using the change (1Password item, Secret, PVC). Omit section if none. |
| **Render & validation** | Exact `helm template ...` command in a blockquote; table **Check** \| **Result** with ✅ for success. |
| **Supporting evidence** | Collapsible `<details>` with emoji + title in `<summary>`; **real rendered excerpts** (YAML) that prove key changes—no placeholders. |
| **Why safe & correct** | One table: **Change** \| **What we did** \| **Why it's safe** \| **Proof in render**. |
| **Next steps** | Numbered or table; concrete actions; optional items clearly marked. |

For **Helm chart** changes, render proof is **mandatory**: run `helm template` with the value files the app uses (e.g. as in Argo CD) and paste relevant excerpts into Supporting evidence.

---

## 4. Deployment safety — don’t brick functionality

These rules keep deployments consistent and avoid breaking running workloads.

| Rule | How to satisfy it |
|------|-------------------|
| **Render before merge** | Every chart PR must show a successful `helm template` with the same value files (and paths) that Argo CD uses. No merge without a passing render and, for logic changes, evidence in the PR. |
| **Path and repo alignment** | When adding or changing a chart, ensure `config.yaml` (Argo CD) uses the correct `path` for that repo (e.g. `helm` for charts under `chart/helm/`, `.` for flat). Document in README. See HELM_REVIEW.md §2. |
| **Shared PVCs** | If a chart shares PVCs with another (e.g. plex ↔ autoscan), document in the chart README: which PVCs, who writes, and that a single writer per path is required. Create PVCs before deploy; document bootstrap. |
| **No silent behavior change** | Changing defaults or template logic must be justified in the PR (equivalence table, “why safe,” and render evidence). Prefer additive changes (new options, docs) over changing existing defaults when possible. |
| **ignoreDifferences** | If Argo CD shows noisy diff (e.g. Secret data, volumeClaimTemplates, env from downward API), add the appropriate `ignoreDifferences` in config.yaml and document why (e.g. “Secret data from 1Password”). |

Before enabling a new application in config.yaml, confirm: namespace exists (or is created), required PVCs/secrets/1Password items exist, and the chart’s README lists them under Requirements.

---

## 5. Pre-merge checklist (chart PRs)

Use this as a quick gate before merging any chart PR.

- [ ] **Chart.yaml** has at least `name`, `version`, `description`.
- [ ] **values.yaml** has a top comment (summary + “See README”).
- [ ] **README** has Chart contents, Requirements, Key values, Render & validation (exact command), and Next steps.
- [ ] **PR description** has TL;DR table, Summary with icons, Render & validation with command + result table, Supporting evidence with real snippets, Why safe table, Next steps.
- [ ] **`helm template`** was run with the value files the app uses and passes; key changes are shown in Supporting evidence.
- [ ] **Shared volumes** (if any) are documented in README and single-writer rule stated.
- [ ] **Argo CD** `path` and repo layout match; config.yaml (or comment) documents intent if the app is disabled or not yet deployed.
- [ ] **Publishable subcharts** (charts consumed by other charts via repo URL or intended for it): have `release-on-merge`, `release-notes`, and `helm-publish` (or equivalent) workflows so the chart can be published and versioned.

---

## 6. References

| Document | Purpose |
|----------|---------|
| **README-STANDARD.md** | Full README structure, legibility rules, and copy-paste template. |
| **HELM_REVIEW.md** | Chart layout, Argo CD mapping, shared volumes, Atlantis, security/ops/performance notes. |
| **.cursor/rules/pr-description-standard.mdc** | Full PR description format and Helm evidence requirement (cursor rule). |
| **.cursor/rules/after-merge-reconcile.mdc** | After PRs are merged: checkout main, pull, and reconcile locally (cursor rule). |

Charts that meet this standard: **plex-autoskip**, **oauth2-proxy**, **nextcloud** (PR descriptions); **plex**, **nextcloud**, **atlantis**, **immich** (README/Chart.yaml). Use them as references when adding or updating charts.
