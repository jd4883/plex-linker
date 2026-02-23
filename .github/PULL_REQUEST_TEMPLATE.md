# [Chart name] — [Short title]

---

## TL;DR

| | |
|---|---|
| **What** | One-line summary of the change. |
| **Why safe** | One-line: why this is safe (e.g. soft affinity only, no breaking change). |
| **Proof** | One-line: how you verified (e.g. `helm template` OK, or test steps). |

---

## Summary

| Icon | Change |
|------|--------|
| | **Change 1** — Short description. |
| | **Change 2** — Short description. |

*(Use one row per logical change; lead with an emoji if helpful: e.g. lock, wave, bug, book.)*

---

## Setup requirements (if any)

*(Omit if none. Otherwise: bullet list of what reviewers or deployers need — e.g. 1Password item, PVC, env var.)*

---

## Render & validation (for Helm charts)

> **Command used:**  
> `helm template <release> . -f values.yaml -n <namespace>`

| Check | Result |
|-------|--------|
| `helm template ...` | OK / failed |
| *(Other checks)* | OK / failed |

---

## Supporting evidence

<details>
<summary>Relevant snippet or proof</summary>

```yaml
# Paste short rendered YAML or output that proves the change.
```

</details>

---

## Why this change is safe & correct

| Change | What we did | Why it's safe | Proof |
|--------|--------------|---------------|-------|
| *(Change)* | *(Brief)* | *(Brief)* | *(Reference evidence above)* |

---

## Next steps

| Step | Action |
|------|--------|
| 1 | Merge; *(what happens next)*. |
| 2 | *(Optional follow-up.)* |

---

**Checklist**

- [ ] Title starts with chart name or scope (e.g. `[nextcloud]` or `[plex]`).
- [ ] Chart version bumped in `Chart.yaml` if applicable (semver).
- [ ] `helm dependency update` and `helm template` run successfully.
