from os import environ

import messaging.frontend as message
import jobs.path_handling as paths
from movies.movie.shows.show import init
from movies.movie.shows.show.episode.gets import (get_padded_episode_number, season_folder_key)
from movies.movies_puts import (set_nested_dictionary_key_value_pair)


def parse_show(self, g):
	message.method_launch(g)
	init.anime_status(self)
	if not self.show_dictionary['Season']:
		self.show_dictionary['Season'] = str(0)
	self.show_dictionary['Parsed Season Folder'] = season_folder_key(self, g)
	self.episode = set_nested_dictionary_key_value_pair(self.show_dictionary['Episode'], str())
	self.absolute_episode = set_nested_dictionary_key_value_pair(self.show_dictionary['Absolute Episode'], str())
	message.method_launch(g)
	if self.show_dictionary['Anime']:
		self.episode = "-".join([get_padded_episode_number(e, 3) for e in self.episode])
		self.absolute_episode = "-".join([get_padded_episode_number(e, 3) for e in self.absolute_episode])
	else:
		self.episode = "-".join([get_padded_episode_number(e, 2) for e in self.episode])
		self.absolute_episode = "-".join([get_padded_episode_number(e, 2) for e in self.absolute_episode])
	message.method_exit(g)
	self.parsed_relative_title = set_nested_dictionary_key_value_pair(self.show_dictionary['Parsed Relative Show Title'],
	                                                                  parse_show_title_from_show_dictionary(self, g))
	message.method_exit(g)
	return self.parsed_relative_title


def parse_show_title_from_show_dictionary(show, g):
	message.method_launch(g)
	paths.create_directory("/".join((show.path, show.show_dictionary['Parsed Season Folder'])))
	if show.absolute_episode:
		show.parsed_title = set_nested_dictionary_key_value_pair(show.show_dictionary['Parsed Show Title'],
		                                                         f"{show.path}/{show.show_dictionary['Parsed Season Folder']}/{show.show} - S{show.show_dictionary['Season']}E{show.episode} (E{show.absolute_episode}) - {show.title}")
	else:
		show.parsed_title = set_nested_dictionary_key_value_pair(show.show_dictionary['Parsed Show Title'],
		                                                         f"{show.path}/{show.show_dictionary['Parsed Season Folder']}/{show.show} - S{show.show_dictionary['Season']}E{show.episode} - {show.title}")
	message.method_exit(g)
	return show.parsed_title


def get_parsed_show_title(show):
	return " ".join((show.parsed_title, show.quality))


def parse_root_path_string(api_query):
	return str(api_query['path']).replace(str(environ['SONARR_ROOT_PATH_PREFIX']), '')
