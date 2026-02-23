# qbittorrent-jobs

CronJobs for qBittorrent instances: **cleanup** (unregistered torrent removal, reannounce) and **ratio-manager** (seeding ratio management per tracker).

Each job has `enable: true` by default; override in parent chart values.

## Usage

Use as a Helm dependency from the homelab qbittorrent chart. Each qbittorrent instance (public, private, anime-public, anime-private) deploys one release with this jobs subchart.

### Generic inputs (derived in chart)

- **qbittorrentHost** / **qbittorrentApiUrl**: Derived from `Release.Name` and `Release.Namespace` (service DNS). Override only when service name differs from release name.

### Parent overrides

- `ratioManager.configMaps.ratioManager.data`: Instance-specific `.qman` files (override in parent)
- `cleanup.schedule`, `ratioManager.schedule`: Optional schedule overrides

### Example values override (parent chart)

```yaml
jobs:
  ratioManager:
    configMaps:
      ratioManager:
        data:
          seeding.qman: |
            { "category": "seeding", "public": {...}, "private": {...}, "delete_files": true }
```

## Repo

This chart lives in a **private** repository. Set `repository` in the parent Chart.yaml to your private Helm repo or `file://` for local development.
