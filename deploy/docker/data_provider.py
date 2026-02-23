"""Single abstraction for link rules and settings: from DB when DATABASE_URL is set, else from YAML."""
from typing import Any

from config import database_url


def _use_db() -> bool:
    return bool(database_url())


def get_movies_dictionary_object() -> Any:
    if _use_db():
        from db.schema import get_movies_dict, init_db
        if init_db():
            return get_movies_dict()
    from IO.YAML.yaml_to_object import get_yaml_dictionary
    return get_yaml_dictionary()


def get_setting(category: str) -> Any:
    """Return setting by key (e.g. 'Movie Directories', 'Show Directories', 'Movie Extensions')."""
    if _use_db():
        from db.schema import get_setting as db_get, init_db
        if init_db():
            return db_get(category)
    from IO.YAML.yaml_to_object import get_variable_from_yaml
    return get_variable_from_yaml(category)


def should_persist_to_yaml() -> bool:
    """When False, the link job should not write back to YAML (state is in DB)."""
    return not _use_db()
