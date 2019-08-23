#!/usr/bin/env python3
from os import listdir
from os.path import exists

from messaging.frontend import (print_absolute_show_path)


def validate_show_path_presence(show_object):
	for show_path in show_object.show_paths:
		for path in listdir(show_path):
			show_object.path = "/".join((show_path, path,
			                             show_object.show))
			if exists(show_object.path):
				print_absolute_show_path(show_object)
				return True
	return False


def validate_ready_to_link_movie_to_show(quality):
	if quality:
		return True
	return False
