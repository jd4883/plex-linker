"""SQLite database for link rules and settings."""
from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Generator, Optional

_CREATE_TABLES = """\
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS link_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_title TEXT NOT NULL,
    tmdb_id INTEGER NOT NULL,
    show_name TEXT NOT NULL,
    episode INTEGER,
    season TEXT,
    episode_id INTEGER,
    series_id INTEGER,
    tvdb_id INTEGER,
    UNIQUE(movie_title, show_name)
);
"""

_initialized: set[str] = set()


def _sqlite_path(db_url: str) -> Optional[str]:
    if not db_url.startswith("sqlite:///"):
        return None
    return db_url.removeprefix("sqlite:///")


@contextmanager
def _connect(db_url: str) -> Generator[Optional[sqlite3.Connection], None, None]:
    path = _sqlite_path(db_url)
    if path is None:
        yield None
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_url: str) -> bool:
    """Create tables if needed. Returns True when the DB is usable."""
    if not db_url or _sqlite_path(db_url) is None:
        return False
    if db_url in _initialized:
        return True
    with _connect(db_url) as conn:
        if conn is None:
            return False
        conn.executescript(_CREATE_TABLES)
    _initialized.add(db_url)
    return True


def list_rules(db_url: str) -> list[dict[str, Any]]:
    with _connect(db_url) as conn:
        if conn is None:
            return []
        rows = conn.execute(
            "SELECT id, movie_title, tmdb_id, show_name, episode, season, "
            "episode_id, series_id, tvdb_id FROM link_rules ORDER BY movie_title, show_name"
        ).fetchall()
    return [dict(r) for r in rows]


def add_rule(
    db_url: str,
    *,
    movie_title: str,
    tmdb_id: int,
    show_name: str,
    episode: Optional[int] = None,
    season: Optional[str] = None,
    episode_id: Optional[int] = None,
    series_id: Optional[int] = None,
    tvdb_id: Optional[int] = None,
) -> Optional[int]:
    with _connect(db_url) as conn:
        if conn is None:
            return None
        cur = conn.execute(
            "INSERT INTO link_rules (movie_title, tmdb_id, show_name, episode, season, "
            "episode_id, series_id, tvdb_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (movie_title, tmdb_id, show_name, episode, season, episode_id, series_id, tvdb_id),
        )
        return cur.lastrowid


def delete_rule(db_url: str, rule_id: int) -> bool:
    with _connect(db_url) as conn:
        if conn is None:
            return False
        cur = conn.execute("DELETE FROM link_rules WHERE id = ?", (rule_id,))
        return cur.rowcount > 0


def get_movies_dict(db_url: str) -> dict[str, Any]:
    """Return link rules in the same shape the YAML config uses:
    { movie_title: { "Movie DB ID": tmdb_id, "Shows": { show_name: {...} } } }
    """
    with _connect(db_url) as conn:
        if conn is None:
            return {}
        rows = conn.execute(
            "SELECT movie_title, tmdb_id, show_name, episode, season, "
            "episode_id, series_id, tvdb_id FROM link_rules ORDER BY movie_title, show_name"
        ).fetchall()
    out: dict[str, Any] = {}
    for r in rows:
        row = dict(r)
        mt = row["movie_title"]
        if mt not in out:
            out[mt] = {"Movie DB ID": row["tmdb_id"], "Shows": {}}
        show_data = {
            "Episode": row.get("episode"),
            "Season": row.get("season"),
            "Episode ID": row.get("episode_id"),
            "seriesId": row.get("series_id"),
            "tvdbId": row.get("tvdb_id"),
        }
        out[mt]["Shows"][row["show_name"]] = {k: v for k, v in show_data.items() if v is not None}
    return out


def get_setting(db_url: str, key: str) -> Any:
    with _connect(db_url) as conn:
        if conn is None:
            return None
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    if not row:
        return None
    try:
        return json.loads(row[0])
    except (TypeError, ValueError):
        return row[0]


def set_setting(db_url: str, key: str, value: Any) -> None:
    v = json.dumps(value) if isinstance(value, (list, dict)) else str(value)
    with _connect(db_url) as conn:
        if conn is None:
            return
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, v))
