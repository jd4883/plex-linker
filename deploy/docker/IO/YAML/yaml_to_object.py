"""Load YAML config from config root."""
import os
import yaml

from config import config_root


def _config_path(*parts: str) -> str:
    root = config_root()
    return os.path.join(root, *parts) if root else ""


def get_yaml_dictionary():
    path = _config_path("config_files", "media_collection_parsed_last_run.yaml")
    with open(path) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_variable_from_yaml(category: str):
    path = _config_path("config_files", "variables.yaml")
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data.get(category)
