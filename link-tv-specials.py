#!/usr/bin/env python3.7
from class_objects.sonarr_api import *
from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Globals, \
	Movies
from movies.movies_parser import parse_all_movies_in_yaml_dictionary


if __name__ == "__main__":
	g = Globals()
	sonarr = SonarrAPI()
	print(sonarr.get_series())
	print(sonarr.lookup_series('Breaking Bad'))
	full_movie_database = Movies(g)
	parse_all_movies_in_yaml_dictionary(g)
	write_python_dictionary_object_to_yaml_file(g)
