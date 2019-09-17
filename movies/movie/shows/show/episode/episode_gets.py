#!/usr/bin/env python3
from messaging.frontend import (method_launch,
                                method_exit)


def get_season(self,
               g):
	method_launch(g)
	from movies.movie.shows.show.show_gets import (get_alphabetical_specials_string)
	if not g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Season'] and \
			g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Season']:
		g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Parsed Season'] = \
			get_season_value_from_movies_dictionary(self.movie_dictionary_object,
		                                                             self.show,
		                                                             g)
	# noinspection PyDeepBugsBinOperand
	if (g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Season'] is int(0)) or \
			str(g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Season']).isdigit():
		g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Parsed Season'] = \
			str(get_padded_episode_number(g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Season'],
			                              2))
	else:
		g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Parsed Season'] = \
			str(get_alphabetical_specials_string())  # play with this
	# add more logic to prevent non-defined dictionary_for_shows to go through
	method_exit(g)
	return g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Parsed Season']


def get_season_folder(self,
                      g):
	method_launch(g)
	from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
	if g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Season'] is 0 or get_alphabetical_specials_string():
		self.season_folder = get_alphabetical_specials_string()
	elif g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Season']:  # add error handling for isdigit
		self.season_folder = \
			f"Season {get_season(self, g)}"
	else:
		method_exit(g)
		return
	method_exit(g)
	g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Parsed Season Folder'] = \
		self.season_folder
	return self.season_folder


def get_season_value_from_movies_dictionary(movie_dictionary_object,
                                            show,
                                            g):
	method_launch(g)
	try:
		if not movie_dictionary_object['Shows'][show]['Season']:
			movie_dictionary_object['Shows'][show]['Season'] = str()
	except KeyError as err:
		print(f"{g.method} had a KeyError{err}")  # testing
		movie_dictionary_object['Shows'][show]['Season'] = str()
	method_exit(g)
	return movie_dictionary_object['Shows'][show]['Season']


def get_padded_episode_number(e,
                              num):
	return str(e).zfill(num)
