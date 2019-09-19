#!/usr/bin/env python3.7
import time
from os import chdir
from os.path import abspath

from IO.YAML.yaml_to_object import (get_yaml_dictionary,
                                    get_variable_from_yaml)
from class_objects.radarr_api import *
from class_objects.sonarr_api import *
from logs.bin.get_parameters import (get_method_main,
                                     get_logger,
                                     get_log_name)
from movies.movie.movie_gets import (get_absolute_movie_file_path,
                                     get_relative_movie_file_path,
                                     get_movie_path,
                                     get_relative_movie_path)
from movies.movie.movie_puts import (set_movie_quality)
from movies.movie.movie_validation import (validate_extensions_from_movie_file,
                                           validated_movie_path_is_not_null)
from movies.movie.shows.show.episode.episode_parser import parse_season_using_sonarr_api
from movies.movie.shows.show.show_gets import (get_anime_status_from_api)
from movies.movie.shows.show.show_puts import set_season_dictionary_value, set_show_id
from movies.movie.shows.shows_parse import set_show_root_path
from movies.movies_gets import (get_relative_movies_path)
from movies.movies_puts import (set_nested_dictionary_key_value_pair)


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
		self.method = \
			self.parent_method = \
			get_method_main()
		pass


class Movies:
	def __init__(self,
	             absolute_movies_path=abspath("/".join((str(environ['DOCKER_MEDIA_PATH']),
	                                                    get_variable_from_yaml("Movie Directories")[0])))):
		self.start_time = time.time()
		self.absolute_movies_path = absolute_movies_path
		self.relative_movies_path = get_relative_movies_path(self)


class Movie(Movies,
            Globals):
	def __init__(self,
	             movie,
	             movie_dictionary,
	             g):
		super().__init__()
		self.movie_dictionary = movie_dictionary
		self.movie_dictionary['Unparsed Movie Title'] = self.movie_title = str(movie)
		self.radarr_dictionary = g.radarr.lookup_movie(self.movie_title)
		self.shows_dictionary = self.movie_dictionary['Shows']
		# self.absolute_movie_path =
		self.movie_dictionary['Absolute Movie Path'] = \
			get_movie_path(self,
			               g)
		self.relative_movie_path = \
			set_nested_dictionary_key_value_pair(self.movie_dictionary['Relative Movie Path'],
			                                     get_relative_movie_path(self,
			                                                             g))
		self.quality = set_nested_dictionary_key_value_pair(self.movie_dictionary['Parsed Movie Quality'],
			                                     str())
		self.extension = set_nested_dictionary_key_value_pair(self.movie_dictionary['Parsed Movie Extension'])
		self.movie_file = \
			set_nested_dictionary_key_value_pair(self.movie_dictionary['Parsed Movie File'],
			                                     str())
		if validated_movie_path_is_not_null(self,
		                                    g):
			validate_extensions_from_movie_file(self,
			                                    g)
			set_movie_quality(self,
			                  g)
			self.absolute_movie_file_path = \
				set_nested_dictionary_key_value_pair(self.movie_dictionary['Absolute Movie File Path'],
				                                     get_absolute_movie_file_path(self))
			self.movie_dictionary['Relative Movie File Path'] = str()
			self.relative_movie_file_path = \
				set_nested_dictionary_key_value_pair(self.movie_dictionary['Relative Movie File Path'],
				                                     get_relative_movie_file_path(self,
				                                                                  g))


class Show(Movie,
           Globals):
	# noinspection PyDeepBugsBinOperand
	def __init__(self,
	             show,
	             movie,
	             movie_dictionary,
	             g):
		super().__init__(movie,
		                 movie_dictionary,
		                 g)
		chdir(str(environ['DOCKER_MEDIA_PATH']))
		self.movie_dictionary = movie_dictionary
		self.show = str(show)
		self.show_dictionary = self.movie_dictionary['Shows'][self.show]
		self.sonarr_show_dictionary = g.sonarr.lookup_series(self.show)
		print(f"show dictionary created: {self.show_dictionary}")
		set_show_id(self.show, g)
		try:
			self.sonarr_api_query = g.sonarr.lookup_series(str(self.show))[0]
		except (IndexError or FileNotFoundError or KeyError):
			self.sonarr_api_query = str()
			return
		g.sonarr.get_episodes_by_series_id(self.show_dictionary)
		try:
			self.raw_episodes = g.sonarr.get_episodes_by_series_id(self.show_dictionary['Show ID'])
		except TypeError:
			return
		try:
			self.raw_episode_files = \
				g.sonarr.get_episode_files_by_series_id(self.show_dictionary['Show ID'])
		except TypeError:
			return
		
		try:
			self.show_root_path = set_show_root_path(self.sonarr_api_query,
			                                         self.show,
			                                         g,
			                                         movie)
		except TypeError:
			self.show_root_path = str()
		try:
			self.season = set_season_dictionary_value(self.show_dictionary,
			                                          self.sonarr_api_query)
		except TypeError:
			self.season = int(0)
		self.episode = \
			self.show_dictionary['Parsed Episode'] = str()
		self.absolute_episode = \
			set_nested_dictionary_key_value_pair(self.show_dictionary['Absolute Episode'],
			                                     str())
		try:
			parse_season_using_sonarr_api(self.show_dictionary,
			                              self.raw_episode_files)
		except TypeError as err:
			pass
		# parse_episode_using_sonarr_api(self.show_dictionary, self.raw_episode_files)
		# print('this is the new parse season and episode segment')
		
		self.parsed_title = \
			set_nested_dictionary_key_value_pair(
				self.show_dictionary['Parsed Show Title'],
				str())
		
		self.parsed_relative_title = \
			set_nested_dictionary_key_value_pair(
				self.show_dictionary['Parsed Relative Show Title'],
				str())
		self.relative_show_path = \
			set_nested_dictionary_key_value_pair(
				self.show_dictionary['Relative Show File Path'],
				str())


def parse_episode_using_sonarr_api(show,
                                   query):
	padding = 2
	if not show['Episode']:
		show['episode'] = str()
		show['Parsed Episode'] = str()
	for item in query:
		try:
			if query[item]['episodeNumber'] == show['Episode']:
				show['Episode'] = query[item]['episodeNumber']
				show['Episode ID'] = int(query[item]['id'])
				if get_anime_status_from_api(query[item]):
					show['Anime'] = True
					padding = 3
				if query['absoluteEpisodeNumber']:
					show['Absolute Episode'] = int(query['absoluteEpisodeNumber'])
					show['Parsed Absolute Episode'] = str(show['Absolute Episode']).zfill(padding)
		except KeyError:
			continue
		show['Parsed Episode'] = str(show['Episode']).zfill(padding)
		print(f"Parsed Episode ID {show['Episode ID']} for Show")
		print(f"Episode parsed as {show['Episode']}")
		print(f"Parsed Episode {show['Parsed Episode']} for Show")
		break
	


# tv_show_class_object.raw_episode_files
