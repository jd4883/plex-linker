#!/usr/bin/env python3
from os import chdir

import yaml

from movies.movies_gets import (get_media_collection_parsed_last_time)


def get_yaml_dictionary():
	from movies.movies_puts import set_working_directory_to_script_path
	set_working_directory_to_script_path()
	# may be worth making a dynamic by date backup of each config and archive the old ones since they are small
	with open(get_media_collection_parsed_last_time()) as f:
		return yaml.load(f)


def get_variable_from_yaml(category):
	chdir('/var/data/scripts/symlink_scripts/movie_tv_pairing')
	# need to correct to relative pathing, suspect the method entry points screw this up
	with open("config_files/variables.yaml") as f:
		dictionary_object = yaml.load(f)
		return dictionary_object[category]
