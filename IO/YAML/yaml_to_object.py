#!/usr/bin/env python3
from os import (chdir,
                environ)

import yaml

from movies.movies_gets import (get_media_collection_parsed_last_time)


def get_yaml_dictionary():
	chdir(environ['PLEX_LINKER'])
	# may be worth making a dynamic by date backup of each config and archive the old ones since they are small
	with open(get_media_collection_parsed_last_time()) as f:
		return yaml.load(f,
		                 Loader=yaml.FullLoader)


def get_variable_from_yaml(category):
	chdir(environ['PLEX_LINKER'])
	# need to correct to relative pathing, suspect the method entry points screw this up
	with open("config_files/variables.yaml") as f:
		dictionary_object = yaml.load(f,
		                              Loader=yaml.FullLoader)
		return dictionary_object[category]
