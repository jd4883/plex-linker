#!/usr/bin/env python3.7

from messaging.frontend import (method_launch,
                                method_exit)
from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Movies, Movie
from movies.movie.movie_puts import init_link_target_for_movies_dictionary
from movies.movie.shows.shows_parse import parse_shows_dictionary_object
from movies.movies_puts import set_working_directory_to_media_path
from class_objects import Globals

if __name__ == "__main__":
	g = Globals()
	full_movie_database = Movies(g)
	set_working_directory_to_media_path(g.MEDIA_PATH)
	for movie in g.movies_dictionary_object:
		init_link_target_for_movies_dictionary(g.movies_dictionary_object[movie],
		                                       g)
		if g.movies_dictionary_object[movie]['Shows']:
			parse_shows_dictionary_object(Movie(movie,
			                                    g),
			                              g)
	
	sorted(g.movies_dictionary_object)
	write_python_dictionary_object_to_yaml_file(g)
