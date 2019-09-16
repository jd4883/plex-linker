#!/usr/bin/env python3
from os import (makedirs)

from IO.YAML.yaml_to_object import *


def set_working_directory_to_media_path(media_directory):
	chdir(media_directory)


# noinspection PyUnusedLocal
def create_directory_if_not_present(path):
	try:
		makedirs(path)
	except FileExistsError as err:
		# print(f"create_directory_if_not_present had a KeyError{err}")  # testing
		return


# noinspection PyUnusedLocal
def set_nested_dictionary_key_value_pair(dictionary_position_key,
                                         value=str()):
	try:
		if not dictionary_position_key:
			dictionary_position_key = value
	except KeyError as err:
		# print(f"{g.method} had a KeyError{err}")  # testing
		dictionary_position_key = value
	finally:
		return dictionary_position_key
