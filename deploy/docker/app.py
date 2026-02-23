"""FastAPI app: health, web UI and API for link rules and settings when DATABASE_URL is set."""
import os
from typing import Any, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

from config import database_url

app = FastAPI(title="Plex Linker", version="3.0")

# --- Health (always) ---


@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"


@app.get("/", response_class=HTMLResponse)
def root():
    if database_url():
        return HTMLResponse(UI_HTML)
    return HTMLResponse(
        "<!DOCTYPE html><html><head><title>Plex Linker</title></head><body><h1>Plex Linker</h1><p>Health: <a href='/health'>/health</a></p><p>Set DATABASE_URL to use the web UI for link rules.</p></body></html>",
        status_code=200,
    )


# --- DB-backed API and UI (when DATABASE_URL is set) ---


def _db():
    if not database_url():
        return None
    from db.schema import init_db
    if not init_db():
        return None
    return __import__("db.schema", fromlist=["db"])


class LinkRuleIn(BaseModel):
    movie_title: str
    tmdb_id: int
    show_name: str
    episode: Optional[int] = None
    season: Optional[str] = None
    episode_id: Optional[int] = None
    series_id: Optional[int] = None
    tvdb_id: Optional[int] = None


class SettingIn(BaseModel):
    value: Any


@app.get("/api/rules")
def list_rules() -> List[dict]:
    db = _db()
    if db is None:
        raise HTTPException(503, "Database not configured (set DATABASE_URL)")
    return db.list_link_rules()


@app.post("/api/rules", status_code=201)
def add_rule(rule: LinkRuleIn) -> dict:
    db = _db()
    if db is None:
        raise HTTPException(503, "Database not configured")
    rid = db.add_link_rule(
        movie_title=rule.movie_title,
        tmdb_id=rule.tmdb_id,
        show_name=rule.show_name,
        episode=rule.episode,
        season=rule.season,
        episode_id=rule.episode_id,
        series_id=rule.series_id,
        tvdb_id=rule.tvdb_id,
    )
    if rid is None:
        raise HTTPException(500, "Failed to add rule")
    return {"id": rid, "movie_title": rule.movie_title, "show_name": rule.show_name}


@app.delete("/api/rules/{rule_id}")
def delete_rule(rule_id: int) -> dict:
    db = _db()
    if db is None:
        raise HTTPException(503, "Database not configured")
    if not db.delete_link_rule(rule_id):
        raise HTTPException(404, "Rule not found")
    return {"deleted": rule_id}


@app.get("/api/settings/{key}")
def get_setting(key: str) -> Any:
    db = _db()
    if db is None:
        raise HTTPException(503, "Database not configured")
    v = db.get_setting(key)
    if v is None:
        raise HTTPException(404, "Setting not found")
    return {"key": key, "value": v}


@app.put("/api/settings/{key}")
def put_setting(key: str, body: SettingIn) -> dict:
    db = _db()
    if db is None:
        raise HTTPException(503, "Database not configured")
    db.set_setting(key, body.value)
    return {"key": key, "value": body.value}


# --- Simple HTML UI ---

UI_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Plex Linker — Link Rules</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 900px; margin: 1rem auto; padding: 0 1rem; }
    h1 { font-size: 1.25rem; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }
    th { background: #eee; }
    form { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: flex-end; margin: 1rem 0; }
    input, button { padding: 0.4rem 0.6rem; }
    button.danger { background: #c00; color: #fff; border: none; cursor: pointer; }
    .msg { margin: 0.5rem 0; color: green; }
    .err { color: red; }
  </style>
</head>
<body>
  <h1>Plex Linker — Link Rules</h1>
  <p>Map movies (Radarr) to show specials (Sonarr). Add rules below; the link job runs on a schedule.</p>

  <form id="addForm">
    <input name="movie_title" placeholder="Movie title" required size="20">
    <input name="tmdb_id" type="number" placeholder="TMDB ID" required min="1" size="8">
    <input name="show_name" placeholder="Show name (Sonarr)" required size="20">
    <input name="episode" type="number" placeholder="Episode" min="0" size="4">
    <input name="season" placeholder="Season (e.g. 00)" size="4">
    <button type="submit">Add rule</button>
  </form>
  <div id="msg" class="msg"></div>
  <div id="err" class="err"></div>

  <table>
    <thead><tr><th>Movie</th><th>TMDB ID</th><th>Show</th><th>Episode</th><th>Season</th><th></th></tr></thead>
    <tbody id="rules"></tbody>
  </table>

  <script>
    const api = (path, opts = {}) => fetch(path, { ...opts, headers: { "Content-Type": "application/json", ...opts.headers } });
    function err(e) { document.getElementById("err").textContent = e; document.getElementById("msg").textContent = ""; }
    function msg(m) { document.getElementById("msg").textContent = m; document.getElementById("err").textContent = ""; }

    function load() {
      api("/api/rules").then(r => {
        if (!r.ok) { err("Database not configured (set DATABASE_URL) or API error"); return r.json().catch(() => ({})); }
        return r.json();
      }).then(data => {
        if (!Array.isArray(data)) return;
        const tbody = document.getElementById("rules");
        tbody.innerHTML = data.map(r =>
          `<tr><td>${escapeHtml(r.movie_title)}</td><td>${r.tmdb_id}</td><td>${escapeHtml(r.show_name)}</td><td>${r.episode ?? ""}</td><td>${r.season ?? ""}</td><td><button class="danger" onclick="del(${r.id})">Delete</button></td></tr>`
        ).join("");
      }).catch(() => err("Failed to load rules"));
    }
    function escapeHtml(s) { const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
    function del(id) {
      api("/api/rules/" + id, { method: "DELETE" }).then(r => { if (r.ok) { msg("Deleted"); load(); } else err("Delete failed"); });
    }
    document.getElementById("addForm").onsubmit = (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const body = { movie_title: fd.get("movie_title"), tmdb_id: parseInt(fd.get("tmdb_id"), 10), show_name: fd.get("show_name") };
      if (fd.get("episode")) body.episode = parseInt(fd.get("episode"), 10);
      if (fd.get("season")) body.season = fd.get("season");
      api("/api/rules", { method: "POST", body: JSON.stringify(body) })
        .then(r => { if (r.ok) { msg("Rule added"); e.target.reset(); load(); } else r.json().then(j => err(j.detail || "Failed")); })
        .catch(() => err("Request failed"));
    };
    load();
  </script>
</body>
</html>
"""


