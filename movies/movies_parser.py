#!/usr/bin/env python3
import jobs.cleanup.remove_duplicates
from class_objects import Movie

from messaging.frontend import (method_launch,
                                method_exit)
from movies.movie.shows.shows_parse import parse_shows_dictionary_object


def parse_movies_in_library_and_remove_duplicates(var1,
                                                  var2,
                                                  path_array,
                                                  g):
	method_launch(g)
	if var1 or var2 is 'staging':
		jobs.cleanup.remove_duplicates.removing_duplicate_movies_from_staging(path_array,
		                                                                      var1,
		                                                                      var2,
		                                                                      g)
	else:
		jobs.cleanup.remove_duplicates.remove_duplicate_movies_that_are_not_from_staging(path_array,
		                                                                                 var1,
		                                                                                 var2,
		                                                                                 g)
	method_exit(g)


def parse_all_movies_in_yaml_dictionary(g):
	method_launch(g)
	for movie in g.movies_dictionary_object:
		movie = str(movie).replace(":", "-")
		try:
			movie_object = Movie(movie,
			                     g.movies_dictionary_object[movie],
			                     g)
		except KeyError as err:
			print(f"Key Error detected in parse all movies in yaml: {err}")
			continue
		try:
			parse_shows_dictionary_object(movie_object,
			                              g)
		except KeyError:
			continue
	sorted(g.movies_dictionary_object)
	method_exit(g)
