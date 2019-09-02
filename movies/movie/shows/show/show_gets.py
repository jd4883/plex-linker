#!/usr/bin/env python3

from messaging.frontend import (
	method_exit,
	method_launch,
	print_method_shows_dictionary_value,
)
from movies.movie.shows.show.show_puts import set_show
from movies.movie.shows.show.show_validation import (validate_show_path_presence)


def get_show_root_path(show_object,
                       g):
	method_launch(g)
	method_exit(g)
	if validate_show_path_presence(show_object,
	                               g):
		return True
	return False


def get_show(show_object,
             g):
	method_launch(g)
	show_object.show_paths = g.SHOWS_PATH
	set_show(show_object,
	         g)
	print_method_shows_dictionary_value(show_object,
	                                    g)
	method_exit(g)
	return show_object


def get_fully_parsed_show_with_absolute_episode(show_object,
                                                g):
	method_launch(g)
	# noinspection LongLine
	g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Show Title'] = \
		f"{show_object.path}/{show_object.season_folder}/{show_object.show} - S{show_object.season}E{show_object.episode} (E{show_object.absolute_episode}) - {show_object.title}"
	method_exit(g)
	return g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Show Title']


def get_fully_parsed_show_without_absolute_episode(show_object,
                                                   g):
	method_launch(g)
	g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Show Title'] = \
		f"{show_object.path}/{show_object.season_folder}/{show_object.show} - " \
		f"S{show_object.season}E{show_object.episode} - {show_object.title}"
	method_exit(g)
	return g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Show Title']


def get_alphabetical_specials_string(g):
	method_launch(g)
	method_exit(g)
	return "Season 00"  # create sonarr API call here to get the name dynamically

