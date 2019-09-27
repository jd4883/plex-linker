#!/usr/bin/env python3
import class_objects as media
import messaging.frontend as message
from movies.movie.shows.shows_parse import parse_shows_dictionary_object as parse_shows

#
# def parse_movies_in_library_and_remove_duplicates(var1, var2, path_array, g):
# 	message.method_launch(g)
# 	if var1 or var2 is 'staging':
# 		duplicate_handling.removing_duplicate_movies_from_staging(path_array, var1, var2, g)
# 	else:
# 		duplicate_handling.remove_duplicate_movies_that_are_not_from_staging(path_array, var1, var2, g)
# 	message.method_exit(g)


def parse_all_movies_in_yaml_dictionary(g):
	message.method_launch(g)
	for movie in g.movies_dictionary_object:
		movie = str(movie).replace(":", "-")
		try:
			self = media.Movie(movie, g.movies_dictionary_object[movie], g)
		except KeyError as err:
			print(f"Key Error detected in parse all movies in yaml: {err}")
			continue
		try:
			parse_shows(self, g)
		except KeyError:
			continue
	sorted(g.movies_dictionary_object)
	message.method_exit(g)
