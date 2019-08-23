#!/usr/bin/env python3
from messaging.frontend import (method_launch,
                                method_exit,
                                print_season_parsed_value)


def get_absolute_episode_value_from_movies_dictionary(class_object):
	if not class_object.movie_dictionary_object['Shows'][class_object.show]['Absolute Episode']:
		class_object.movie_dictionary_object['Shows'][class_object.show]['Absolute Episode'] = ""
	return class_object.movie_dictionary_object['Shows'][class_object.show]['Absolute Episode']


def get_anime_boolean_value_from_movies_dictionary(class_object):
	if not class_object.movie_dictionary_object['Shows'][class_object.show]['Anime']:
		class_object.movie_dictionary_object['Shows'][class_object.show]['Anime'] = False
	class_object.movie_dictionary_object['Shows'][class_object.show]['Anime'] = True
	return class_object.movie_dictionary_object['Shows'][class_object.show]['Anime']


def get_season(show_object):
	method_launch(show_object)
	from movies.movie.shows.show.show_gets import (get_alphabetical_specials_string)
	show_object.season = get_season_value_from_movies_dictionary(show_object.movie_dictionary_object,
	                                                             show_object.show)
	if show_object.season is 0 \
			or get_alphabetical_specials_string():
		show_object.season = get_padded_zero_string()
	elif show_object.season.isdigit():
		show_object.season = get_2x_padded_episode_number(show_object.season)
	else:
		show_object.season = get_alphabetical_specials_string()  # play with this
	# add more logic to prevent non-defined dictionary_for_shows to go through
	print_season_parsed_value(show_object)
	method_exit(show_object)
	return show_object.season


def get_season_folder(show_object):
	method_launch(show_object)
	from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
	if show_object.season is 0 or get_alphabetical_specials_string():
		show_object.season_folder = get_alphabetical_specials_string()
	elif show_object.season:  # add error handling for isdigit
		show_object.season_folder = f"Season {get_season(show_object)}"
	else:
		method_exit(show_object)
		return
	method_exit(show_object)
	return show_object.season_folder


def get_season_folder_value_from_movies_dictionary(movies_dictionary_object,
                                                   show):
	if not movies_dictionary_object['Shows'][show]['Season Folder']:
		movies_dictionary_object['Shows'][show]['Season Folder'] = ""
	return movies_dictionary_object['Shows'][show]['Season Folder']


def get_season_value_from_movies_dictionary(movie_dictionary_object,
                                            show):
	if not movie_dictionary_object['Shows'][show]['Season']:
		movie_dictionary_object['Shows'][show]['Season'] = ""
	return movie_dictionary_object['Shows'][show]['Season']


def get_show_episode_number_value_from_movies_dictionary(movies_dictionary_object,
                                                         show):
	if not movies_dictionary_object['Shows'][show]['Episode']:
		movies_dictionary_object['Shows'][show]['Episode'] = ""
	return movies_dictionary_object['Shows'][show]['Episode']


def get_show_episode_title_value_from_movies_dictionary(movies_dictionary_object,
                                                        show):
	if not movies_dictionary_object['Shows'][show]['Title']:
		movies_dictionary_object['Shows'][show]['Title'] = ""
	return movies_dictionary_object['Shows'][show]['Title']


def get_padded_episode_number(e,
                              num):
	return f"{e}".zfill(num)


def get_padded_zero_string():
	return '0'.zfill(2)
