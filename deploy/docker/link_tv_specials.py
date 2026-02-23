#!/usr/bin/env python3
"""One-shot or periodic link job: sync TV specials from movies into show paths (Sonarr/Radarr + Plex)."""
import os
from pathlib import Path


def _remove_broken_symlinks(root: str) -> None:
    """Remove broken symlinks under root (Python-only; no find binary)."""
    root_path = Path(root)
    for dirpath, _dirnames, filenames in os.walk(root_path, topdown=False):
        for name in filenames:
            p = Path(dirpath) / name
            if p.is_symlink() and not p.exists():
                try:
                    p.unlink()
                except OSError:
                    pass


def run_link_job() -> None:
    """Run the link job once. No-op and return if no media path configured."""
    media_root = os.environ.get("MEDIA_ROOT") or os.environ.get("DOCKER_MEDIA_PATH")
    if not media_root or not os.path.isdir(media_root):
        return

    script_dir = os.path.dirname(os.path.realpath(__file__))
    lock_path = os.path.join(script_dir, "pid.lock")
    if os.path.exists(lock_path):
        return

    # Lazy import so health-only (no media) runs don't require Sonarr/Radarr/Plex env
    import methods as media
    from data_provider import should_persist_to_yaml
    from jobs.cleanup.cleanup import post_execution_cleanup
    from plex_linker.gets.path import get_docker_media_path
    from plex_linker.parser.movies import parse_all_movies_in_yaml_dictionary as parse_movies

    work_dir = str(os.environ.get("DOCKER_MEDIA_PATH", media_root))
    os.chdir(work_dir)
    _remove_broken_symlinks(work_dir)
    Path(lock_path).touch()
	try:
		g = media.Globals()
		master_dictionary = media.Movies(str(os.path.abspath(get_docker_media_path(g))))
		parse_movies(g)
		if should_persist_to_yaml():
			from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file as dict_to_yaml
			dict_to_yaml(g)
		post_execution_cleanup()
	finally:
		try:
			os.remove(lock_path)
		except OSError:
			pass


if __name__ == "__main__":
	run_link_job()
	media_root = os.environ.get("MEDIA_ROOT") or os.environ.get("DOCKER_MEDIA_PATH")
	if not media_root or not os.path.isdir(media_root):
		raise SystemExit(0)
