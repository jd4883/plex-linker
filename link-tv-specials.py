#!/usr/bin/env python3.7

from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Movies, Movie
from movies.movie.movie_puts import init_link_target_for_movies_dictionary
from movies.movie.shows.shows_parse import parse_shows_dictionary_object

if __name__ == "__main__":
	full_movie_database = Movies()
	for movie in full_movie_database.movies_dictionary_object:
		individual_movie_dictionary = Movie(movie)
		init_link_target_for_movies_dictionary(full_movie_database.movies_dictionary_object[movie])
		parse_shows_dictionary_object(individual_movie_dictionary)
		
	write_python_dictionary_object_to_yaml_file(full_movie_database)
