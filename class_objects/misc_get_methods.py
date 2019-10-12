#!/usr/bin/env python3
from os import environ

from IO.YAML.yaml_to_object import get_yaml_dictionary, get_variable_from_yaml


def get_movies_dictionary_object():
	return get_yaml_dictionary()


def get_shows_path():
	return get_variable_from_yaml("Show Directories")


def get_movie_extensions():
	return get_variable_from_yaml("Movie Extensions")


def get_movies_path():
	return get_variable_from_yaml("Movie Directories")


def get_host_media_path():
	return environ["HOST_MEDIA_PATH"]


def get_docker_media_path():
	return environ['DOCKER_MEDIA_PATH']


