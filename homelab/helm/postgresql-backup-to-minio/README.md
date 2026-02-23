# postgresql-backup-to-minio

CronJob that runs **pg_dumpall** against the shared PostgreSQL cluster and uploads the dump to **MinIO (HDD/backups tier)**. Deploy in namespace **postgresql**. **Managed by Argo CD** when enabled in config.

---

## Chart contents

- **CronJob:** Runs daily (default 02:00); uses `postgres:16-alpine`, installs MinIO client (`mc`), runs pg_dumpall and uploads to `s3-backups` (MinIO backups tier).
- **Secrets:** Uses existing Secret for Postgres superuser password and a Secret in `postgresql` namespace for MinIO credentials.

---

## Requirements

| Dependency | Notes |
|------------|--------|
| **PostgreSQL** | Shared cluster in namespace `postgresql`; Secret **postgresql-superuser** with key **password** (already created by postgresql cluster chart). |
| **MinIO backups tier** | MinIO deployed with **values-backups.yaml** (minio-backups); endpoint e.g. `https://s3-backups.expectedbehaviors.com`. |
| **Secret minio-backups-credentials** | In namespace **postgresql**, with keys **rootUser** and **rootPassword** (same as MinIO root credentials). Create via 1Password/ExternalSecret or replicate from `minio` namespace (e.g. kubernetes-replicator). |
| **Bucket** | Chart uploads to bucket **db-backups**; create the bucket in MinIO console or it may be auto-created on first upload. |

---

## Setup

1. Ensure **minio-backups** (HDD tier) is deployed and reachable at `minio.minio.svc` or your ingress host.
2. Create Secret **minio-backups-credentials** in namespace **postgresql** with keys **rootUser** and **rootPassword** (e.g. same values as Secret **minio** in `minio` namespace; use replicator or 1Password).
3. Deploy this chart to namespace **postgresql** (e.g. via Argo CD).

---

## Key values

| Area | Where | What to set |
|------|--------|-------------|
| Schedule | `schedule` | Cron expression (default `0 2 * * *`). |
| PostgreSQL | `postgresql.*` | Host, port, user, existingSecret (postgresql-superuser), passwordKey. |
| MinIO | `minio.*` | endpoint, bucket, existingSecret (minio-backups-credentials), rootUserKey, rootPasswordKey. |

---

## Render & validation

> `helm template postgresql-backup-to-minio . -f values.yaml -n postgresql`

Chart lints and templates successfully.

---

## Argo CD

Application is defined in **homelab/helm/core/argocd/terraform/argocd-config/configs/config.yaml** under the postgresql project (e.g. `postgresql-backup-to-minio`). Path and sourceRepo match the repo that contains this chart.

---

## Next steps

- [ ] Deploy MinIO backups tier (minio with values-backups.yaml) and ensure endpoint/bucket exist.
- [ ] Create Secret **minio-backups-credentials** in namespace **postgresql** (rootUser, rootPassword).
- [ ] Deploy this chart to namespace **postgresql** via Argo CD or `helm install`; confirm CronJob runs and uploads appear in MinIO.

---

## Other databases (*arr, Redis)

- ***arr (Prowlarr, etc.):** Each *arr chart has its own pg_dumpall CronJob writing to a PVC (e.g. prowlarr-postgresql-pgdumpall). To also send those to MinIO, you can add a second CronJob per app that mounts the same PVC and runs `mc mirror` to the backups tier, or extend the backup command to upload after dump. Not included in this chart.
- **Redis:** For Redis RDB backup to MinIO, add a separate CronJob that triggers BGSAVE and uploads the RDB file; not included here.
