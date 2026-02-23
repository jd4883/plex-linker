"""Database layer for link rules and settings. Supports SQLite and PostgreSQL via SQLAlchemy."""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
    delete,
    insert,
    select,
)
from sqlalchemy.engine import Engine

log = logging.getLogger(__name__)

metadata = MetaData()

link_rules = Table(
    "link_rules",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("movie_title", String, nullable=False),
    Column("tmdb_id", Integer, nullable=False),
    Column("show_name", String, nullable=False),
    Column("episode", Integer),
    Column("season", String),
    Column("episode_id", Integer),
    Column("series_id", Integer),
    Column("tvdb_id", Integer),
    UniqueConstraint("movie_title", "show_name"),
)

settings_table = Table(
    "settings",
    metadata,
    Column("key", String, primary_key=True),
    Column("value", Text, nullable=False),
)

_engine: Optional[Engine] = None


def _normalize_url(db_url: str) -> str:
    """Rewrite postgresql:// to postgresql+pg8000:// so the pure-Python driver is used."""
    if db_url.startswith("postgresql://"):
        return db_url.replace("postgresql://", "postgresql+pg8000://", 1)
    return db_url


def get_engine(db_url: str) -> Engine:
    global _engine
    if _engine is not None:
        return _engine

    url = _normalize_url(db_url)

    if url.startswith("sqlite"):
        path = url.removeprefix("sqlite:///")
        if path:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    _engine = create_engine(url, pool_pre_ping=True)
    metadata.create_all(_engine)
    log.info("Database initialized: %s", url.split("@")[-1] if "@" in url else url)
    return _engine


def init_db(db_url: str) -> bool:
    """Ensure tables exist. Returns True when the engine is ready."""
    if not db_url:
        return False
    try:
        get_engine(db_url)
        return True
    except Exception:
        log.exception("Failed to initialize database")
        return False


# --- Link Rules ---


def list_rules(db_url: str) -> list[dict[str, Any]]:
    engine = get_engine(db_url)
    with engine.connect() as conn:
        rows = conn.execute(
            select(link_rules).order_by(link_rules.c.movie_title, link_rules.c.show_name)
        ).mappings().all()
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
    engine = get_engine(db_url)
    with engine.begin() as conn:
        result = conn.execute(
            insert(link_rules).values(
                movie_title=movie_title,
                tmdb_id=tmdb_id,
                show_name=show_name,
                episode=episode,
                season=season,
                episode_id=episode_id,
                series_id=series_id,
                tvdb_id=tvdb_id,
            )
        )
        return result.inserted_primary_key[0] if result.inserted_primary_key else None


def delete_rule(db_url: str, rule_id: int) -> bool:
    engine = get_engine(db_url)
    with engine.begin() as conn:
        result = conn.execute(delete(link_rules).where(link_rules.c.id == rule_id))
        return result.rowcount > 0


def get_movies_dict(db_url: str) -> dict[str, Any]:
    """Return link rules in the dict shape the linker expects:
    { movie_title: { "Movie DB ID": tmdb_id, "Shows": { show_name: {...} } } }
    """
    engine = get_engine(db_url)
    with engine.connect() as conn:
        rows = conn.execute(
            select(
                link_rules.c.movie_title,
                link_rules.c.tmdb_id,
                link_rules.c.show_name,
                link_rules.c.episode,
                link_rules.c.season,
                link_rules.c.episode_id,
                link_rules.c.series_id,
                link_rules.c.tvdb_id,
            ).order_by(link_rules.c.movie_title, link_rules.c.show_name)
        ).mappings().all()

    out: dict[str, Any] = {}
    for row in rows:
        mt = row["movie_title"]
        if mt not in out:
            out[mt] = {"Movie DB ID": row["tmdb_id"], "Shows": {}}
        show_data = {
            "Episode": row["episode"],
            "Season": row["season"],
            "Episode ID": row["episode_id"],
            "seriesId": row["series_id"],
            "tvdbId": row["tvdb_id"],
        }
        out[mt]["Shows"][row["show_name"]] = {k: v for k, v in show_data.items() if v is not None}
    return out


# --- Settings ---


def get_setting(db_url: str, key: str) -> Any:
    engine = get_engine(db_url)
    with engine.connect() as conn:
        row = conn.execute(
            select(settings_table.c.value).where(settings_table.c.key == key)
        ).fetchone()
    if not row:
        return None
    try:
        return json.loads(row[0])
    except (TypeError, ValueError):
        return row[0]


def set_setting(db_url: str, key: str, value: Any) -> None:
    v = json.dumps(value) if isinstance(value, (list, dict)) else str(value)
    engine = get_engine(db_url)
    with engine.begin() as conn:
        existing = conn.execute(
            select(settings_table.c.key).where(settings_table.c.key == key)
        ).fetchone()
        if existing:
            conn.execute(
                settings_table.update().where(settings_table.c.key == key).values(value=v)
            )
        else:
            conn.execute(insert(settings_table).values(key=key, value=v))
