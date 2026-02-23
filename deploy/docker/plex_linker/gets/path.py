"""Config and media paths. Uses config.config_root() and DOCKER_MEDIA_PATH."""
import os

from config import config_archives, config_root, docker_media_path


def parsed_collection() -> str:
    root = config_root()
    return os.path.join(root, "config_files", "media_collection_parsed_last_run.yaml") if root else ""


def get_media_collection_parsed_archives() -> str:
    return config_archives()


def get_docker_media_path(g) -> str:
    base = docker_media_path()
    first = (g.MOVIES_PATH or [""])[0]
    return os.path.join(base, first) if base else first
