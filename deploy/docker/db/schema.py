"""Schema and access for link rules and settings. Same logical shape as the YAML config. SQLite only (Postgres can be added via SQLAlchemy later)."""
import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

from config import database_url


def _get_connection_url() -> Optional[str]:
    url = database_url().strip()
    if not url:
        return None
    if url.startswith("sqlite:///"):
        path = url.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(path), exist_ok=True)
    return url


@contextmanager
def _connection():
    url = _get_connection_url()
    if not url:
        yield None
        return
    if not url.startswith("sqlite:///"):
        yield None
        return
    path = url.replace("sqlite:///", "")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> bool:
    """Create tables if they don't exist. Returns True if DB is in use."""
    url = _get_connection_url()
    if not url or not url.startswith("sqlite:///"):
        return False
    path = url.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with _connection() as conn:
        if conn is None:
            return False
        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.execute("""
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
            )
        """)
    return True


def get_movies_dict() -> Dict[str, Any]:
    """Same shape as YAML: { movie_title: { Movie DB ID, Shows: { show_name: {...} } } }."""
    with _connection() as conn:
        if conn is None:
            return {}
        cur = conn.execute(
            "SELECT movie_title, tmdb_id, show_name, episode, season, episode_id, series_id, tvdb_id FROM link_rules ORDER BY movie_title, show_name"
        )
        rows = cur.fetchall()
    out = {}
    for r in rows:
        row = dict(r)
        mt = row["movie_title"]
        if mt not in out:
            out[mt] = {"Movie DB ID": row["tmdb_id"], "Shows": {}}
        show = row["show_name"]
        out[mt]["Shows"][show] = {
            "Episode": row.get("episode"),
            "Season": row.get("season"),
            "Episode ID": row.get("episode_id"),
            "seriesId": row.get("series_id"),
            "tvdbId": row.get("tvdb_id"),
        }
        # Drop None values so the rest of the code doesn't see missing keys as None
        out[mt]["Shows"][show] = {k: v for k, v in out[mt]["Shows"][show].items() if v is not None}
    return out


def get_setting(key: str) -> Any:
    """Return a setting (e.g. 'Movie Directories'). Lists stored as JSON."""
    with _connection() as conn:
        if conn is None:
            return None
        cur = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cur.fetchone()
    if not row:
        return None
    val = row[0]
    try:
        return json.loads(val)
    except (TypeError, ValueError):
        return val


def set_setting(key: str, value: Any) -> None:
    url = _get_connection_url()
    if not url:
        return
    v = json.dumps(value) if isinstance(value, (list, dict)) else str(value)
    with _connection() as conn:
        if conn is None:
            return
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, v))


def list_link_rules() -> List[Dict[str, Any]]:
    with _connection() as conn:
        if conn is None:
            return []
        cur = conn.execute(
            "SELECT id, movie_title, tmdb_id, show_name, episode, season, episode_id, series_id, tvdb_id FROM link_rules ORDER BY movie_title, show_name"
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def add_link_rule(
    movie_title: str,
    tmdb_id: int,
    show_name: str,
    episode: Optional[int] = None,
    season: Optional[str] = None,
    episode_id: Optional[int] = None,
    series_id: Optional[int] = None,
    tvdb_id: Optional[int] = None,
) -> Optional[int]:
    with _connection() as conn:
        if conn is None:
            return None
        cur = conn.execute(
            "INSERT INTO link_rules (movie_title, tmdb_id, show_name, episode, season, episode_id, series_id, tvdb_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (movie_title, tmdb_id, show_name, episode, season, episode_id, series_id, tvdb_id),
        )
        return cur.lastrowid


def delete_link_rule(rule_id: int) -> bool:
    with _connection() as conn:
        if conn is None:
            return False
        conn.execute("DELETE FROM link_rules WHERE id = ?", (rule_id,))
        return True
