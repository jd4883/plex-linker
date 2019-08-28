#!/usr/bin/env python3.7

from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Movies, Movie, Show
from movies.movies_parser import parse_all_movies_from_yaml

if __name__ == "__main__":
	full_movie_database = Movies()
	parse_all_movies_from_yaml(full_movie_database)
	write_python_dictionary_object_to_yaml_file(full_movie_database)
	
	# trick to try pre sql swap:
	# x = {a:1,b:2}
	# y = {a:1 c:3}
	# z = {**x, **y}
	# supposedly this will get a dictionary to combine with changes, gotta try adding in fields this way
