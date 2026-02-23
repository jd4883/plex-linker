"""Parse movie→show mapping and create symlinks; trigger Sonarr/Radarr refresh after link."""
import os

import methods
from jobs.set_path_permissions import (
    set_file_mask_with_chmod_on_files_and_links,
    set_ownership_on_files_and_links,
)
from jobs.symlinking import symlink_force
from messaging import frontend as message


def parse_shows_dictionary_object(movie, g):
    message.method_launch(g)
    if not movie.shows_dictionary:
        return
    for series in movie.shows_dictionary:
        if not isinstance(movie.shows_dictionary.get(series), dict):
            continue
        show = methods.Show(g, series, movie.shows_dictionary[series], movie.movie_dictionary)
        if not g.sonarr.lookup_series(show):
            continue
        show.initShow(movie, g)
        symlink_force(movie, show, g)
        message.method_launch(g)
        directory = os.environ.get("DOCKER_MEDIA_PATH", g.MEDIA_PATH)
        try:
            os.chdir(directory)
            set_file_mask_with_chmod_on_files_and_links(movie.absolute_movie_file_path, g)
            set_ownership_on_files_and_links(movie.absolute_movie_file_path)
        except (FileNotFoundError, NotADirectoryError, OSError):
            pass
    try:
        g.radarr.rescan_movie(movie.movieId)
    except Exception:
        pass
