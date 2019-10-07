#!/usr/bin/env python3.7
import time
from os import chdir
from os.path import abspath
import class_objects.sonarr_api
import class_objects.sonarr_class_methods
from class_objects.misc_get_methods import (
	get_movies_dictionary_object,
	get_shows_path,
	get_movie_extensions,
	get_movies_path,
	get_host_media_path,
	get_docker_media_path,
	get_shows_dictionary,
	)
from class_objects.radarr_api import *
from class_objects.sonarr_api import *
from class_objects.radarr_class_methods import parse_movie_title, parse_relpath
from class_objects.sonarr_class_methods import (get_parsed_relative_show_title)
from IO.YAML.yaml_to_object import (get_variable_from_yaml)
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
		self.MEDIA_PATH = str(get_docker_media_path())
		self.MEDIA_DIRECTORY = str(get_host_media_path())
		self.LOG = get_logger(get_log_name())
		self.MOVIES_PATH = get_movies_path()
		self.MOVIE_EXTENSIONS = get_movie_extensions()
		self.SHOWS_PATH = get_shows_path()
		self.movies_dictionary_object = get_movies_dictionary_object()
		self.method = self.parent_method = get_method_main()
		pass


class Movies:
	def __init__(self, absolute_movies_path = abspath("/".join((str(environ['DOCKER_MEDIA_PATH']),
	                                                            get_variable_from_yaml("Movie Directories")[0])))):
		self.start_time = time.time()
		self.absolute_movies_path = absolute_movies_path
		self.relative_movies_path = get_relative_movies_path(self)


class Movie(Movies, Globals):
	def __init__(self, movie, movie_dictionary, g, media_path = str(os.environ['DOCKER_MEDIA_PATH'])):
		super().__init__()
		self.movie_dictionary = movie_dictionary
		self.radarr_dictionary = g.radarr.lookup_movie(movie)
		self.movie_title = \
			self.movie_dictionary['Title'] = str(parse_movie_title(self.radarr_dictionary, movie))
		self.movie_file = str()
		self.shows_dictionary = get_shows_dictionary(self.movie_dictionary)
		self.absolute_movie_path = \
			self.movie_dictionary['Absolute Movie Path'] = str(get_movie_path(self, g))
		# from API
		self.relative_movie_path = self.movie_dictionary['Relative Movie Path'] = str(parse_relpath(self, g, media_path))
		self.extension = str(self.movie_dictionary['Parsed Movie Extension'])
		self.quality = str(self.movie_dictionary['Parsed Movie Quality'])
		self.quality = str(self.parse_quality())
		
		
		validate_extensions_from_movie_file(self, g)
		self.absolute_movie_file_path = \
			self.movie_dictionary['Absolute Movie File Path'] = str(get_absolute_movie_file_path(self))
		self.relative_movie_file_path = \
			self.movie_dictionary['Relative Movie File Path'] = str(get_relative_movie_file_path(self))
	
	def parse_quality(self):
		if self.quality:
			quality = self.quality
		else:
			return
		if str(self.quality).lower() == "Remux-1080p.mkv".lower():
			quality.replace("Remux-1080p.mkv", "Bluray-1080p Remux.mkv")
		if quality.endswith(f"Proper.{self.extension}"):
			quality = f"{self.movie_file.split().pop(-2)} {self.quality}"
		else:
			quality = movie_file.split().pop()
		return quality


class Show(Movie, Globals):
	def __init__(self,
	             g,
	             series = str(),
	             film = str(),
	             movie_dict = dict(),
	             show_dict = dict(),
	             series_lookup = dict()):
		super().__init__(film, movie_dict, g)
		os.chdir(str(os.environ['DOCKER_MEDIA_PATH']))
		prefix = str(environ['SONARR_ROOT_PATH_PREFIX'])
		self.parsed_episode = list()
		self.parsed_episode = list()
		self.movie_dictionary = movie_dict
		self.show = series
		self.show_dictionary = show_dict
		self.link_status = \
			str(self.show_dictionary['Symlinked'])
		
		self.sonarr_show_dictionary = series_lookup
		
		self.sonarr_api_query = \
			self.lookup_episode_index(self.sonarr_show_dictionary[0]) if \
			self.sonarr_show_dictionary else dict()
		
		self.show_id = \
			self.show_dictionary['Show ID'] = \
			parse_show_id(self.show, g)

		self.episode_id = \
			self.show_dictionary['Episode ID'] = \
			self.parse_episode_id(g.sonarr.get_episodes_by_series_id(self.show_id))

		self.anime_status = \
			self.lookup_anime_status()
		
		self.padding = \
			int(3) if self.anime_status else int(os.environ['EPISODE_PADDING'])

		self.episode_dict = \
			g.sonarr.get_episode_by_episode_id(self.episode_id)
		
		self.episode_file_dict = \
			g.sonarr.get_episode_file_by_episode_id(self.episode_id)
		
		self.episode = \
			self.show_dictionary['Episode'] = \
			self.episode_dict.pop('episodeNumber', int())

		self.absolute_episode = \
			self.show_dictionary['Absolute Episode'] = \
			self.episode_dict.pop('absoluteEpisodeNumber', int())
		
		self.parsed_relative_title = \
			str(get_parsed_relative_show_title(self.show_dictionary))
		
		self.season = \
			self.show_dictionary['Season'] = \
			str(self.episode_dict.pop('seasonNumber', str())).zfill(2)
			
		self.season_folder = \
			self.show_dictionary['Parsed Season Folder'] = \
			f"Season {self.season}"
		
		self.show_root_path = \
			self.show_dictionary['Show Root Path'] = \
			str(self.episode_dict.pop('path', f"{self.get_path()}/{self.show}")).replace(prefix, str())
		
		try:
			self.relative_show_path = \
				self.show_dictionary['Relative Show File Path'] = \
				str(self.episode_dict['episodeFile']['path']).replace(prefix, str())
		except KeyError:
			self.relative_show_path = \
				str(self.show_dictionary['Relative Show File Path'])
		
		self.parsed_episode = \
			self.show_dictionary['Parsed Episode'] = \
			str(self.episode).zfill(self.padding)
		
		self.parsed_absolute_episode = \
			self.show_dictionary['Parsed Absolute Episode'] = \
			str(self.absolute_episode).zfill(self.padding)
			
		self.episode_title = \
			self.show_dictionary['Title'] = \
			str(self.episode_dict.pop('title', self.movie_title))
		
		self.parsed_title = \
			self.show_dictionary['Parsed Show Title'] = \
			f"{self.show_root_path}/{self.season_folder}/{self.show} - S{self.season}E{self.parsed_episode} - {self.episode_title}"
		
		
			
	def get_path(self):
		if self.anime_status:
			return 'anime'
		return 'tv'
	# make this segment dynamic
	
	def lookup_anime_status(self):
		try:
			if self.sonarr_api_query['seriesType'] == 'anime':
				return True
		except KeyError:
			pass
		except ValueError:
			pass
		except IndexError:
			pass
		return False
	
	def lookup_episode_index(self, query=dict()):
		if self.sonarr_show_dictionary:
			for item in query:
				if ('episodeNumber' in query) and (query[item]['episodeNumber'] == self.episode) and (self.season ==
				                                                                                      query[item]['seasonNumber']):
					query = query[item]
		return query
	
	def parse_episode_id(self, query):
		try:
			for i in query:
				if int(i['seasonNumber']) == int(self.show_dictionary['Season']):
					if int(i['episodeNumber']) == int(self.show_dictionary['Episode'][0]):
					   return i['id']
		except TypeError:
			pass
		except KeyError:
			pass
		return int()
