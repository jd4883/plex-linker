#!/usr/bin/env python3.7
import time
from os.path import abspath

import class_objects.sonarr_api
import class_objects.sonarr_class_methods
import messaging.backend as backend
from class_objects.misc_get_methods import (
	get_docker_media_path,
	get_host_media_path,
	get_movie_extensions,
	get_movies_dictionary_object,
	get_movies_path,
	get_shows_dictionary,
	get_shows_path,
	)
from class_objects.radarr_api import *
from class_objects.radarr_class_methods import parse_movie_title, parse_relpath
from class_objects.sonarr_api import *
from IO.YAML.yaml_to_object import (get_variable_from_yaml)
from logs.bin.get_parameters import (get_log_name, get_logger, get_method_main)
from movies.movie.movie_gets import (get_absolute_movie_file_path, get_movie_path, get_relative_movie_file_path)
from movies.movie.movie_validation import (validate_extensions_from_movie_file)
from movies.movie.shows.show.show_parser import parse_show_id
from movies.movies_gets import (get_relative_movies_path)

# TODO: create an automatic list of all active, ping Many J for list of active certificates
# TODO: try to get this done sooner than later
# TODO: play with marshmallow across the board for class objects, want to be able to go to and from a dictionary easily
from plex_linker.parser.parser import parse_relative_episode_file_path


class Globals:
	def __init__(self):
		self.sonarr = SonarrAPI()
		self.radarr = RadarrAPI()
		self.sonarr_root_folders = self.sonarr.get_root_folder()
		#self.radarr_root_folders = self.radarr.get_root_folder() # fairly sure this isnt a radarr endpoint
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
	def __init__(self, movie, movie_dict, g, media_path = str(os.environ['DOCKER_MEDIA_PATH'])):
		super().__init__()
		self.movie_dictionary = movie_dict
		g.LOG.debug(backend.debug_message(627, g, self.movie_dictionary))
		self.radarr_dictionary = g.radarr.lookup_movie(movie)
		
		g.LOG.debug(backend.debug_message(628, g, self.radarr_dictionary))
		self.tmbdid = str(self.parse_tmdbid(g))
		#print(g.radarr.get_movie_file(self.tmbdid))
		self.movie_title = \
			self.movie_dictionary['Title'] = str(parse_movie_title(self.radarr_dictionary, movie))
		g.LOG.debug(backend.debug_message(613, g, str(self.movie_title)))
		
		self.movie_file = \
			self.movie_dictionary['Movie File'] = \
			str()
		
		self.shows_dictionary = \
			get_shows_dictionary(self.movie_dictionary)
		
		self.absolute_movie_path =\
			self.movie_dictionary['Absolute Movie Path'] =\
			str(get_movie_path(self, g))
		
		g.LOG.debug(backend.debug_message(614, g, str(self.absolute_movie_path)))
		self.extension = self.movie_dictionary['Parsed Movie Extension'] = str()
		self.quality = self.movie_dictionary['Parsed Movie Quality'] = str()
		validate_extensions_from_movie_file(self, g)
		self.quality = str(self.parse_quality())
		g.LOG.debug(backend.debug_message(608, g, str(self.extension)))
		g.LOG.debug(backend.debug_message(612, g, str(self.quality)))
		g.LOG.debug(backend.debug_message(610, g, str(self.movie_file)))
		
		
		
		# from API
		self.relative_movie_path = \
			self.movie_dictionary['Relative Movie Path'] = \
			str(parse_relpath(self, g, media_path))
		g.LOG.debug(backend.debug_message(617, g, self.relative_movie_path))
		
		self.absolute_movie_file_path = self.movie_dictionary['Absolute Movie File Path'] = str(
				get_absolute_movie_file_path(self))
		g.LOG.debug(backend.debug_message(615, g, str(self.absolute_movie_file_path)))
		
		self.relative_movie_file_path = \
			self.movie_dictionary['Relative Movie File Path'] = str(get_relative_movie_file_path(self))
		g.LOG.debug(backend.debug_message(616, g, self.relative_movie_file_path))
	
	def parse_tmdbid(self, g):
		tmdbID = str()
		if 'tmdbId' in self.radarr_dictionary:
			if 'Movie DB ID' in self.movie_dictionary and self.movie_dictionary['Movie DB ID']:
				tmdbID = self.movie_dictionary['Movie DB ID']
			elif 'tmdbId' in self.radarr_dictionary[0] and int(self.radarr_dictionary[0]['tmdbId']) > 0:
				tmdbID = int(self.radarr_dictionary[0]['tmdbId'])
			g.radarr.rescan_movie(int(tmdbID)) if len(self.radarr_dictionary) > 0 else str()
				# rescan movie in case it was picked up since last scan
			g.radarr.refresh_movie(int(tmdbID)) if len(self.radarr_dictionary) > 0 else str()
				# to ensure metadata is up to date
			if len(self.radarr_dictionary) > 0 and self.radarr_dictionary[0]['monitored']:
				g.radarr.movie_search(int(tmdbID))
		return tmdbID
	
	def parse_quality(self):
		if self.quality:
			quality = str(self.quality)
		else:
			return str()
		if str(self.quality).lower() == "Remux-1080p.mkv".lower():
			try:
				quality.replace("Remux-1080p.mkv", "Bluray-1080p Remux.mkv")
			except IndexError:
				pass
		if quality.endswith(f"Proper.{self.extension}"):
			try:
				quality = f"{self.movie_file.split().pop(-2)} {self.quality}"
			except IndexError:
				pass
		elif not quality:
			quality = str()
		else:
			if self.movie_file:
				quality = str(self.movie_file.split().pop())
			else:
				quality = str()
		return str(quality)


class Show(Movie, Globals):
	def __init__(self,
	             g,
	             series = str(),
	             film = str(),
	             movie_dict = dict(),
	             show_dict = dict(),
	             series_lookup = dict()):
		super().__init__(film, movie_dict, g)
		
		# add better handling for titles with : and/or / in them from the API processing
		
		os.chdir(self.path_str(os.environ['DOCKER_MEDIA_PATH']))
		self.parsed_episode = list()
		self.movie_dictionary = movie_dict
		self.show = series
		self.show_dictionary = show_dict
		if 'Parsed Relative Show Title' in self.show_dictionary:
			del self.show_dictionary['Parsed Relative Show Title']
		g.LOG.debug(backend.debug_message(624, g, self.show_dictionary))
		self.sonarr_show_dictionary = series_lookup
		self.sonarr_api_query = self.parse_sonarr_api_query_results(g)
		self.link_status = str(self.show_dictionary['Symlinked'])
		g.LOG.debug(backend.debug_message(625, g, self.sonarr_show_dictionary))
		
		self.show_id = self.show_dictionary['Show ID'] \
			if 'Show ID' in self.show_dictionary \
			else str(parse_show_id(self.show, g))
		g.LOG.debug(backend.debug_message(618, g,self.show_id))
		self.episode_id = self.show_dictionary['Episode ID'] \
			if 'Episode ID' in self.show_dictionary else self.set_episode_id(g)
		g.LOG.debug(backend.debug_message(619, g, self.episode_id))
		print(self.episode_id)
		if not self.episode_id:
			print(f"EPISODE ID FAILED TO PROCESS FOR {self.show}")
			raise
		
		try:
			g.sonarr.rescan_series(int(self.show_id))  # rescan movie in case it was picked up since last scan
			g.sonarr.refresh_series(int(self.show_id))  # to ensure metadata is up to date
		except ValueError:
			g.LOG.error(backend.debug_message(620, g, self.show, self.episode_id))
		
		self.anime_status = \
			bool(self.lookup_anime_status())
		g.LOG.debug(backend.debug_message(621, g, self.anime_status))
		
		self.padding = \
			int(3) if self.anime_status else int(os.environ['EPISODE_PADDING'])
		g.LOG.debug(backend.debug_message(622, g, self.padding))
		
		self.episode_dict = \
			g.sonarr.get_episode_by_episode_id(self.episode_id)
		g.LOG.debug(backend.debug_message(623, g, self.episode_dict))
		self.episode_file_dict = \
			g.sonarr.get_episode_file_by_episode_id(self.episode_id)
		
		self.episode = \
			self.show_dictionary['Episode'] \
				if 'Episode' in self.show_dictionary \
				else str(self.episode_dict.pop('episodeNumber', str()))
		g.LOG.debug(backend.debug_message(622, g, self.episode))
		
		if not self.episode:
			print(f"NO EPISODE SET FOR {self.show}")
			raise
		
		self.absolute_episode = \
			self.show_dictionary['Absolute Episode'] = \
			str(self.episode_dict.pop('absoluteEpisodeNumber', str()))
		if self.absolute_episode:
			g.LOG.debug(backend.debug_message(628, g, self.absolute_episode))
		elif 'Absolute Episode' in self.show_dictionary:
			del self.show_dictionary['Absolute Episode']
		self.season = \
			self.show_dictionary['Season'] = \
			str(self.episode_dict.pop('seasonNumber', str())).zfill(2)
		g.LOG.debug(backend.debug_message(630, g, self.season))
		
		self.season_folder = self.show_dictionary['Parsed Season Folder'] = f"Season {self.season}"
		g.LOG.debug(backend.debug_message(631, g, self.season_folder))
		
		self.show_root_path =\
			self.show_dictionary['Show Root Path'] =\
			self.path_str(self.episode_dict.pop('path', self.path_str(self.parse_show_root_path(g))))
		# confirm this is always calculating correctly
		g.LOG.debug(backend.debug_message(632, g, self.show_root_path))
		self.relative_show_path = self.path_str(self.set_relative_show_path(g))
		if 'Relative Show Path' in self.show_dictionary and not self.relative_show_path:
			print(self.show_dictionary)
			raise
		
		self.parsed_episode = self.show_dictionary['Parsed Episode'] = str(self.episode).zfill(self.padding) if self.episode else str()
		g.LOG.debug(backend.debug_message(634, g, self.parsed_episode))
		
		self.parsed_absolute_episode = self.show_dictionary['Parsed Absolute Episode'] = \
			self.path_str(self.absolute_episode).zfill(self.padding) if self.absolute_episode else str()
		if 'Parsed Absolute Episode' in self.show_dictionary and not self.parsed_absolute_episode:
			del self.show_dictionary['Parsed Absolute Episode']
		g.LOG.info(backend.debug_message(635, g, self.parsed_absolute_episode))
		self.episode_title = self.show_dictionary['Title'] = self.path_str(self.episode_dict.pop('title', self.movie_title))
		g.LOG.debug(backend.debug_message(636, g, self.episode_title))
		
		self.parsed_show_title = \
			self.show_dictionary['Parsed Show Title'] = \
			self.path_str(f"{self.show_root_path}/{self.season_folder}/{self.show} - S{self.season}E{self.parsed_episode} "
			            f"- {self.episode_title}")
		g.LOG.debug(backend.debug_message(637, g, self.parsed_show_title))
	
	def set_episode_id(self, g):
		
		return self.show_dictionary['Episode ID'] \
			if 'Episode ID' in self.show_dictionary \
			else str(self.parse_episode_id(g.sonarr.get_episodes_by_series_id(int(self.show_id))))
	
	def path_str(self, string):
		return str((str(string).replace('//','/')
		         ).replace(":", "")
		        ).replace(str(os.environ['SONARR_ROOT_PATH_PREFIX']), str())
	
	def parse_sonarr_api_query_results(self, g):
		query = self.lookup_episode_index(self.sonarr_show_dictionary[0]) if self.sonarr_show_dictionary else dict()
		g.LOG.debug(backend.debug_message(626, g, query))
		return query
	
	def set_relative_show_path(self, g):
		path = self.show_dictionary['Relative Show File Path'] \
			if self.show_dictionary \
			else self.path_str(parse_relative_episode_file_path(self, self.episode_dict))
		print(path)
		if (not path) or (path == (None or str(None) or str())):
			return str()
		g.LOG.debug(backend.debug_message(633, g, path))
		return path
	
	def parse_show_root_path(self, g):
		default_root = f"tv/staging/{self.show}"        # adjust to be an environ
		#default_root = f"{os.environ['SONARR_DEFAULT_ROOT']}/{self.show}"
		
		for item in g.sonarr_root_folders:
			item = self.path_str(item['path'])
			potential = self.path_str(f"{item}{self.show}/{self.season_folder}")
			if os.path.exists(potential) and os.path.isdir(potential):
				return self.path_str(f"{item}{self.show}")
		return str(default_root)
	
	def lookup_anime_status(self):
		if 'Anime' in self.show_dictionary and self.show_dictionary['Anime']:
			return bool(self.show_dictionary['Anime'])
		elif ['seriesType'] in self.sonarr_api_query and self.sonarr_api_query['seriesType'] == 'anime':
				return True
		return False
	
	def lookup_episode_index(self, query = dict()):
		if self.sonarr_show_dictionary:
			for item in query:
				if ('episodeNumber' in query) \
						and (query[item]['episodeNumber'] == self.episode) \
						and (self.season == query[item]['seasonNumber']):
					query = query[item]
		return query
	
	def parse_episode_id(self, query):
		if not query:
			return str()
		try:
			for i in query:
				if int(i['seasonNumber']) == int(self.show_dictionary['Season']):
					if int(i['episodeNumber']) == int(self.show_dictionary['Episode'][0]):
						return i['id']
		except TypeError:
			pass
		except KeyError:
			pass
		except IndexError:
			pass
		return str()
