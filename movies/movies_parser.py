#!/usr/bin/env python3
import jobs.cleanup.remove_duplicates
from messaging.frontend import (method_exit,
                                method_launch)
from movies.movie.shows.shows_parse import (parse_shows_dictionary_object)


def parse_all_movies_from_yaml(movie_class_object):
	from class_objects import Movie
	method_launch(movie_class_object)
	for movie in movie_class_object.movies_dictionary_object:
		individual_movie_dictionary = Movie(movie)
		try:
			parse_shows_dictionary_object(individual_movie_dictionary)
		except AttributeError:
			continue
	method_exit(movie_class_object)


def parse_movies_in_library_and_remove_duplicates(var1,
                                                  var2,
                                                  path_array):
	if var1 or var2 is 'staging':
		jobs.cleanup.remove_duplicates.removing_duplicate_movies_from_staging(path_array,
		                                                                      var1,
		                                                                      var2)
	else:
		jobs.cleanup.remove_duplicates.remove_duplicate_movies_that_are_not_from_staging(
			path_array,
			var1,
			var2)
