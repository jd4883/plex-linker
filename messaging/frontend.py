#!/usr/bin/env python3.7
import os
import logs.bin.get_parameters as parameters

from messaging.backend import debug_message


def print_movie_file_quality(movie, g):
	g.LOG.debug(debug_message(612, g, movie.quality))


def message_exiting_function(g):
	os.chdir(g.MEDIA_DIRECTORY)
	g.LOG.debug(debug_message(601, g))


# def display_show_class_attributes(show_object,
#                                   g):
# 	method_launch(g)
# 	print_media_path_value(g)
# 	print_show_path_value(show_object, g)
# 	print_show_title_value(show_object, g)
# 	method_exit(g)


def print_show_title_value(show_object, g):
	g.LOG.debug(debug_message(604, g, show_object.title))


def print_show_path_value(show_object, g):
	g.LOG.debug(debug_message(605, g, show_object.show_paths))


def print_media_path_value(g):
	g.LOG.debug(debug_message(606, g, str(os.environ['DOCKER_MEDIA_PATH'])))


def message_no_items_found_to_parse(g):
	g.LOG.debug(debug_message(602, g, "Nothing to parse in this directory, add handling here, moving on to better things"))


def print_movie_extension_found_to_parse(movie, g):
	g.LOG.debug(debug_message(608, g, movie.extension))


def print_movie_file_found_to_parse(movie, g):
	g.LOG.debug(debug_message(610, g, movie.movie_file))


def method_launch(g):
	os.chdir(str(os.environ['DOCKER_MEDIA_PATH']))
	g.parent_method = parameters.get_parent_method_string()
	g.method = parameters.get_child_method_string()


def message_no_duplicates_to_remove():
	# TODO: standardize method
	print("Nothing to remove here detected as a duplicate")


def method_exit(g):
	os.chdir(g.MEDIA_DIRECTORY)
	message_exiting_function(g)
