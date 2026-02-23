# deploy/helm

Helm chart submodules for qBittorrent deployment.

## Submodules

| Path | Repo | Purpose |
|------|------|---------|
| `qbittorrent-vpn` | [jd4883/qbittorrent-vpn-helm](https://github.com/jd4883/qbittorrent-vpn-helm) | qBittorrent + Gluetun + Privoxy |
| `qbittorrent-jobs` | jd4883/qbittorrent-jobs (private) | CronJobs: cleanup, ratio-manager |

## qbittorrent-jobs submodule

The `qbittorrent-jobs` chart is in this directory. To convert to a submodule once the private repo exists:

1. Create `jd4883/qbittorrent-jobs` (private) on GitHub
2. Push the content:
   ```bash
   cd deploy/helm/qbittorrent-jobs
   git init && git add . && git commit -m "feat: initial qbittorrent-jobs chart"
   git remote add origin git@github.com:jd4883/qbittorrent-jobs.git
   git push -u origin main
   ```
3. In the home repo root:
   ```bash
   git rm -r --cached deploy/helm/qbittorrent-jobs
   git submodule add git@github.com:jd4883/qbittorrent-jobs.git deploy/helm/qbittorrent-jobs
   git add .gitmodules deploy/helm/qbittorrent-jobs
   git commit -m "chore: convert qbittorrent-jobs to submodule"
   ```

## qbittorrent-vpn

Chart content is in the submodule. After pushing updates to `qbittorrent-vpn-helm`, run `git submodule update --remote deploy/helm/qbittorrent-vpn` in the home repo.
