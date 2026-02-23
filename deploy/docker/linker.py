"""Core link job: match movies (Radarr) to show specials (Sonarr) and create symlinks."""
from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Optional

from api_clients import RadarrClient, SonarrClient
from config import Settings

log = logging.getLogger(__name__)


def remove_broken_symlinks(root: str) -> None:
    """Walk root and unlink any symlinks whose target no longer exists."""
    for dirpath, _, filenames in os.walk(root, topdown=False):
        for name in filenames:
            p = Path(dirpath) / name
            if p.is_symlink() and not p.exists():
                try:
                    p.unlink()
                    log.debug("Removed broken symlink: %s", p)
                except OSError:
                    pass


def _sanitize_path(s: str) -> str:
    """Normalize a path component: collapse '..', replace ':' with '-', strip leading '/'."""
    return s.replace("..", ".").replace(":", "-").lstrip("/")


def _find_radarr_movie(tmdb_id: int, radarr_movies: list[dict]) -> Optional[dict]:
    for movie in radarr_movies:
        if movie.get("tmdbId") == tmdb_id:
            return movie
    return None


def _extract_movie_file_info(radarr_data: dict) -> tuple[str, str, str]:
    """Return (absolute_file_path, quality_name, extension) from a Radarr movie entry."""
    movie_file = radarr_data.get("movieFile")
    if not movie_file:
        return "", "", ".mkv"

    movie_path = radarr_data.get("path", "")
    relative = movie_file.get("relativePath", "")
    quality_name = ((movie_file.get("quality") or {}).get("quality") or {}).get("name", "")
    extension = (
        re.sub(re.escape(quality_name), "", relative.rsplit(" ", 1)[-1])
        if quality_name
        else os.path.splitext(relative)[1]
    )
    absolute = os.path.join(movie_path, relative).replace(":", "-")
    return absolute, quality_name, extension


def _find_special_episode(sonarr: SonarrClient, series_id: int, target_episode: int) -> Optional[dict]:
    """Find a Season 0 episode matching target_episode for the given series."""
    for ep in sonarr.get_episodes(series_id):
        try:
            if int(ep.get("seasonNumber", -1)) == 0 and int(ep.get("episodeNumber", -1)) == target_episode:
                return ep
        except (TypeError, ValueError):
            continue
    return None


def _pad_episode(episode: Any, padding: int) -> str:
    if isinstance(episode, list):
        return "-".join(str(e).zfill(padding) for e in episode)
    if episode is not None:
        return str(episode).zfill(padding)
    return "00"


def _create_relative_symlink(src: Path, dst: Path) -> bool:
    """Create a symlink at dst pointing to src using a relative target."""
    if not src.is_file():
        log.warning("Source file not found: %s", src)
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)
    rel_target = os.path.relpath(src, dst.parent)

    if dst.exists() or dst.is_symlink():
        dst.unlink()

    os.symlink(rel_target, dst)
    log.info("Symlink: %s -> %s", dst, rel_target)
    return True


def _process_show_link(
    sonarr: SonarrClient,
    show_name: str,
    show_rule: dict,
    movie_file_path: str,
    quality: str,
    extension: str,
    media_root: str,
    root_path_prefix: str,
) -> None:
    """Look up a show in Sonarr, find the matching specials episode, and create the symlink."""
    try:
        series_data = sonarr.lookup_series(show_name)
    except Exception:
        log.exception("Sonarr lookup failed for %s", show_name)
        return
    if not series_data:
        log.warning("Show not found in Sonarr: %s", show_name)
        return

    series_id = series_data.get("id", 0)
    if not series_id:
        return

    show_path = str(series_data.get("path", "")).replace(root_path_prefix, "", 1)
    is_anime = "anime" in (series_data.get("seriesType") or "")
    padding = 3 if is_anime else 2

    target_episode = show_rule.get("Episode")
    if target_episode is None:
        log.debug("No target episode for show %s, skipping", show_name)
        return

    episode_data = _find_special_episode(sonarr, series_id, target_episode)
    if not episode_data:
        log.warning("Episode S00E%s not found for %s", target_episode, show_name)
        return

    episode_title = re.sub(r"\(\d+\)$", "", episode_data.get("title", "")).strip()
    season = show_rule.get("Season", "00")
    parsed_ep = _pad_episode(target_episode, padding)
    season_folder = f"Season {season}"
    series_title = series_data.get("title", show_name)
    dst_filename = f"{series_title} - S{season}E{parsed_ep} - {episode_title} {quality}{extension}"
    dst_rel = os.path.join(show_path, season_folder, dst_filename)

    src_clean = _sanitize_path(movie_file_path)
    dst_clean = _sanitize_path(dst_rel)

    src_abs = Path(media_root) / src_clean
    dst_abs = Path(media_root) / dst_clean

    _create_relative_symlink(src_abs, dst_abs)

    try:
        sonarr.rescan_series(series_id)
        sonarr.refresh_series(series_id)
    except Exception:
        log.exception("Failed to refresh Sonarr series %d", series_id)


def _load_data(settings: Settings) -> dict[str, Any]:
    """Return movies_dict, a get_setting callable, and whether to persist back to YAML."""
    if settings.use_db:
        import db

        if db.init_db(settings.database_url):
            return {
                "movies_dict": db.get_movies_dict(settings.database_url),
                "get_setting": lambda key: db.get_setting(settings.database_url, key),
                "persist_yaml": False,
            }
    import yaml_config

    return {
        "movies_dict": yaml_config.read_movies_dict(settings.app_root),
        "get_setting": lambda key: yaml_config.read_setting(settings.app_root, key),
        "persist_yaml": True,
    }


def run_link_job(settings: Settings) -> None:
    """Execute one link-job run. No-op when the media path is missing or invalid."""
    media_root = settings.media_root
    if not media_root or not os.path.isdir(media_root):
        log.info("No valid media root configured, skipping link job")
        return

    lock_path = Path(__file__).parent / "pid.lock"
    if lock_path.exists():
        log.info("Lock file exists, another job may be running")
        return

    lock_path.touch()
    try:
        _run(settings, media_root)
    finally:
        lock_path.unlink(missing_ok=True)


def _run(settings: Settings, media_root: str) -> None:
    remove_broken_symlinks(media_root)

    sonarr = SonarrClient(
        settings.sonarr_api_base,
        settings.sonarr_api_key,
        root_path_prefix=settings.sonarr_root_path_prefix,
    )
    radarr = RadarrClient(settings.radarr_api_base, settings.radarr_api_key)

    provider = _load_data(settings)
    movies_dict: dict[str, Any] = provider["movies_dict"]
    if not movies_dict:
        log.info("No link rules found")
        return

    radarr_library = radarr.get_movies()

    for movie_name in sorted(movies_dict):
        rule = movies_dict[movie_name]
        tmdb_id = rule.get("Movie DB ID")
        if not tmdb_id or not str(tmdb_id).isdigit() or int(tmdb_id) == 0:
            log.debug("Skipping %s: invalid TMDB ID %s", movie_name, tmdb_id)
            continue

        radarr_data = _find_radarr_movie(int(tmdb_id), radarr_library)
        if not radarr_data or not radarr_data.get("hasFile"):
            log.debug("Skipping %s: not in Radarr or no file downloaded", movie_name)
            continue

        movie_file_path, quality, extension = _extract_movie_file_info(radarr_data)
        if not movie_file_path:
            continue

        movie_id = radarr_data.get("id", 0)

        for show_name, show_rule in (rule.get("Shows") or {}).items():
            if not isinstance(show_rule, dict):
                continue
            _process_show_link(
                sonarr=sonarr,
                show_name=show_name,
                show_rule=show_rule,
                movie_file_path=movie_file_path,
                quality=quality,
                extension=extension,
                media_root=media_root,
                root_path_prefix=settings.sonarr_root_path_prefix,
            )

        if movie_id:
            try:
                radarr.rescan_movie(movie_id)
            except Exception:
                log.exception("Failed to rescan Radarr movie %d", movie_id)

    if provider["persist_yaml"]:
        import yaml_config

        yaml_config.write_movies_dict(settings.app_root, movies_dict, settings.config_archives)
