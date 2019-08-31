#!/usr/bin/env python3.7
from os import chdir

from messaging.backend import debug_message


def print_method_hierarchy(g):
	return f"({g.parent_method} -> {g.method}):".ljust(60)


def print_movie_file_quality(movie,
                             g):
	g.LOG.debug(debug_message(804,
	                          g,
	                          movie.quality))


def print_season_parsed_value(show_object,
                              g):
	g.LOG.debug(debug_message(825,
	                          g,
	                          show_object.season))


def message_exiting_function(g):
	chdir(g.MEDIA_DIRECTORY)
	g.LOG.debug(debug_message(990,
	                          g))


# replace shows object with dictionary
def print_shows_class_object_dictionary_object(shows_class_object,
                                               g):
	if shows_class_object.shows_dictionary_object:
		g.LOG.info(debug_message(808,
		                         g,
		                         shows_class_object.shows_dictionary_object))


# replace shows object with dictionary
def print_shows(shows_class_object,
                g):
	if shows_class_object.title:
		g.LOG.info(debug_message(803,
		                         g,
		                         shows_class_object.title,
		                         shows_class_object.shows))


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
	g.LOG.debug(debug_message(820,
	                          g,
	                          show_object.title))


def print_show_path_value(show_object,
                          g):
	g.LOG.debug(debug_message(819,
	                          g,
	                          show_object.show_paths))


def print_media_path_value(g):
	g.LOG.debug(debug_message(818,
	                          g,
	                          g.MEDIA_PATH))


def message_no_items_found_to_parse(g):
	g.LOG.debug(debug_message(981,
	                          g,
	                          "Nothing to parse in this directory, add handling here, moving on to better things"))


def print_movie_extension_found_to_parse(movie,
                                         g):
	g.LOG.debug(debug_message(814,
	                          g,
	                          movie.extension))


def print_movie_file_found_to_parse(movie,
                                    g):
	g.LOG.debug(debug_message(812,
	                          g,
	                          movie.movie_file))


def method_launch(g):
	from logs.bin.get_parameters import (get_child_method_string,
	                                     get_parent_method_string)
	from movies.movies_puts import (set_working_directory_to_media_path,
	                                set_working_directory_to_script_path)
	set_working_directory_to_script_path()
	g.parent_method = get_parent_method_string()
	g.method = get_child_method_string()
	set_working_directory_to_media_path(g.MEDIA_PATH)
	message_entering_function(g)


def message_entering_function(g):
	g.LOG.debug(debug_message(991,
	                          g))


def print_extension(movie,
                    g):
	if movie.extension:
		g.LOG.info(debug_message(805,
		                         g,
		                         movie.extension))


def print_quality(movie):
	if movie.quality:
		g.LOG.debug(debug_message(804,
		                          g,
		                          movie.quality))


def print_individual_show_raw_dictionary(show_object,
                                         g):
	if show_object.show_raw_dictionary_for_show:
		g.LOG.info(debug_message(807,
		                         g,
		                         show_object.show_raw_dictionary_for_show))


def print_removing_duplicate_file(show_class_object,
                                  g):
	g.LOG.debug(debug_message(992,
	                          g,
	                          show_class_object.absolute_movie_path,
	                          show_class_object.relative_show_path))


def print_method_shows_dictionary_value(show_object,
                                        g):
	g.LOG.debug(debug_message(808,
	                          g,
	                          show_object.shows_dictionary_object))


def print_possible_root_paths(paths,
                              g):
	g.LOG.debug(debug_message(821,
	                          g,
	                          paths.show_paths))


def print_absolute_show_path(show,
                             g):
	g.LOG.debug(debug_message(822,
	                          g,
	                          show.path))


def print_shows_dictionary(movie_object,
                           g):
	g.LOG.debug(debug_message(808,
	                          g,
	                          movie_object.shows_dictionary_object))


def message_no_duplicates_to_remove():
	# TODO: standardize method
	print("Nothing to remove here detected as a duplicate")


def print_permissions_set(path,
                          g):
	g.LOG.info(debug_message(824,
	                         g,
	                         f"PERMISSIONS SET ON",
	                         path.absolute_movie_path))


def print_validated_episode_has_an_absolute_episode_value(g):
	g.LOG.info(debug_message(1000,
	                         g))


def method_exit(g):
	from movies.movies_puts import set_working_directory_to_script_path
	set_working_directory_to_script_path()
	message_exiting_function(g)


def print_exiting_function(g):
	g.info(debug_message(990,
	                     g))


def print_entering_function(g):
	g.info(debug_message(991,
	                     g))


def print_symbolic_link_name(g,
                             symbolic_link_name):
	g.info(debug_message(986,
	                     g,
	                     f"SYMBOLIC LINK DESTINATION",
	                     symbolic_link_name))


def print_successfully_linked_target_to_destination(g,
                                                    symbolic_link_name,
                                                    target):
	g.info(debug_message(982,
	                     g,
	                     f"Linked {target} -> {symbolic_link_name}"))


def print_symbolic_link_target(g,
                               target):
	g.info(debug_message(986,
	                     g,
	                     f"SYMBOLIC LINK TARGET",
	                     target))


def print_absolute_media_file_path(g,
                                   path):
	g.debug_message(985,
	                g,
	                "MEDIA FILE",
	                path,
	                method)


def print_linking_show_to_movie(process):
	print(f'Link Success: {process}')
# need to add log handling for this
