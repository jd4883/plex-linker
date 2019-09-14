#!/usr/bin/env python3
from jobs.set_path_permissions import (set_permissions)
from messaging.frontend import (method_launch,
                                method_exit,
                                print_movie_file_quality,
                                message_no_items_found_to_parse,
                                debug_message,
                                message_exiting_function)
from movies.movie.movie_puts import (set_movie_file_and_and_extension)


def validate_extensions_from_movie_file(movie,
                                        g):
	method_launch(g)
	if validate_movie_extension(movie,
	                            g):
		movie.absolute_movie_file_path = "/".join((movie.absolute_movie_path,
		                                           movie.movie_file))
		
		set_permissions(movie,
		                g)
		print_movie_file_quality(movie,
		                         g)
	method_exit(g)


def validate_movie_extension(movie,
                             g):
	method_launch(g)
	from os import listdir
	for file in listdir(movie.absolute_movie_path):
		g.LOG.debug(debug_message(607,
		                          g,
		                          file))
		for file_extension in g.MOVIE_EXTENSIONS:
			g.LOG.debug(debug_message(609,
			                          g,
			                          file_extension))
			if file.endswith(file_extension):
				set_movie_file_and_and_extension(file,
				                                 file_extension,
				                                 movie,
				                                 g)
				return True
	message_exiting_function(g)
	return False


# noinspection PyDeepBugsBinOperand
def validated_movie_path_is_not_null(movie,
                                     g):
	from os import listdir
	method_launch(g)
	if movie.absolute_movie_path:
		try:
			if len(listdir(movie.absolute_movie_path)) == 0 or \
					movie.absolute_movie_path.endswith("None" or None) \
					or (movie.absolute_movie_path == str() or None \
					    or movie.absolute_movie_path.endswith("None")):
				message_no_items_found_to_parse(g)
				method_exit(g)
				return False
		except FileNotFoundError:
			method_exit(g)
			return False
	method_exit(g)
	return True
