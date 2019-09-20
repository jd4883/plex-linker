#!/usr/bin/env python3.7
import os
import class_objects as media
from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file as dict_to_yaml
from movies.movies_parser import parse_all_movies_in_yaml_dictionary as parse_movies

if __name__ == "__main__":
	g = media.Globals()
	# need to work on assignments here, planning to pass the raw Movies, Movie, Shows, and Show dictionary respectfully
	# towards class objects for reference at init
	master_dictionary = media.Movies(os.path.abspath("/".join((str(os.environ['DOCKER_MEDIA_PATH']), g.MOVIES_PATH[0]))))
	# confirm if the above actually does anything and if so move to the class object level
	
	parse_movies(g)
	dict_to_yaml(g)
