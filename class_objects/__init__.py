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
from movies.movie.shows.show.show_gets import get_anime_status_from_api
from movies.movies_gets import (get_absolute_movies_path,
                                get_relative_movies_path)
from movies.movies_puts import (set_nested_dictionary_key_value_pair,
                                set_working_directory_to_media_path)


class Globals:
	def __init__(self):
		self.sonarr = SonarrAPI()
		self.shows_dictionary = self.sonarr.get_series()
		#self.movies_dictionary = self.radarr # get full library
		self.MEDIA_PATH = str(environ['DOCKER_MEDIA_PATH'])
		self.MEDIA_DIRECTORY = str(environ["HOST_MEDIA_PATH"])
		self.LOG = get_logger(get_log_name())
		self.MOVIES_PATH = get_variable_from_yaml("Movie Directories")
		self.MOVIE_EXTENSIONS = get_variable_from_yaml("Movie Extensions")
		self.SHOWS_PATH = get_variable_from_yaml("Show Directories")
		self.movies_dictionary_object = get_yaml_dictionary()
		self.list_of_linked_movies = list()
		self.list_of_movies_to_locate = list()
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
				                                     get_absolute_movie_file_path(self,
				                                                                  g))
			g.movies_dictionary_object[title]['Relative Movie File Path'] = str()
			self.relative_movie_file_path = \
				set_nested_dictionary_key_value_pair(g.movies_dictionary_object[title]['Relative Movie File Path'],
				                                     get_relative_movie_file_path(self,
				                                                                  g))


# noinspection ProblematicWhitespace
class Show(Movie,
           Globals):
	def __init__(self,
	             show,
	             movie,
	             g):
		super().__init__(movie,
		                 g)
		set_working_directory_to_media_path(str(environ['DOCKER_MEDIA_PATH']))
		
		self.show = str(show)
		self.series_id = self.get_show_id(g,
		                                  movie)
		try:
			self.sonarr_api_query = g.sonarr.lookup_series(str(self.show))[0]
		except IndexError or FileNotFoundError:
			return
		try:
			g.movies_dictionary_object[movie]['Shows'][self.show]['Show Root Path'] = \
				str(self.sonarr_api_query['path']).replace(str(environ['SONARR_ROOT_PATH_PREFIX']),
				                                           '')
		except:
			g.movies_dictionary_object[movie]['Shows'][self.show]['Show Root Path'] = str()
		self.show_root_path = g.movies_dictionary_object[movie]['Shows'][self.show]['Show Root Path']
		print(f"SHOW TVDB ID: {self.sonarr_api_query['tvdbId']}")
		# print(f"SHOW SERIES TYPE: {self.sonarr_api_query['seriesType']}")  # if anime else
		
		#print(f"Show ID: {self.sonarr_api_query['id']}") # need to figure out the correct way to do this
		self.season = self.set_season_dictionary_value(g, movie)
		self.parsed_season = \
			g.movies_dictionary_object[movie]['Shows'][self.show]['Parsed Season'] = \
			str(get_season(self, g)).zfill(2)
		self.episode = \
			g.movies_dictionary_object[movie]['Shows'][self.show]['Parsed Episode'] = \
			str()
		self.absolute_episode = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[movie]['Shows'][self.show]['Absolute Episode'],
			                                     str())
		self.anime_status = \
			g.movies_dictionary_object[movie]['Shows'][self.show]['Anime'] = \
			get_anime_status_from_api(self.sonarr_api_query)
		self.parsed_title = \
			set_nested_dictionary_key_value_pair(g.movies_dictionary_object[movie]['Shows'][self.show]['Parsed Show Title'],
			                                     str())
		
		self.parsed_relative_title = \
			set_nested_dictionary_key_value_pair(
				g.movies_dictionary_object[movie]['Shows'][self.show]['Parsed Relative Show Title'],
				str())
		self.relative_show_path = \
			set_nested_dictionary_key_value_pair(
				g.movies_dictionary_object[self.movie_title]['Shows'][self.show]['Relative Show File Path'],
				str())
	
	def get_show_id(self,
	                g,
	                movie):
		for item in g.shows_dictionary:
			if item['title'] == self.show:
				g.movies_dictionary_object[movie]['Shows'][self.show]['Show ID'] = int(item['id'])
				return g.movies_dictionary_object[movie]['Shows'][self.show]['Show ID']
	
	def set_season_dictionary_value(self,
	                                g,
	                                movie):
		if self.sonarr_api_query['seasons'][0]['seasonNumber'] != 0:
			g.movies_dictionary_object[movie]['Shows'][self.show]['Season'] = 0
		else:
			g.movies_dictionary_object[movie]['Shows'][self.show]['Season'] = \
				self.sonarr_api_query['seasons'][0].pop('seasonNumber')
		return g.movies_dictionary_object[movie]['Shows'][self.show]['Season']
