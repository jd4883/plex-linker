#!/usr/bin/env python3

from messaging.frontend import (
	method_exit,
	method_launch,
	print_method_shows_dictionary_value,
	print_shows_dictionary,
	)
from movies.movie.shows.show.show_puts import set_show
from movies.movie.shows.show.show_validation import (validate_show_path_presence)


def get_show_root_path(show_object):
	try:
		if validate_show_path_presence(show_object):
			return True
		return False
	except TypeError:
		return False


def get_show(show_object):
	method_launch(show_object)
	show_object.show_paths = show_object.SHOWS_PATH
	set_show(show_object)
	print_method_shows_dictionary_value(show_object)
	method_exit(show_object)
	return show_object


def create_tv_show_class_object(movie_object,
                                show):
	from modules import Show
	method_launch(movie_object)
	tv_show_class_object = Show(show,
	                            movie_object.movie_title)
	tv_show_class_object.show = show
	get_show(tv_show_class_object)
	print_shows_dictionary(movie_object)
	method_exit(movie_object)
	return tv_show_class_object


def get_fully_parsed_show_with_absolute_episode(show_object):
	return f"{show_object.path}/{show_object.season_folder}/{show_object.show} - S{show_object.season}E{show_object.episode} (E{show_object.absolute_episode}) - {show_object.title}"


def get_fully_parsed_show_without_absolute_episode(show_object):
	return f"{show_object.path}/{show_object.season_folder}/{show_object.show} - S{show_object.season}E{show_object.episode} - {show_object.title}"


def get_alphabetical_specials_string():
	return "Season 00"  # create sonarr API call here to get the name dynamically
