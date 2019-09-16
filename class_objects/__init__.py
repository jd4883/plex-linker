#!/usr/bin/env python3.7
import time

from IO.YAML.yaml_to_object import (get_yaml_dictionary,
                                    get_variable_from_yaml)
from class_objects.sonarr_api import *
from logs.bin.get_parameters import (get_method_main,
                                     get_logger,
                                     get_log_name)
from movies.movie.movie_gets import (get_absolute_movie_file_path,
                                     get_relative_movie_file_path,
                                     get_movie_path,
                                     get_relative_movie_path,
                                     get_unparsed_movie_title)
from movies.movie.movie_puts import (set_movie_quality)
from movies.movie.movie_validation import (validate_extensions_from_movie_file,
                                           validated_movie_path_is_not_null)
from movies.movie.shows.show.episode.episode_gets import (get_season)
from movies.movie.shows.show.show_gets import (get_anime_status_from_api,
                                               get_show_id)
from movies.movie.shows.show.show_puts import set_season_dictionary_value
from movies.movie.shows.shows_parse import set_show_root_path
from movies.movies_gets import (get_absolute_movies_path,
                                get_relative_movies_path)
from movies.movies_puts import (set_nested_dictionary_key_value_pair,
                                set_working_directory_to_media_path)


class Globals:
	def __init__(self):
		self.sonarr = SonarrAPI()
		self.sonarr_genres = []
		self.shows_dictionary = self.sonarr.get_series()
		# self.movies_dictionary = self.radarr # get full library
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
	             g):
		self.start_time = time.time()
		self.absolute_movies_path = get_absolute_movies_path(g)
		self.relative_movies_path = get_relative_movies_path(self)
		self.list_of_possible_paths = []


class Movie(Movies,
            Globals):
	def __init__(self,
	             title,
	             g):
		super().__init__(g)
		self.movie_title = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Unparsed Movie Title'],
			                                     get_unparsed_movie_title(title,
			                                                              g))
		self.shows_dictionary_object = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Shows'],
			                                     [{}])
		self.movie_dictionary_object = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title],
			                                     [{}])
		self.absolute_movie_path = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Absolute Movie Path'],
			                                     get_movie_path(self,
			                                                    g))
		self.relative_movie_path = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Relative Movie Path'],
			                                     get_relative_movie_path(self,
			                                                             g))
		self.quality = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Parsed Movie Quality'],
			                                     str())
		self.extension = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Parsed Movie Extension'],
			                                     str())
		self.movie_file = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Parsed Movie File'],
			                                     str())
		if validated_movie_path_is_not_null(self,
		                                    g):
			validate_extensions_from_movie_file(self,
			                                    g)
			set_movie_quality(self,
			                  g)
			self.absolute_movie_file_path = \
				set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Absolute Movie File Path'],
				                                     get_absolute_movie_file_path(self))
			g.movies_dictionary_object[title]['Relative Movie File Path'] = str()
			self.relative_movie_file_path = \
				set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Relative Movie File Path'],
				                                     get_relative_movie_file_path(self,
				                                                                  g))


class Show(Movie,
           Globals):
	# noinspection PyDeepBugsBinOperand
	def __init__(self,
	             show,
	             movie,
	             g):
		super().__init__(movie,
		                 g)
		set_working_directory_to_media_path(str(environ['DOCKER_MEDIA_PATH']))
		
		self.show = str(show)
		g.movies_dictionary_object[movie]['Shows'][show]['Show ID'] = \
			get_show_id(self.show,
			            g)
		try:
			self.sonarr_api_query = g.sonarr.lookup_series(str(self.show))[0]
		except (IndexError or FileNotFoundError) as err:
			print(f"{g.method} had a IndexError or FileNotFoundError: {err}")  # testing
			self.sonarr_api_query = str()
			return
		g.movies_dictionary_object[movie]['Shows'][self.show]['Anime'] = get_anime_status_from_api(self.sonarr_api_query)
		self.show_root_path = set_show_root_path(self.sonarr_api_query,
		                                         self.show,
		                                         g,
		                                         movie)
		self.season = set_season_dictionary_value(self.sonarr_api_query,
		                                          self.show,
		                                          g,
		                                          movie)
		self.parsed_season = \
			g.movies_dictionary_object[movie]['Shows'][self.show]['Parsed Season'] = str(get_season(self, g)).zfill(2)
		self.episode = \
			g.movies_dictionary_object[movie]['Shows'][self.show]['Parsed Episode'] = str()
		self.absolute_episode = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[movie]['Shows'][self.show]['Absolute Episode'],
			                                     str())
		
		self.parsed_title = \
			set_nested_dictionary_key_value_pair(
				g.movies_dictionary_object[movie]['Shows'][self.show]['Parsed Show Title'],
				str())
		
		self.parsed_relative_title = \
			set_nested_dictionary_key_value_pair(
				g.movies_dictionary_object[movie]['Shows'][self.show]['Parsed Relative Show Title'],
				str())
		self.relative_show_path = \
			set_nested_dictionary_key_value_pair(
				g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Relative Show File Path'],
				str())
