#!/usr/bin/env python3
def get_absolute_episode_status_value_from_movies_dictionary(movies_dictionary_object,
                                                             show):
	try:
		if not movies_dictionary_object['Shows'][show]['Absolute Episode']:
			movies_dictionary_object['Shows'][show]['Absolute Episode'] = False
		return movies_dictionary_object['Shows'][show]['Absolute Episode']
	except TypeError:
		return False


def get_shows_directories_from_yaml(inventoried_movies_from_yaml_file):
	return inventoried_movies_from_yaml_file["Show Directories"]
