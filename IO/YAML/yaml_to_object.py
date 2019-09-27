#!/usr/bin/env python3
import os
import yaml
import movies.movies_gets as movies_gets


def get_yaml_dictionary():
	os.chdir(os.environ['PLEX_LINKER'])
	with open(movies_gets.parsed_collection()) as f:
		return yaml.load(f, Loader=yaml.FullLoader)


def get_variable_from_yaml(category):
	os.chdir(os.environ['PLEX_LINKER'])
	with open("config_files/variables.yaml") as f:
		dictionary_object = yaml.load(f, Loader=yaml.FullLoader)
		return dictionary_object[category]
