#!/usr/bin/env python3.7
import os
import time
from os import chdir
from os.path import abspath

import movies.movie.shows.show.episode.sets as set_episode
from class_objects.radarr_api import *
from class_objects.sonarr_api import *
from IO.YAML.yaml_to_object import (get_variable_from_yaml, get_yaml_dictionary)
from logs.bin.get_parameters import (get_log_name, get_logger, get_method_main)
from movies.movie.movie_gets import (get_absolute_movie_file_path, get_movie_path, get_relative_movie_file_path)
from movies.movie.movie_validation import (validate_extensions_from_movie_file)
from movies.movie.shows.show.show_parser import parse_show_id
from movies.movies_gets import (get_relative_movies_path)


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
	             absolute_movies_path = abspath("/".join((str(environ['DOCKER_MEDIA_PATH']),
	                                                      get_variable_from_yaml("Movie Directories")[0])))):
		self.start_time = time.time()
		self.absolute_movies_path = absolute_movies_path
		self.relative_movies_path = get_relative_movies_path(self)


class Movie(Movies, Globals):
	def __init__(self, movie, movie_dictionary, g, media_path = str(os.environ['DOCKER_MEDIA_PATH'])):
		super().__init__()
		self.movie_dictionary = movie_dictionary
		self.movie_dictionary['Unparsed Movie Title'] = self.movie_title = str(movie)
		self.radarr_dictionary = g.radarr.lookup_movie(self.movie_title)
		self.movie_title = str(self.parse_movie_title(movie))
		self.shows_dictionary = self.movie_dictionary['Shows']
		self.absolute_movie_path = \
			self.movie_dictionary['Absolute Movie Path'] = str(get_movie_path(self, g))
		# from API
		# seem to be having buggy behavior with aphrodite API, all my API calls give inaccurate info about files on disk
		# print(self.radarr_dictionary)
		self.relative_movie_path = self.movie_dictionary['Relative Movie Path'] = str(self.parse_relpath(g, media_path))
		self.quality = str(self.movie_dictionary['Parsed Movie Quality'])
		self.extension = str(self.movie_dictionary['Parsed Movie Extension'])
		self.movie_file = str(self.movie_dictionary['Parsed Movie File'])
		validate_extensions_from_movie_file(self, g)
		self.absolute_movie_file_path = \
			self.movie_dictionary['Absolute Movie File Path'] = str(get_absolute_movie_file_path(self))
		self.relative_movie_file_path = \
			self.movie_dictionary['Relative Movie File Path'] = str(get_relative_movie_file_path(self))
	
	def parse_movie_title(self, movie):
		movie_title = movie.replace(":", "-")
		try:
			base = str(self.radarr_dictionary[0].pop('title', str(movie)))
			year = str(self.radarr_dictionary[0].pop('year', str())).replace(":", "-")
			movie_title = f"{base} ({year})".replace(" ()", str()).replace(":", "-")
		except IndexError:
			pass
		except KeyError:
			pass
		return movie_title
	
	
	def parse_relpath(self, g, media_path):
		film = get_movie_path(self, g)
		if os.path.exists(film):
			return os.path.relpath(film, media_path)


class Show(Movie, Globals):
	def __init__(self,
	             g,
	             series = str(),
	             film = str(),
	             movie_dict = dict(),
	             show_dict = dict(),
	             series_lookup = dict()):
		super().__init__(film, movie_dict, g)
		chdir(g.MEDIA_PATH)
		self.movie_dictionary = movie_dict
		self.padding = int(os.environ['EPISODE_PADDING'])
		self.show = series
		self.show_dictionary = show_dict
		self.link_status = str(self.show_dictionary['Symlinked'])
		self.sonarr_show_dictionary = series_lookup
		self.sonarr_api_query = dict()
		if self.sonarr_show_dictionary:
			self.sonarr_api_query = self.sonarr_show_dictionary[0]
		self.show_root_path = self.show_dictionary['Show Root Path'] = self.set_root_path()
		self.parsed_title = str(self.show_dictionary['Parsed Show Title'])
		self.relative_show_path = str(self.show_dictionary['Relative Show File Path'])
		self.parsed_relative_title = self.show_dictionary['Parsed Relative Show Title'], str()
		# assign at class object level and return
		self.show_id = self.show_dictionary['Show ID'] = parse_show_id(self.show, g)
		self.raw_episodes = list(g.sonarr.get_episodes_by_series_id(self.show_dictionary['Show ID']))
		self.raw_episode_files = g.sonarr.get_episode_files_by_series_id(self.show_dictionary['Show ID'])
		self.season = self.show_dictionary['Season'] = str(set_episode.season_dictionary(self)).zfill(2)
		self.episode = str(self.show_dictionary['Parsed Episode'])
		self.absolute_episode = str(self.show_dictionary['Absolute Episode'])
	
	def set_root_path(self):
		prefix = str(environ['SONARR_ROOT_PATH_PREFIX'])
		return str(self.sonarr_api_query.pop('path', '')).replace(prefix, str())
