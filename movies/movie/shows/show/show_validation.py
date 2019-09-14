#!/usr/bin/env python3
from os import listdir, chdir
from os.path import exists

from messaging.frontend import (method_launch,
                                method_exit)
from string_manipulation.string_methods import getCaseInsensitivePath


def validate_show_path_presence(show_object,
                                g):
	method_launch(g)
	chdir('/media')
	for show_path in show_object.show_paths:
		for path in listdir(show_path):
			show_object.path = "/".join((show_path, path,
			                             show_object.show))
			if exists(getCaseInsensitivePath(show_object.path)):
				method_exit(g)
				return True
	method_exit(g)
	return False


def validate_ready_to_link_movie_to_show(quality,
                                         g):
	method_launch(g)
	if quality:
		method_exit(g)
		return True
	method_exit(g)
	return False
