#!/usr/bin/env python3.7
from os import (chdir,
                environ)

from messaging.backend import debug_message


def print_movie_file_quality(movie,
                             g):
	g.LOG.debug(debug_message(612,
	                          g,
	                          movie.quality))


def print_season_parsed_value(show_object,
                              g):
	g.LOG.debug(debug_message(603,
	                          g,
	                          show_object.season))


def message_exiting_function(g):
	chdir(g.MEDIA_DIRECTORY)
	g.LOG.debug(debug_message(601,
	                          g))


def display_show_class_attributes(show_object,
                                  g):
	method_launch(g)
	print_media_path_value(g)
	print_show_path_value(show_object,
	                      g)
	print_show_title_value(show_object,
	                       g)
	method_exit(g)


def print_show_title_value(show_object,
                           g):
	g.LOG.debug(debug_message(604,
	                          g,
	                          show_object.title))


def print_show_path_value(show_object,
                          g):
	g.LOG.debug(debug_message(605,
	                          g,
	                          show_object.show_paths))


def print_media_path_value(g):
	g.LOG.debug(debug_message(606,
	                          g,
	                          str(environ['DOCKER_MEDIA_PATH'])))


def message_no_items_found_to_parse(g):
	g.LOG.debug(debug_message(602,
	                          g,
	                          "Nothing to parse in this directory, add handling here, moving on to better things"))


def print_movie_extension_found_to_parse(movie,
                                         g):
	g.LOG.debug(debug_message(608,
	                          g,
	                          movie.extension))


def print_movie_file_found_to_parse(movie,
                                    g):
	g.LOG.debug(debug_message(610,
	                          g,
	                          movie.movie_file))


def method_launch(g):
	from logs.bin.get_parameters import (get_child_method_string,
	                                     get_parent_method_string)
	chdir(str(environ['DOCKER_MEDIA_PATH']))
	g.parent_method = get_parent_method_string()
	g.method = get_child_method_string()

#
# def message_entering_function(g):
# 	g.LOG.debug(debug_message(600,
# 	                          g))


def print_method_shows_dictionary_value(show_object,
                                        g):
	g.LOG.debug(debug_message(611,
	                          g,
	                          show_object.shows_dictionary_object))


def message_no_duplicates_to_remove():
	# TODO: standardize method
	print("Nothing to remove here detected as a duplicate")


def method_exit(g):
	chdir(g.MEDIA_DIRECTORY)
	message_exiting_function(g)
