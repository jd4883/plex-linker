#!/usr/bin/env python3
from os import chdir

import yaml
from movies.movies_gets import (get_media_collection_parsed_this_time,
                                get_media_collection_parsed_last_time,
                                get_media_collection_parsed_archives)

def get_media_path_from_yaml(movies_dictionary):
	return movies_dictionary["Media Directory"]


def get_movies_dictionary_from_yaml(movies_dictionary):
	return movies_dictionary["Movies"]


def get_yaml_dictionary():
	chdir(get_variable_from_yaml('Script Path'))
	# may be worth making a dynamic by date backup of each config and archive the old ones since they are small
	with open(get_media_collection_parsed_last_time(),
	          'r') as f:
		return yaml.load(f)


def get_variable_from_yaml(category):
	
	chdir('/var/data/scripts/symlink_scripts/movie_tv_pairing')
	# need to correct to relative pathing, suspect the method entry points screw this up
	with open("config_files/variables.yaml",
	          'r') as f:
		dictionary_object = yaml.load(f)
		return dictionary_object[category]
