#!/usr/bin/env python3
from os import (listdir)
from os.path import (relpath,
                     abspath,
                     exists)

from messaging.frontend import (method_launch,
                                method_exit)
from movies.movie.movie_puts import (set_absolute_movie_path,
                                     set_relative_movie_path)


def get_relative_movie_path(movie,
                            g):
	method_launch(g)
	try:
		movie.relative_movie_path = relpath(movie.absolute_movie_path,
		                                    g.MEDIA_PATH)
	except ValueError:
		pass
	if movie.relative_movie_path:
		set_absolute_movie_path(movie,
		                        g)
		set_relative_movie_path(movie,
		                        g)
		method_exit(g)
		return movie.relative_movie_path
	method_exit(g)
	return ""


def get_absolute_movie_file_path(movie,
                                 g):
	method_launch(g)
	method_exit(g)
	return "/".join((str(movie.absolute_movie_path),
	                 str(movie.movie_file)))


def get_absolute_movie_path(self,
                            path,
                            g):
	method_launch(g)
	method_exit(g)
	return abspath("/".join((self.absolute_movies_path,
	                         path,
	                         self.absolute_movie_path)))


def get_relative_movie_file_path(movie,
                                 g):
	method_launch(g)
	movie.absolute_movie_path = abspath(str(movie.relative_movie_path))
	# this is a really hackish way to fix this and should later be done in a non-patching way
	method_exit(g)
	return relpath(movie.absolute_movie_path,
	               g.MEDIA_PATH)


def get_movie_quality(quality,
                      g):
	method_launch(g)
	method_exit(g)
	return quality


def get_movie_path(movie,
                   g):
	method_launch(g)
	for path in listdir(movie.absolute_movies_path):
		movie.absolute_movie_path = '/'.join((movie.absolute_movies_path,
		                                      path,
		                                      movie.movie_title))
		if exists(movie.absolute_movie_path):
			method_exit(g)
			return movie.absolute_movie_path
	method_exit(g)
	return ""


def get_absolute_movie_subpath(absolute_movies_path,
                               path,
                               g):
	method_launch(g)
	method_exit(g)
	return listdir("/".join((absolute_movies_path,
	                         path)))


def get_absolute_movies_parent_path(absolute_movies_path,
                                    g):
	method_launch(g)
	method_exit(g)
	return listdir(absolute_movies_path)


def get_movie_file(movie,
                   g):
	method_launch(g)
	method_exit(g)
	return movie.movie_file


def get_movie_extension(extension,
                        g):
	method_launch(g)
	method_exit(g)
	return extension

#
# def get_movie_directories_from_yaml(inventoried_movies_dictionary_from_yaml):
# 	return inventoried_movies_dictionary_from_yaml["Movie Directories"]


def get_unparsed_movie_title(title,
                             g):
	method_launch(g)
	try:
		g.movies_dictionary_object[title]['Unparsed Movie Title'] = title
	except KeyError:
		g.movies_dictionary_object[title]['Unparsed Movie Title'] = {}
		g.movies_dictionary_object[title]['Unparsed Movie Title'] = ""
	finally:
		method_exit(g)
		return g.movies_dictionary_object[title]['Unparsed Movie Title']
