#!/usr/bin/env python3
from movies.movie.movie_parser import *


def set_absolute_movie_path(self):
	self.movies_dictionary_object[self.movie_title].update({'Absolute Movie Path': self.absolute_movie_path})


def set_movie_file_and_and_extension(file, file_extension, movie):
	movie.movie_file = file
	movie.extension = file_extension
	parse_extension(movie)


def set_movie_quality(movie):
	from movies.movie.movie_gets import (get_movie_file,
	                                     get_movie_extension,
	                                     get_movie_quality)
	movie.movie_file = get_movie_file(movie)
	movie.extension = get_movie_extension(movie.extension)
	movie.quality = get_movie_quality(movie.quality)


def set_relative_movie_path(self):
	self.movies_dictionary_object[self.movie_title].update({'Relative Movie Path': self.relative_movie_path})


def init_link_target_for_movies_dictionary(movie):
	if not movie['Link Target']:
		movie['Link Target'] = ""
	return movie
