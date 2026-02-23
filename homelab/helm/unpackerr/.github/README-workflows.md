# Workflows for jd4883/homelab-unpackerr

These files are used by `create-unpackerr-chart-repo.sh` when pushing to the chart repo. If the first push skipped them (GH_TOKEN missing `workflow` scope), add them in a follow-up:

1. Ensure your GitHub token has the **workflow** scope.
2. Re-run from workspace root:  
   `GH_HOST=github.com op run --env-file=homelab/.env.gh -- ./homelab/helm/create-unpackerr-chart-repo.sh`  
   (Script will clone, add these workflows, commit, push — or add them manually in a PR to jd4883/homelab-unpackerr.)

After merge to main, the release-on-merge workflow creates tag `unpackerr-vX.Y.Z` and a GitHub Release; release-notes (if OPENAI_API_KEY is set) fills in notes.
