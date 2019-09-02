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
                      globals_class_object):
	from movies.movie.movie_gets import (get_movie_file,
	                                     get_movie_extension,
	                                     get_movie_quality)
	method_launch(globals_class_object)
	movie.movie_file = \
		globals_class_object.movies_dictionary_object[movie.movie_title]['Parsed Movie File'] = \
		str(get_movie_file(movie,
		                   globals_class_object))
	movie.extension = \
		globals_class_object.movies_dictionary_object[movie.movie_title]['Parsed Movie Extension'] = \
		str(get_movie_extension(movie.extension,
		                        globals_class_object))
	movie.quality = \
		globals_class_object.movies_dictionary_object[movie.movie_title]['Parsed Movie Quality'] = \
		str(get_movie_quality(movie.quality,
		                      globals_class_object))
	method_exit(globals_class_object)


def set_relative_movie_path(self,
                            globals_class_object):
	method_launch(globals_class_object)
	# noinspection LongLine
	globals_class_object.movies_dictionary_object[self.movie_title].update(
		{'Relative Movie Path': self.relative_movie_path})
	method_exit(globals_class_object)


def init_link_target_for_movies_dictionary(movie_class_object,
                                           globals_class_object):
	method_launch(globals_class_object)
	movie_class_object['Symlink Target'] = \
		str()
	if not movie_class_object['Symlink Target']:
		movie_class_object['Symlink Target'] = \
			str()
	method_exit(globals_class_object)
	return movie_class_object
