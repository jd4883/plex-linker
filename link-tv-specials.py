#!/usr/bin/env python3.7

from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Globals, \
	Movies
from movies.movies_parser import parse_all_movies_in_yaml_dictionary

def write_linked_movies(globals_class_object):
	with open(str('/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/list_of_linked_movies.txt'),
	          'w+') as filehandle:
		for item in globals_class_object.list_of_linked_movies:
			filehandle.write('%s\n' % item)


def write_movies_to_find(globals_class_object):
	with open(str('/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/list_of_movies_to_find.txt'),
	          'w+') as filehandle:
		for item in globals_class_object.list_of_movies_to_locate:
			filehandle.write('%s\n' % item)


if __name__ == "__main__":
	g = Globals()
	full_movie_database = Movies(g)
	parse_all_movies_in_yaml_dictionary(g)
	write_python_dictionary_object_to_yaml_file(g)
	
	write_linked_movies(g)
	write_movies_to_find(g)
