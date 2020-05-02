from IO.YAML.yaml_to_object import get_variable_from_yaml, get_yaml_dictionary


def get_movies_dictionary_object():
	return get_yaml_dictionary()


def get_shows_path():
	return get_variable_from_yaml("Show Directories")


def get_movie_extensions():
	return get_variable_from_yaml("Movie Extensions")


def get_movies_path():
	return get_variable_from_yaml("Movie Directories")
