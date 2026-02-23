"""Path and movie dict access: from DB when DATABASE_URL is set, else from YAML."""
from data_provider import get_movies_dictionary_object as _get_movies_dict
from data_provider import get_setting


def get_movies_dictionary_object():
    return _get_movies_dict()


def get_shows_path():
    return get_setting("Show Directories")


def get_movie_extensions():
    return get_setting("Movie Extensions")


def get_movies_path():
    return get_setting("Movie Directories")
