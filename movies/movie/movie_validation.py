#!/usr/bin/env python3
import jobs.cleanup
import logs.bin
from jobs.set_path_permissions import (set_permissions)
from messaging.frontend import (method_launch,
                                print_movie_file_quality,
                                message_no_items_found_to_parse,
                                debug_message,
                                message_exiting_function)
from movies.movie.movie_puts import (set_movie_file_and_and_extension)


def validate_extensions_from_movie_file(movie):
	method_launch(movie)
	if validate_movie_extension(movie):
		movie.absolute_movie_file_path = "/".join((movie.absolute_movie_path,
		                                           movie.movie_file))
		set_permissions(movie)
		# validate permissions are updating, do some testing here
		print_movie_file_quality(movie)


def validate_movie_extension(movie):
	method_launch(movie)
	from os import listdir
	for file in listdir(movie.absolute_movie_path):
		movie.LOG.debug(debug_message(815,
		                              movie.method,
		                              movie.parent_method,
		                              file))
		for file_extension in movie.MOVIE_EXTENSIONS:
			movie.LOG.debug(debug_message(813,
			                              movie.method,
			                              movie.parent_method,
			                              file_extension))
			if file.endswith(file_extension):
				set_movie_file_and_and_extension(file, file_extension, movie)
				return True
		message_exiting_function(movie)
	return False


def validate_file(file,
                  log,
                  parent_method):
	import sys
	from os.path import exists
	from messaging import debug_message
	method = logs.bin.get_parameters.format_string(f"{sys._getframe().f_code.co_name}")
	log.debug(debug_message(991,
	                        method,
	                        parent_method))
	log.debug(debug_message(990,
	                        method,
	                        parent_method))
	if exists(file):
		return True
	return False


def validated_movie_path_is_not_null(movie):
	from os import listdir
	if movie.absolute_movie_path:
		try:
			if len(listdir(movie.absolute_movie_path)) == 0 or \
					movie.absolute_movie_path.endswith("None" or None) \
					or (movie.absolute_movie_path == "" or None \
					    or movie.absolute_movie_path.endswith("None")):
				message_no_items_found_to_parse(movie)
				print(f"Absolute Movie Path not parsed: {movie.absolute_movie_path}")
				return False
		except FileNotFoundError:
			return False
	return True


def validate_path(path,
                  log,
                  parent_method):
	from os.path import exists
	from messaging import debug_message
	import sys
	method = logs.bin.get_parameters.format_string(f"{sys._getframe().f_code.co_name}")
	log.debug(debug_message(991,
	                        method,
	                        parent_method))
	if exists(path):
		from os import listdir
		for _ in listdir(path):  # this looks redundant to loop
			log.debug(debug_message(990,
			                        method,
			                        parent_method))
			return True
	log.debug(debug_message(990,
	                        method,
	                        parent_method))
	return False


def validate_duplicates_and_handle_them_if_needed(list_of_possible_paths1,
                                                  list_of_possible_paths):
	if len(list_of_possible_paths) > 1:
		# add real messaging handler here
		print(f"{list_of_possible_paths1} triggered a duplicate check")
		jobs.cleanup.remove_duplicates.remove_duplicates(list_of_possible_paths)
		print("made it past paths")
