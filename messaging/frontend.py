#!/usr/bin/env python3.7
from os import chdir

from IO.YAML.yaml_to_object import get_variable_from_yaml
from messaging.backend import debug_message


def print_method_hierarchy(method,
                           parent_method):
	return f"({parent_method} -> {method}):".ljust(60)


def print_movie_file_quality(movie):
	movie.LOG.debug(debug_message(804,
	                              movie.method,
	                              movie.parent_method,
	                              movie.quality))


def print_season_parsed_value(show_object):
	show_object.LOG.debug(debug_message(825,
	                                    show_object.method,
	                                    show_object.parent_method,
	                                    show_object.season))


def message_exiting_function(movies_object):
	chdir(get_variable_from_yaml("Media Directory"))
	movies_object.LOG.debug(debug_message(990,
	                                      movies_object.method,
	                                      movies_object.parent_method))


def print_shows_class_object_dictionary_object(shows_class_object):
	if shows_class_object.shows_dictionary_object:
		shows_class_object.LOG.info(debug_message(808,
		                                          shows_class_object.method,
		                                          shows_class_object.parent_method,
		                                          shows_class_object.shows_dictionary_object))


def print_shows(shows_class_object):
	if shows_class_object.shows and shows_class_object.title:
		shows_class_object.LOG.info(debug_message(803,
		                                          shows_class_object.method,
		                                          shows_class_object.parent_method,
		                                          shows_class_object.title,
		                                          shows_class_object.shows))


def display_show_class_attributes(show_object):
	method_launch(show_object)
	print_media_path_value(show_object)
	print_show_path_value(show_object)
	print_show_title_value(show_object)
	method_exit(show_object)


def print_show_title_value(show_object):
	show_object.LOG.debug(debug_message(820,
	                                    show_object.method,
	                                    show_object.parent_method,
	                                    show_object.title))


def print_show_path_value(show_object):
	show_object.LOG.debug(debug_message(819,
	                                    show_object.method,
	                                    show_object.parent_method,
	                                    show_object.show_paths))


def print_media_path_value(show_object):
	show_object.LOG.debug(debug_message(818,
	                                    show_object.method,
	                                    show_object.parent_method,
	                                    show_object.MEDIA_PATH))


def message_no_items_found_to_parse(items_class_objects):
	items_class_objects.LOG.debug(debug_message(981,
	                                            items_class_objects.method,
	                                            items_class_objects.parent_method,
	                                            "Nothing to parse in this directory, add handling here, \
	                                           	                            moving on to better things"))


def print_movie_extension_found_to_parse(movie):
	movie.LOG.debug(debug_message(814,
	                              movie.method,
	                              movie.parent_method,
	                              movie.extension))


def print_movie_file_found_to_parse(movie):
	movie.LOG.debug(debug_message(812,
	                              movie.method,
	                              movie.parent_method,
	                              movie.movie_file))


def method_launch(movies_parent_class_object):
	from logs.bin.get_parameters import get_child_method_string
	from logs.bin.get_parameters import get_parent_method_string
	from movies.movies_puts import set_working_directory_to_media_path
	from movies.movies_puts import set_working_directory_to_script_path
	set_working_directory_to_script_path()
	movies_parent_class_object.parent_method = get_parent_method_string()
	movies_parent_class_object.method = get_child_method_string()
	set_working_directory_to_media_path(movies_parent_class_object.MEDIA_PATH)
	message_entering_function(movies_parent_class_object)


def message_entering_function(movies_parent_class_object):
	movies_parent_class_object.LOG.debug(debug_message(991,
	                                                   movies_parent_class_object.method,
	                                                   movies_parent_class_object.parent_method))


def print_extension(movie):
	if movie.extension:
		movie.LOG.info(debug_message(805,
		                             movie.method,
		                             movie.parent_method,
		                             movie.extension))


def print_quality(movie):
	if movie.quality:
		movie.LOG.debug(debug_message(804,
		                              movie.method,
		                              movie.parent_method,
		                              movie.quality))


def print_individual_show_raw_dictionary(show_object):
	if show_object.show_raw_dictionary_for_show:
		show_object.LOG.info(debug_message(807,
		                                   show_object.method,
		                                   show_object.parent_method,
		                                   show_object.show_raw_dictionary_for_show))


def print_removing_duplicate_file(show_class_object):
	show_class_object.LOG.debug(debug_message(992,
	                                          show_class_object.method,
	                                          show_class_object.parent_method,
	                                          show_class_object.absolute_movie_path,
	                                          show_class_object.relative_show_path))


def print_media_path(movies_object):
	if movies_object.MEDIA_PATH:
		movies_object.LOG.debug(debug_message(806,
		                                      movies_object.method,
		                                      movies_object.parent_method,
		                                      movies_object.MEDIA_PATH))


def print_method_shows_dictionary_value(show_object):
	show_object.LOG.debug(debug_message(808,
	                                    show_object.method,
	                                    show_object.parent_method,
	                                    show_object.shows_dictionary_object))


def print_possible_root_paths(paths):
	paths.LOG.debug(debug_message(821,
	                              paths.method,
	                              paths.parent_method,
	                              paths.show_paths))


def print_ready_to_link_absolute_movie_path_to_relative_show_path(show_object):
	show_object.LOG.debug(debug_message(988,
	                                    show_object.method,
	                                    show_object.parent_method,
	                                    show_object.absolute_movie_file_path,
	                                    show_object.parsed_relative_title))


def print_absolute_show_path(show):
	show.LOG.debug(debug_message(822,
	                             show.method,
	                             show.parent_method,
	                             show.path))


def print_shows_dictionary(movie_object):
	movie_object.LOG.debug(debug_message(808,
	                                     movie_object.method,
	                                     movie_object.parent_method,
	                                     movie_object.shows_dictionary_object))


def message_no_duplicates_to_remove():
	# TODO: standardize method
	print("Nothing to remove here detected as a duplicate")


def print_permissions_set(path):
	path.LOG.info(debug_message(824,
	                            path.method,
	                            path.parent_method,
	                            f"PERMISSIONS SET ON",
	                            path.absolute_movie_path))


def print_validated_episode_has_an_absolute_episode_value(episode):
	episode.LOG.info(debug_message(1000,
	                               episode.method,
	                               episode.parent_method))


def method_exit(self):
	from movies.movies_puts import set_working_directory_to_script_path
	set_working_directory_to_script_path()
	message_exiting_function(self)


def print_relative_movie_path(log,
                              method,
                              parent_method,
                              relative_movies_path):
	log.debug(debug_message(801,
	                        method,
	                        parent_method,
	                        relative_movies_path),
	          )


def print_absolute_movie_path(log,
                              method,
                              parent_method,
                              absolute_movies_path):
	log.debug(debug_message(802,
	                        method,
	                        parent_method,
	                        absolute_movies_path))


def print_no_elements_in_comparison():
	return "No common elements"


def print_ready_to_link(log,
                        method,
                        parent_method,
                        symbolic_link_name,
                        target):
	log.info(debug_message(993,
	                       method,
	                       parent_method,
	                       target,
	                       symbolic_link_name))


def print_exiting_function(log,
                           method,
                           parent_method):
	log.info(debug_message(990,
	                       method,
	                       parent_method))


def print_entering_function(log,
                            method,
                            parent_method):
	log.info(debug_message(991,
	                       method,
	                       parent_method))


def print_symbolic_link_name(log,
                             method,
                             parent_method,
                             symbolic_link_name):
	log.info(debug_message(986,
	                       method,
	                       parent_method,
	                       f"SYMBOLIC LINK DESTINATION",
	                       symbolic_link_name))


def print_successfully_linked_target_to_destination(log,
                                                    method,
                                                    parent_method,
                                                    symbolic_link_name,
                                                    target):
	log.info(debug_message(982,
	                       method,
	                       parent_method,
	                       f"Linked {target} -> {symbolic_link_name}"))


def print_symbolic_link_target(log,
                               method,
                               parent_method,
                               target):
	log.info(debug_message(986,
	                       method,
	                       parent_method,
	                       f"SYMBOLIC LINK TARGET",
	                       target))


def print_absolute_media_file_path(log,
                                   method,
                                   path):
	log.debug_message(985,
	                  "MEDIA FILE",
	                  path,
	                  method)


def print_linking_show_to_movie(process):
	from os.path import relpath
	print(f'Link Success: {process}')
	# need to add log handling for this
