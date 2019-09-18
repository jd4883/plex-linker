#!/usr/bin/env python3
from os import (chdir,
                environ)
from os.path import (relpath)


def get_media_collection_parsed_last_time():
	chdir(environ['PLEX_LINKER'])
	return "config_files/media_collection_parsed_last_run.yaml"


def get_media_collection_parsed_archives():
	chdir(environ['PLEX_LINKER'])
	return str(environ['CONFIG_ARCHIVES'])


def get_relative_movies_path(self):
	return relpath(self.absolute_movies_path,
	               str(environ['DOCKER_MEDIA_PATH']))

#
#
# def get_intersection_between_lists(a_set, b_set):
# 	return a_set & b_set
# future method for adding movies library from disk
