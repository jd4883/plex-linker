#!/usr/bin/env python3
from messaging.frontend import (method_launch,
                                method_exit,
                                print_season_parsed_value)

def get_season(show_object,
               g):
	method_launch(g)
	from movies.movie.shows.show.show_gets import (get_alphabetical_specials_string)
	show_object.season = get_season_value_from_movies_dictionary(show_object.movie_dictionary_object,
	                                                             show_object.show,
	                                                             g)
	if show_object.season is int(0) \
			or get_alphabetical_specials_string(g):
		show_object.season = get_padded_zero_string(g)
	elif show_object.season.isdigit():
		show_object.season = get_padded_episode_number(show_object.season,
		                                               2,
		                                               g)
	else:
		show_object.season = str(get_alphabetical_specials_string(g))  # play with this
	# add more logic to prevent non-defined dictionary_for_shows to go through
	print_season_parsed_value(show_object,
	                          g)
	g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Season'] = show_object.season
	show_object.season = \
		g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Season'] = \
		show_object.season
	method_exit(g)
	return show_object.season


def get_season_folder(show_object,
                      g):
	method_launch(g)
	from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
	if show_object.season is 0 or get_alphabetical_specials_string(g):
		show_object.season_folder = get_alphabetical_specials_string(g)
	elif show_object.season:  # add error handling for isdigit
		show_object.season_folder = \
			f"Season {get_season(show_object, g)}"
	else:
		method_exit(g)
		return
	method_exit(g)
	g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Season Folder'] = \
		show_object.season_folder
	return show_object.season_folder


def get_season_value_from_movies_dictionary(movie_dictionary_object,
                                            show,
                                            g):
	method_launch(g)
	try:
		if not movie_dictionary_object['Shows'][show]['Season']:
			movie_dictionary_object['Shows'][show]['Season'] = str()
	except KeyError:
		movie_dictionary_object['Shows'][show]['Season'] = str()
	method_exit(g)
	return movie_dictionary_object['Shows'][show]['Season']


def get_padded_episode_number(e,
                              num,
                              g):
	method_launch(g)
	method_exit(g)
	return str(e).zfill(num)


def get_padded_zero_string(g):
	method_launch(g)
	method_exit(g)
	return str(0).zfill(2)
