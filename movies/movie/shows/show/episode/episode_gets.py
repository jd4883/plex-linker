#!/usr/bin/env python3
import messaging.frontend as message


def get_season(self, g):
	message.method_launch(g)
	from movies.movie.shows.show.show_gets import (get_alphabetical_specials_string)
	if self.show_dictionary['Season']:
		self.show_dictionary['Parsed Season'] =\
			get_season_value_from_movies_dictionary(self.movie_dictionary_object, self.show, g)
	if (self.show_dictionary['Season'] == int(0)) or str(self.show_dictionary['Season']).isdigit():
		self.show_dictionary['Parsed Season'] = str(get_padded_episode_number(self.show_dictionary['Season'], 2))
	else:
		self.show_dictionary['Parsed Season'] = str(get_alphabetical_specials_string())  # try to get to the class object
	# level
	message.method_exit(g)
	return self.show_dictionary['Parsed Season']


def get_season_folder(self, g):
	message.method_launch(g)
	from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
	if self.show_dictionary['Season'] is 0 or get_alphabetical_specials_string():
		self.season_folder = get_alphabetical_specials_string()
	elif self.show_dictionary['Season']:
		self.season_folder = f"Season {get_season(self, g)}"
	else:
		self.season_folder = str()
	message.method_exit(g)
	self.show_dictionary['Parsed Season Folder'] = self.season_folder
	return self.season_folder


def get_season_value_from_movies_dictionary(movie, show, g):
	message.method_launch(g)
	try:
		if not movie['Shows'][show]['Season']:
			movie['Shows'][show]['Season'] = str()
	except KeyError as err:
		print(f"{g.method} had a KeyError{err}. If not seen this should go away")  # testing
		exit(-1)
		movie['Shows'][show]['Season'] = str()
	message.method_exit(g)
	return movie['Shows'][show]['Season']


def get_padded_episode_number(e, num):
	return str(e).zfill(num)
