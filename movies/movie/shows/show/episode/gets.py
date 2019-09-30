import os

import messaging.frontend as message
import jobs.cleanup.misc as cleanup
from movies.movie.shows.show.episode import (validate, parser)
# adjust all padding algorithms to pull from the API instead of calculating

def season_key(self, g, season_padding=2):
	message.method_launch(g)
	if self.show_dictionary['Season']:
		self.show_dictionary['Parsed Season'] = \
			parser.season_value_from_dictionary(self.movie_dictionary_object, self.show)
	if validate.parsed_season_value(self):
		self.show_dictionary['Parsed Season'] = str(get_padded_episode_number(self.show_dictionary['Season'], season_padding))
	else:
		self.show_dictionary['Parsed Season'] = f"Season {str(0).zfill(2)}"
	message.method_exit(g)
	return self.show_dictionary['Parsed Season']

def season_folder_key(self, g, season=int(os.environ['SEASON_INT']), padding=2):
	message.method_launch(g)
	season_folder = f"Season {str(season).zfill(padding)}"
	if self.show_dictionary['Season'] is season or season_folder:
		self.season_folder = season_folder
	elif self.show_dictionary['Season']:
		self.season_folder = f"Season {season_key(self, g)}"
	else:
		self.season_folder = str()
	message.method_exit(g)
	self.show_dictionary['Parsed Season Folder'] = self.season_folder
	cleanup.local_variables(list(season, season_folder))
	return self.season_folder


def get_padded_episode_number(e, num):
	return str(e).zfill(num)
