#!/usr/bin/env python3
import messaging.frontend as message
import os

# adjust all padding algorithms to pull from the API instead of calculating
def get_season(self, g, default_season_number = int(os.environ['SEASON_INT']), season_padding = 2):
	message.method_launch(g)
	if self.show_dictionary['Season']:
		self.show_dictionary['Parsed Season'] =\
			get_season_value_from_movies_dictionary(self.movie_dictionary_object, self.show)
	if (self.show_dictionary['Season'] == int(default_season_number)) or str(self.show_dictionary['Season']).isdigit():
		self.show_dictionary['Parsed Season'] = str(get_padded_episode_number(self.show_dictionary['Season'], season_padding))
	else:
		self.show_dictionary['Parsed Season'] = f"Season {str(0).zfill(2)}"
	message.method_exit(g)
	return self.show_dictionary['Parsed Season']


def get_season_folder(self, g):
	message.method_launch(g)
	season = f"Season {str(0).zfill(2)}"
	if self.show_dictionary['Season'] is 0 or season:
		self.season_folder = season
	elif self.show_dictionary['Season']:
		self.season_folder = f"Season {get_season(self, g)}"
	else:
		self.season_folder = str()
	message.method_exit(g)
	self.show_dictionary['Parsed Season Folder'] = self.season_folder
	return self.season_folder


def get_season_value_from_movies_dictionary(movie, show):
	if not movie['Shows'][show]['Season']:
		movie['Shows'][show]['Season'] = str()
	return movie['Shows'][show]['Season']


def get_padded_episode_number(e, num):
	return str(e).zfill(num)
