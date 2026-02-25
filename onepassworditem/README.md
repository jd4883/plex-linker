# onepassworditem (expectedbehaviors fork)

Helm chart to sync [1Password](https://1password.com/) items into Kubernetes Secrets via the [1Password Kubernetes Operator](https://github.com/1Password/onepassword-operator). Each item becomes a `OnePasswordItem` custom resource; the operator creates the Secret in the same namespace.

**This is a fork of the original chart by [vquie](https://github.com/vquie/helm-charts)** (published at https://vquie.github.io/helm-charts). We do not claim credit for the original design. This fork changes the values schema and behavior as described below so the chart is easier to reuse and avoids namespace mistakes.

## Changes in this fork

- **Namespace from release:** OnePasswordItem resources are always created in **`.Release.Namespace`** (the namespace of the Helm release). You no longer key items by namespace in values.
- **Simplified schema:** Use a single list **`items`** instead of **`secrets.<namespace>: [ ... ]`**. No risk of creating secrets in the wrong namespace when the key doesn’t match the release.
- **`enabled` toggle:** Set **`enabled: false`** to create no OnePasswordItem resources (e.g. for a generic chart that can be installed with or without 1Password).

## Prerequisites

- [1Password Kubernetes Operator](https://github.com/1Password/onepassword-operator) (or 1Password Connect + operator) installed and configured.
- Items and vaults exist in 1Password; paths use the form `vaults/<vault_id_or_title>/items/<item_id_or_title>`.

## Values

| Key       | Type    | Default | Description |
|----------|--------|--------|-------------|
| `enabled` | bool   | `true` | If `false`, no OnePasswordItem resources are rendered. |
| `items`   | list   | `[]`   | List of 1Password items to sync. See below. |

Each entry in `items`:

| Key               | Type   | Required | Description |
|-------------------|--------|----------|-------------|
| `item`            | string | yes      | 1Password item path, e.g. `vaults/Kubernetes/items/myapp`. |
| `name`            | string | yes      | Name of the Kubernetes Secret to create. |
| `type`            | string | no       | Kubernetes Secret type (default `Opaque`). |
| `secretAnnotations` | map  | no       | Annotations to apply to the Secret after the operator creates it (see [Secret annotations and labels](#secret-annotations-and-labels-replication)). |
| `secretLabels`    | map    | no       | Labels to apply to the Secret after the operator creates it (see [Secret annotations and labels](#secret-annotations-and-labels-replication)). |

## Secret annotations and labels (replication)

The 1Password operator creates Secrets from `OnePasswordItem` resources but **does not support passing annotations or labels** onto those Secrets via the CRD. If you need the Secret to be annotated or labeled (e.g. for [kubernetes-replicator](https://github.com/mittwald/kubernetes-replicator) or other tools that select Secrets by annotation), this chart provides a workaround:

- Add **`secretAnnotations`** and/or **`secretLabels`** to any item in **`items`**.
- A **post-install/upgrade Helm hook** (a Job with RBAC) runs after the operator has created the Secret, then patches the Secret with those annotations and labels. The hook waits for the Secret to exist (with retries) before patching.

No hook or extra RBAC is created if no item has `secretAnnotations` or `secretLabels`.

Example for replicating a secret to other namespaces with kubernetes-replicator:

```yaml
items:
  - item: vaults/Kubernetes/items/myapp
    name: myapp
    type: Opaque
    secretAnnotations:
      replicator.v1.mittwald.de/replication-allowed: "true"
      replicator.v1.mittwald.de/replication-allowed-namespaces: "*"
```

## Example

```yaml
enabled: true
items:
  - item: vaults/Kubernetes/items/myapp
    name: myapp
    type: Opaque
  - item: vaults/Kubernetes/items/myapp-db
    name: myapp-db-credentials
    type: Opaque
```

Install in namespace `myapp`:

```bash
helm upgrade --install myapp-secrets . -n myapp -f values.yaml
```

Secrets are created in the `myapp` namespace automatically.

## Using as a subchart

Add the chart as a dependency and pass `items` (and optionally `enabled`) from the parent:

**Chart.yaml:**

```yaml
dependencies:
  - name: onepassworditem
    version: "1.1.0"
    repository: https://expectedbehaviors.github.io/onepassworditem  # or OCI / git
```

**Parent values (e.g. `values.yaml`):**

```yaml
onepassworditem:
  enabled: true
  items:
    - item: vaults/Kubernetes/items/sonarr
      name: sonarr
      type: Opaque
```

The subchart receives values under the dependency name (`onepassworditem`). OnePasswordItem resources are created in the **parent release’s namespace** (`.Release.Namespace`), so they always match where the parent chart is installed.

## Publishing this fork

To host in the **expectedbehaviors** GitHub org:

1. Create a new repository **expectedbehaviors/onepassworditem** on GitHub.
2. From this directory:  
   `git init && git add . && git commit -m "chore: initial fork from vquie/helm-charts"`  
   `git remote add origin git@github.com:expectedbehaviors/onepassworditem.git`  
   `git branch -M main && git push -u origin main`
3. To serve via Helm repo: use GitHub Pages, or push the chart to an OCI registry, and reference that URL in parent `Chart.yaml` (see “Using as a subchart” above).

## Original chart

- **Author:** [vquie](https://github.com/vquie/helm-charts)
- **Helm repo:** https://vquie.github.io/helm-charts  
- Original schema uses `secrets.<namespace>: [ { item, name, type } ]`; the key is the target Kubernetes namespace. This fork replaces that with `enabled` + `items` and derives namespace from the Helm release.

---

## Support

If this project is useful to you, consider supporting its development. Anything public we publish in the expectedbehaviors org is maintained in our spare time; donations help keep the lights on and the charts updated.

- **[GitHub Sponsors](https://github.com/sponsors/expectedbehaviors)** — Recurring or one-time support.
- **[Ko-fi](https://ko-fi.com/expectedbehaviors)** — One-time tip (replace with your Ko-fi link if different).

Thank you for using our charts.
