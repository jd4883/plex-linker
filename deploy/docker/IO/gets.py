"""Paths for parsed collection YAML (this run vs last run)."""
import os

from config import config_root


def get_collection_absolute_path_parsed_this_run() -> str:
    root = config_root()
    if not root:
        return os.environ.get("YAML_FILE_CURRENT", "config_files/media_collection_parsed_this_run.yaml")
    return os.path.join(root, "config_files", "media_collection_parsed_this_run.yaml")


def get_collection_absolute_path_parsed_last_run() -> str:
    root = config_root()
    if not root:
        return os.environ.get("YAML_FILE_PREVIOUS", "config_files/media_collection_parsed_last_run.yaml")
    return os.path.join(root, "config_files", "media_collection_parsed_last_run.yaml")
