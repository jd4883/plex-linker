from os import (makedirs)


def create_directory_if_not_present(path):
	try:
		makedirs(path)
	except FileExistsError:
		return


def set_nested_dictionary_key_value_pair(dictionary_position_key, value=str()):
	try:
		if not dictionary_position_key:
			dictionary_position_key = value
	except KeyError:
		dictionary_position_key = value
	finally:
		return dictionary_position_key
