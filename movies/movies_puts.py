#!/usr/bin/env python3
from os import makedirs

from IO.YAML.yaml_to_object import *


def set_working_directory_to_media_path(media_directory):
	chdir(media_directory)


def set_working_directory_to_script_path():
	chdir(get_script_path())


def create_directory_if_not_present(path,
                                    g):
	try:
		makedirs(path)
	except FileExistsError:
		pass


def get_script_path():
	return '/config'


def set_nested_dictionary_key_value_pair(g,
                                         dictionary_position_key,
                                         value=str()):
	# this helper method takes in a key and the default desired value. It then checks if the key is defined,
	# and if not it creates the key and assigns the default value. It returns the value as the data type that was fed in
	# it is good best practice to type the variables passed to this function to ensure everything is parsed properly
	try:
		if not dictionary_position_key:
			dictionary_position_key = value
	except KeyError:
		dictionary_position_key = value
	finally:
		return dictionary_position_key
