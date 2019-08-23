#!/usr/bin/env python3
from os import (listdir)
from os.path import (relpath,
                     abspath,
                     exists)

from movies.movie.movie_puts import (set_absolute_movie_path,
                                     set_relative_movie_path)


def get_relative_movie_path(movie):
	try:
		movie.relative_movie_path = relpath(movie.absolute_movie_path,
		                                    movie.MEDIA_PATH)
	except ValueError:
		pass
	if movie.relative_movie_path:
		set_absolute_movie_path(movie)
		set_relative_movie_path(movie)
		return movie.relative_movie_path


def get_absolute_movie_file_path(movie):
	return "/".join((f"{movie.absolute_movie_path}",
	                 f"{movie.movie_file}"))


def get_absolute_movie_path(self,
                            path):
	return abspath("/".join((self.absolute_movies_path,
	                         path,
	                         self.absolute_movie_path)))


def get_relative_movie_file_path(movie):
	movie.absolute_movie_path = abspath(f"{movie.relative_movie_path}")
	# this is a really hackish way to fix this and should later be done in a non-patching way
	return relpath(movie.absolute_movie_path,
	               movie.MEDIA_PATH)


def get_movie_quality(quality):
	return quality


def get_movie_path(movie):
	for path in listdir(movie.absolute_movies_path):
		movie.absolute_movie_path = '/'.join((movie.absolute_movies_path,
		                                      path,
		                                      movie.movie_title))
		if exists(movie.absolute_movie_path):
			return movie.absolute_movie_path


def get_absolute_movie_subpath(absolute_movies_path,
                               path):
	return listdir("/".join((absolute_movies_path,
	                         path)))


def get_absolute_movies_parent_path(absolute_movies_path):
	return listdir(absolute_movies_path)


def get_movie_file(movie):
	return movie.movie_file


def get_movie_extensions_list_from_yaml(movies_dictionary_object):
	return movies_dictionary_object["Movie Extensions"]


def get_movie_extension(extension):
	return extension


def get_movie_dictionary_title_value(movies_dictionary_object,
                                     movie):
	return movies_dictionary_object[movie]


def get_movie_dictionary_attributes(title,
                                    absolute_movie_path,
                                    relative_movie_path):
	return {
		title: {
			"Absolute Movie Path": absolute_movie_path,
			"Relative Movie Path": relative_movie_path,
			"Shows": ""
		}  # TODO: shows should be defined here rather than being vague
	}


def get_movie_dictionary_object_parsed_without_shows(title,
                                                     absolute_movie_path,
                                                     relative_movie_path):
	return {
		title: {
			"Absolute Movie Path": absolute_movie_path,
			"Relative Movie Path": relative_movie_path
		}
	}


def get_movie_directories_from_yaml(inventoried_movies_dictionary_from_yaml):
	return inventoried_movies_dictionary_from_yaml["Movie Directories"]
