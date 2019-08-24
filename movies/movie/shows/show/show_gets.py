#!/usr/bin/env python3

from messaging.frontend import (method_exit,
                                method_launch,
                                print_method_shows_dictionary_value,
                                print_shows_dictionary)
from movies.movie.shows.show.show_puts import set_show
from movies.movie.shows.show.show_validation import (validate_show_path_presence)


def get_symlink_status_value_from_movies_dictionary(movies_dictionary_object,
                                                    show):
	if not movies_dictionary_object['Shows'][show]['Symlink Status']:
		movies_dictionary_object['Shows'][show]['Symlink Status'] = False
	return movies_dictionary_object['Shows'][show]['Symlink Status']


def get_show_root_path(show_object):
	method_launch(show_object)
	method_exit(show_object)
	if validate_show_path_presence(show_object):
		return True
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


def get_relative_episode_value_from_movies_dictionary(movies_dictionary_object,
                                                      show):
	if not movies_dictionary_object['Shows'][show]['Absolute Episode Path']:
		movies_dictionary_object['Shows'][show]['Absolute Episode Path'] = ""
	return movies_dictionary_object['Shows'][show]['Absolute Episode Path']


def get_populated_show_dictionary_object(show_object):
	method_launch(show_object)
	return {[
		{"Absolute Episode Path": show_object.absolute_movie_path},  # 0
		{"Relative Episode Path": show_object.relative_show_path},  # 1
		{"Season": show_object.season},  # 2
		{"Parsed Title": show_object.title},  # 3
		{"Absolute Episode Status": show_object.absolute_episode},  # 4
		{"Anime Status": show_object.anime_status},  # 5
		{"Linked Path": show_object.live_linked_path},  # 6
		{"Episode": show_object.episode}]}  # 7


def get_fully_parsed_show_with_absolute_episode(show_object):
	return f"{show_object.path}/{show_object.season_folder}/{show_object.show} - S{show_object.season}E{show_object.episode} (E{show_object.absolute_episode}) - {show_object.title}"


def get_fully_parsed_show_without_absolute_episode(show_object):
	return f"{show_object.path}/{show_object.season_folder}/{show_object.show} - S{show_object.season}E{show_object.episode} - {show_object.title}"


def get_alphabetical_specials_string():
	return "Season 00"
	#return "Specials"
