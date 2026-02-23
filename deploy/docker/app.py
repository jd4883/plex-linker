"""FastAPI app: health, web UI, and REST API for link rules and settings."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

import db
from config import get_settings

app = FastAPI(title="Plex Linker", version="3.0")
_settings = get_settings()
_UI_HTML = (Path(__file__).parent / "templates" / "index.html").read_text()


@app.on_event("startup")
def _init_database() -> None:
    db.init_db(_settings.database_url)


def _db_url() -> str:
    if not _settings.database_url:
        raise HTTPException(503, "DATABASE_URL is not set")
    return _settings.database_url


# --- Health ---


@app.get("/health", response_class=PlainTextResponse)
def health() -> str:
    return "ok"


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    return HTMLResponse(_UI_HTML)


# --- Link Rules API ---


class LinkRuleIn(BaseModel):
    movie_title: str
    tmdb_id: int
    show_name: str
    episode: Optional[int] = None
    season: Optional[str] = None
    episode_id: Optional[int] = None
    series_id: Optional[int] = None
    tvdb_id: Optional[int] = None


@app.get("/api/rules")
def list_rules() -> list[dict]:
    return db.list_rules(_db_url())


@app.post("/api/rules", status_code=201)
def add_rule(rule: LinkRuleIn) -> dict:
    url = _db_url()
    rid = db.add_rule(
        url,
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
def delete_rule_endpoint(rule_id: int) -> dict:
    if not db.delete_rule(_db_url(), rule_id):
        raise HTTPException(404, "Rule not found")
    return {"deleted": rule_id}


# --- Settings API ---


class SettingIn(BaseModel):
    value: Any


@app.get("/api/settings/{key}")
def get_setting(key: str) -> dict:
    v = db.get_setting(_db_url(), key)
    if v is None:
        raise HTTPException(404, "Setting not found")
    return {"key": key, "value": v}


@app.put("/api/settings/{key}")
def put_setting(key: str, body: SettingIn) -> dict:
    db.set_setting(_db_url(), key, body.value)
    return {"key": key, "value": body.value}
