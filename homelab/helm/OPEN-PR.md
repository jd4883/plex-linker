# Opening a PR for this branch

Use this when you want to get the current branch onto a PR (e.g. after committing chart changes).

1. **Remote** — Ensure the repo has a remote (e.g. `git remote add origin <url>`).
2. **Push** — `git push -u origin <branch>` (e.g. `feature/secrets-immich-harbor-longhorn`).
3. **Create PR** — `gh pr create --base main --head <branch> --title "<scope> Short title" --body-file .github/PULL_REQUEST_TEMPLATE.md`  
   Then edit the PR body in the UI to fill the template (TL;DR, Summary, Render & validation, etc.) per [CHART_STANDARD.md](./CHART_STANDARD.md).

If you use 1Password for `gh`: `GH_HOST=github.com op run --env-file=homelab/.env.gh -- gh pr create ...`
