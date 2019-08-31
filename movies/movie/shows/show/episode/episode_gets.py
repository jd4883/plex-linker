#!/usr/bin/env python3
from messaging.frontend import (method_launch,
                                method_exit,
                                print_season_parsed_value)


def get_absolute_episode_value_from_movies_dictionary(class_object,
                                                      g):
	method_launch(g)
	if not class_object.movie_dictionary_object['Shows'][class_object.show]['Absolute Episode']:
		class_object.movie_dictionary_object['Shows'][class_object.show]['Absolute Episode'] = ""
	method_exit(g)
	return class_object.movie_dictionary_object['Shows'][class_object.show]['Absolute Episode']


# adjust to work from globals
def get_anime_boolean_value_from_movies_dictionary(class_object,
                                                   g):
	method_launch(g)
	if not class_object.movie_dictionary_object['Shows'][class_object.show]['Anime']:
		class_object.movie_dictionary_object['Shows'][class_object.show]['Anime'] = False
		return False
	class_object.movie_dictionary_object['Shows'][class_object.show]['Anime'] = True
	method_exit(g)
	return True


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
		show_object.season = get_2x_padded_episode_number(show_object.season,
		                                                  g)
	else:
		show_object.season = get_alphabetical_specials_string(g)  # play with this
	# add more logic to prevent non-defined dictionary_for_shows to go through
	print_season_parsed_value(show_object,
	                          g)
	g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Season'] = show_object.season
	method_exit(g)
	return g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Season']


def get_season_folder(show_object,
                      g):
	method_launch(g)
	from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
	if show_object.season is 0 or get_alphabetical_specials_string(g):
		show_object.season_folder = get_alphabetical_specials_string(g)
	elif show_object.season:  # add error handling for isdigit
		show_object.season_folder = f"Season {get_season(show_object,g)}"
	else:
		method_exit(g)
		return
	method_exit(g)
	return show_object.season_folder


def get_season_value_from_movies_dictionary(movie_dictionary_object,
                                            show,
                                            g):
	method_launch(g)
	if not movie_dictionary_object['Shows'][show]['Season']:
		movie_dictionary_object['Shows'][show]['Season'] = ""
	method_exit(g)
	return movie_dictionary_object['Shows'][show]['Season']


def get_show_episode_number_value_from_movies_dictionary(movies_dictionary_object,
                                                         show,
                                                         g):
	method_launch(g)
	if not movies_dictionary_object['Shows'][show]['Episode']:
		movies_dictionary_object['Shows'][show]['Episode'] = ""
	method_exit(g)
	return movies_dictionary_object['Shows'][show]['Episode']


def get_show_episode_title_value_from_movies_dictionary(movies_dictionary_object,
                                                        show,
                                                        g):
	method_launch(g)
	if not movies_dictionary_object['Shows'][show]['Title']:
		movies_dictionary_object['Shows'][show]['Title'] = ""
	method_exit(g)
	return movies_dictionary_object['Shows'][show]['Title']


def get_padded_episode_number(e,
                              num,
                              g):
	method_launch(g)
	method_exit(g)
	return f"{e}".zfill(num)


def get_padded_zero_string(g):
	method_launch(g)
	method_exit(g)
	return '0'.zfill(2)
