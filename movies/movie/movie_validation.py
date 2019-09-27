#!/usr/bin/env python3
import os.path

from jobs.set_path_permissions import (set_permissions)
import messaging.frontend as message
from movies.movie.movie_puts import (set_movie_file_and_extension)


def validate_extensions_from_movie_file(movie, g):
	if validate_movie_extension(movie, g):
		movie.absolute_movie_file_path = "/".join((movie.absolute_movie_path, movie.movie_file))
		set_permissions(movie, g)
		message.print_movie_file_quality(movie, g)


def validate_movie_extension(movie, g):
	if os.path.exists(movie.absolute_movie_path):
		for file in os.listdir(movie.absolute_movie_path):
			for file_extension in g.MOVIE_EXTENSIONS:
				if file.endswith(file_extension):
					set_movie_file_and_extension(file, file_extension, movie, g)
					return True
	return False


def validated_movie_path_is_not_null(movie):
	if movie.absolute_movie_path:
		return True
	return False
