#!/usr/bin/env python3
from os import makedirs
from messaging.frontend import (method_launch,
                                method_exit)
from IO.YAML.yaml_to_object import *


def set_working_directory_to_media_path(media_directory):
	chdir(media_directory)


def set_working_directory_to_script_path():
	chdir(get_script_path())


def create_directory_if_not_present(path,
                                    g):
	method_launch(g)
	try:
		makedirs(path)
	except FileExistsError:
		pass
	method_exit(g)


def get_script_path():
	from IO.YAML.yaml_to_object import get_variable_from_yaml
	return get_variable_from_yaml("Script Path")


