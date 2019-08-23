#!/usr/bin/env python3.7

from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Movies
from movies.movies_parser import parse_all_movies_from_yaml

if __name__ == "__main__":
	full_movie_database = Movies()
	parse_all_movies_from_yaml(full_movie_database)
	write_python_dictionary_object_to_yaml_file(full_movie_database)
