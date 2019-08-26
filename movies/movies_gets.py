#!/usr/bin/env python3
from os.path import relpath, abspath


def get_media_collection_parsed_this_time():
	return "config_files/media_collection_parsed_this_run.yaml"


def get_media_collection_parsed_last_time():
	return "config_files/media_collection_parsed_last_run.yaml"

def get_media_collection_parsed_archives():
	return "config_files/archives"

def get_relative_movies_path(self):
	return relpath(self.absolute_movies_path,
	               self.MEDIA_PATH)


def get_absolute_movies_path(self):
	return abspath("/".join((self.MEDIA_PATH,
	                         self.MOVIES_PATH[0])))
#
#
# def get_intersection_between_lists(a_set, b_set):
# 	return a_set & b_set
# future method for adding movies library from disk