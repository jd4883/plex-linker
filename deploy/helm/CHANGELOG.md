# deploy/helm

## 2026-02-22

### Added

- **deploy/helm/** path with submodules for qBittorrent charts
- **qbittorrent-vpn** submodule → [jd4883/qbittorrent-vpn-helm](https://github.com/jd4883/qbittorrent-vpn-helm)
  - Chart content pushed with author/committer `15719920+jd4883@users.noreply.github.com` (GitHub email privacy)
- **qbittorrent-jobs** chart (tracked as regular files; convert to submodule when private repo exists)
- **README.md** with instructions for qbittorrent-jobs submodule conversion

### Usage

From repo root:

```bash
git submodule update --init deploy/helm/qbittorrent-vpn
cd homelab/helm/qbittorrent
helm dependency update
helm template qbittorrent-public . -f values/configmaps.yaml -f values/public.yaml -n media-server
```

### PRs

- **homelab-qbittorrent**: [PR #1](https://github.com/jd4883/homelab-qbittorrent/pull/1) — refactor: 4x instantiation, deploy/helm submodules, generic inputs
