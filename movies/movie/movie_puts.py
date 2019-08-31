#!/usr/bin/env python3
from movies.movie.movie_parser import *


def set_absolute_movie_path(self,
                            g):
	g.movies_dictionary_object[self.movie_title].update({'Absolute Movie Path': self.absolute_movie_path})


def set_movie_file_and_and_extension(file, file_extension,
                                     movie,
                                     g):
	method_launch(g)
	movie.movie_file = file
	movie.extension = file_extension
	parse_extension(movie,
	                g)
	method_exit(g)


def set_movie_quality(movie,
                      g):
	from movies.movie.movie_gets import (get_movie_file,
	                                     get_movie_extension,
	                                     get_movie_quality)
	method_launch(g)
	movie.movie_file = get_movie_file(movie,
	                                  g)
	movie.extension = get_movie_extension(movie.extension,
	                                      g)
	movie.quality = get_movie_quality(movie.quality,
	                                  g)
	method_exit(g)


def set_relative_movie_path(self,
                            g):
	method_launch(g)
	g.movies_dictionary_object[self.movie_title].update({'Relative Movie Path': self.relative_movie_path})
	method_exit(g)


def init_link_target_for_movies_dictionary(movie,
                                           g):
	method_launch(g)
	if not movie['Link Target']:
		movie['Link Target'] = ""
	method_exit(g)
	return movie
