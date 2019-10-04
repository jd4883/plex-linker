#!/usr/bin/env python3.7
import time
import movies.movie.shows.show.episode.parser as parse_episode
from os import chdir
from os.path import abspath

import movies.movie.shows.show.episode.parser
from IO.YAML.yaml_to_object import (get_yaml_dictionary, get_variable_from_yaml)
from class_objects.radarr_api import *
from class_objects.sonarr_api import *
from logs.bin.get_parameters import (get_method_main, get_logger, get_log_name)
from movies.movie.movie_gets import (get_absolute_movie_file_path, get_relative_movie_file_path, get_movie_path,
                                     get_relative_movie_path)
from movies.movie.movie_puts import (set_movie_quality)
from movies.movie.movie_validation import (validate_extensions_from_movie_file)
from movies.movie.shows.show.show_puts import set_season_dictionary_value, set_show_id
from movies.movie.shows.sets import set_show_root_path
from movies.movies_gets import (get_relative_movies_path)
from movies.movies_puts import (set_nested_dictionary_key_value_pair)

# TODO: play with marshmallow across the board for class objects, want to be able to go to and from a dictionary easily

class Globals:
	def __init__(self):
		self.sonarr = SonarrAPI()
		self.radarr = RadarrAPI()
		self.shows_dictionary = self.sonarr.get_series()
		self.movies_dictionary = self.radarr.get_movie_library()
		self.MEDIA_PATH = str(environ['DOCKER_MEDIA_PATH'])
		self.MEDIA_DIRECTORY = str(environ["HOST_MEDIA_PATH"])
		self.LOG = get_logger(get_log_name())
		self.MOVIES_PATH = get_variable_from_yaml("Movie Directories")
		self.MOVIE_EXTENSIONS = get_variable_from_yaml("Movie Extensions")
		self.SHOWS_PATH = get_variable_from_yaml("Show Directories")
		self.movies_dictionary_object = get_yaml_dictionary()
		self.list_of_linked_movies = []
		self.list_of_movies_to_locate = []
		self.method = self.parent_method = get_method_main()
		pass


class Movies:
	def __init__(self,
	             absolute_movies_path=abspath("/".join((str(environ['DOCKER_MEDIA_PATH']),
	                                                    get_variable_from_yaml("Movie Directories")[0])))):
		self.start_time = time.time()
		self.absolute_movies_path = absolute_movies_path
		self.relative_movies_path = get_relative_movies_path(self)


class Movie(Movies, Globals):
	def __init__(self, movie, movie_dictionary, g):
		super().__init__()
		self.movie_dictionary = movie_dictionary
		self.movie_dictionary['Unparsed Movie Title'] = self.movie_title = str(movie)
		self.radarr_dictionary = g.radarr.lookup_movie(self.movie_title)
		self.shows_dictionary = self.movie_dictionary['Shows']
		# self.absolute_movie_path =
		self.movie_dictionary['Absolute Movie Path'] = get_movie_path(self, g)
		self.relative_movie_path = \
			set_nested_dictionary_key_value_pair(self.movie_dictionary['Relative Movie Path'],
			                                     get_relative_movie_path(self, g))
		self.quality = set_nested_dictionary_key_value_pair(self.movie_dictionary['Parsed Movie Quality'], str())
		self.extension = set_nested_dictionary_key_value_pair(self.movie_dictionary['Parsed Movie Extension'])
		self.movie_file = set_nested_dictionary_key_value_pair(self.movie_dictionary['Parsed Movie File'], str())
		validate_extensions_from_movie_file(self, g)
		set_movie_quality(self, g)
		self.absolute_movie_file_path = \
			self.movie_dictionary['Absolute Movie File Path'] = \
			set_nested_dictionary_key_value_pair(self.movie_dictionary['Absolute Movie File Path'],
			                                     get_absolute_movie_file_path(self))
		self.movie_dictionary['Relative Movie File Path'] = str()
		self.relative_movie_file_path = set_nested_dictionary_key_value_pair(
			self.movie_dictionary['Relative Movie File Path'], get_relative_movie_file_path(self, g))


class Show(Movie, Globals):
	def __init__(self,
	             g,
	             series=str(),
	             film=str(),
	             movie_dict=dict(),
	             show_dict=dict(),
	             series_lookup=dict()):
		super().__init__(film, movie_dict, g)
		chdir(str(environ['DOCKER_MEDIA_PATH']))
		self.movie_dictionary = movie_dict
		self.show = series
		self.show_dictionary = show_dict
		self.show_dictionary['Symlinked'] = str()
		self.sonarr_show_dictionary = series_lookup
		self.sonarr_api_query = str()
		if self.sonarr_show_dictionary:
			self.sonarr_api_query = self.sonarr_show_dictionary[0]
		set_show_id(self.show, g)
		if self.show_dictionary['Show ID']:
			self.raw_episodes = g.sonarr.get_episodes_by_series_id(self.show_dictionary['Show ID'])
			self.raw_episode_files = g.sonarr.get_episode_files_by_series_id(self.show_dictionary['Show ID'])
		try:
			self.show_root_path = set_show_root_path(self.sonarr_api_query, self.show, g, film)
		except TypeError:
			self.show_root_path = str()
		try:
			self.season = set_season_dictionary_value(self)
		except TypeError:
			self.season = str('00')
		try:
			self.episode = self.show_dictionary['Parsed Episode'] = str()
		except TypeError:
			self.episode = str()
		try:
			self.absolute_episode = set_nested_dictionary_key_value_pair(self.show_dictionary['Absolute Episode'], str())
		except TypeError:
			self.absolute_episode = str()
		try:
			movies.movie.shows.show.episode.parser.season_from_api(self.show_dictionary, self.raw_episode_files)
		except TypeError:
			pass
		except AttributeError:
			pass
		self.parsed_title = set_nested_dictionary_key_value_pair(self.show_dictionary['Parsed Show Title'], str())
		self.parsed_relative_title = set_nested_dictionary_key_value_pair(
			self.show_dictionary['Parsed Relative Show Title'], str())
		self.relative_show_path = set_nested_dictionary_key_value_pair(self.show_dictionary['Relative Show File Path'],
		                                                               str())
		print('problem spot here')
		print(self.show_dictionary)

