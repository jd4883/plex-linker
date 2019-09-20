#!/usr/bin/env python3
from os import listdir, chdir
from os.path import exists

import messaging.frontend as message
from string_manipulation.string_methods import getCaseInsensitivePath


def validate_show_path_presence(show_object,
                                g):
	message.method_launch(g)
	chdir('/media')
	for show_path in show_object.show_paths:
		for path in listdir(show_path):
			show_object.path = "/".join((show_path, path,
			                             show_object.show))
			if exists(getCaseInsensitivePath(show_object.path)):
				message.method_exit(g)
				return True
	message.method_exit(g)
	return False


def validate_ready_to_link_movie_to_show(quality):
	if quality:
		return True
	return False
