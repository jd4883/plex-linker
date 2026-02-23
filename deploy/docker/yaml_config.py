"""Legacy YAML config reader/writer (used when DATABASE_URL is unset)."""
from __future__ import annotations

import os
import shutil
import time
from pathlib import Path
from typing import Any

import yaml


def read_movies_dict(app_root: str) -> dict[str, Any]:
    path = os.path.join(app_root, "config_files", "media_collection_parsed_last_run.yaml")
    with open(path) as f:
        return yaml.safe_load(f) or {}


def read_setting(app_root: str, key: str) -> Any:
    path = os.path.join(app_root, "config_files", "variables.yaml")
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return data.get(key)


def write_movies_dict(app_root: str, movies_dict: dict[str, Any], archives_dir: str) -> None:
    """Archive the previous run file and write the updated dict."""
    config_dir = os.path.join(app_root, "config_files")
    current = os.path.join(config_dir, "media_collection_parsed_this_run.yaml")
    previous = os.path.join(config_dir, "media_collection_parsed_last_run.yaml")

    Path(current).parent.mkdir(parents=True, exist_ok=True)
    with open(current, "w") as f:
        yaml.dump(movies_dict, f)

    if os.path.exists(previous) and archives_dir:
        Path(archives_dir).mkdir(parents=True, exist_ok=True)
        archive_name = f"collection_parsed_{time.strftime('%m-%d-%Y')}.yaml"
        shutil.move(previous, os.path.join(archives_dir, archive_name))

    shutil.move(current, previous)
