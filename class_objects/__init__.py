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
	def __init__(self, movie, movie_dict, g, media_path = str(os.environ['DOCKER_MEDIA_PATH'])):
		super().__init__()
		self.movie_dictionary = movie_dict
		g.LOG.debug(backend.debug_message(627, g, self.movie_dictionary))
		self.radarr_dictionary = g.radarr.lookup_movie(movie)
		g.LOG.debug(backend.debug_message(628, g, self.radarr_dictionary))
		self.tmbdid = str()
		if 'tmdbId' in self.radarr_dictionary:
			self.tmbdid = self.movie_dictionary['Movie DB ID'] = int(self.radarr_dictionary[0]['tmdbId']) if len(self.radarr_dictionary) > 0 else str()
			g.radarr.rescan_movie(int(self.tmbdid)) if len(self.radarr_dictionary) > 0 else str()      # rescan movie in case it was picked up since last scan
			g.radarr.refresh_movie(int(self.tmbdid)) if len(self.radarr_dictionary) > 0 else str()     # to ensure metadata is up to date
			if len(self.radarr_dictionary) > 0 and self.radarr_dictionary[0]['monitored']:
				g.radarr.movie_search(int(self.tmbdid))
		
		
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
		
		g.LOG.info(backend.debug_message(614, g, str(self.absolute_movie_path)))
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
	
	def parse_quality(self):
		if self.quality:
			quality = str(self.quality)
		else:
			return str()
		if (str(self.quality).lower() == "Remux-1080p.mkv".lower()):
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
		os.chdir(str(os.environ['DOCKER_MEDIA_PATH']))
		prefix = str(os.environ['SONARR_ROOT_PATH_PREFIX'])
		self.parsed_episode = \
			list()
		
		self.movie_dictionary = \
			movie_dict
		
		self.show = \
			series
		
		self.show_dictionary = \
			show_dict
		g.LOG.info(backend.debug_message(624, g, self.show_dictionary))
		
		self.link_status = \
			self.show_dictionary['Symlinked'] = \
			str()
		
		self.sonarr_show_dictionary = \
			series_lookup
		g.LOG.info(backend.debug_message(625, g, self.sonarr_show_dictionary))
			
		self.sonarr_api_query = \
			self.lookup_episode_index(self.sonarr_show_dictionary[0]) if \
				self.sonarr_show_dictionary else dict()
		g.LOG.debug(backend.debug_message(626, g, self.sonarr_api_query))
		
		self.show_id = \
			self.show_dictionary['Show ID'] = \
			str(parse_show_id(self.show, g))
		g.LOG.info(backend.debug_message(618, g,self.show_id))
		
		self.episode_id = \
			self.show_dictionary['Episode ID'] = \
			str(self.parse_episode_id(g.sonarr.get_episodes_by_series_id(self.show_id)))
		g.LOG.info(backend.debug_message(619, g, self.episode_id))
		
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
			self.show_dictionary['Episode'] = \
			str(self.episode_dict.pop('episodeNumber', str()))
		g.LOG.info(backend.debug_message(622, g, self.episode))
		
		self.absolute_episode = \
			self.show_dictionary['Absolute Episode'] = \
			str(self.episode_dict.pop('absoluteEpisodeNumber', str()))
		g.LOG.info(backend.debug_message(628, g, self.absolute_episode))
		print(f"ABSOLUTE EPISODE: {self.absolute_episode}")
		
		self.parsed_relative_title = \
			str(self.show_dictionary['Parsed Relative Show Title'])
		print(f"PARSED RELATIVE TITLE: {self.parsed_relative_title}")
		g.LOG.info(backend.debug_message(629, g, self.parsed_relative_title))
		
		self.season = \
			self.show_dictionary['Season'] = \
			str(self.episode_dict.pop('seasonNumber', str())).zfill(2)
		g.LOG.info(backend.debug_message(630, g, self.season))
		print(f"SEASON: {self.season}")
		
		self.season_folder = \
			self.show_dictionary['Parsed Season Folder'] = \
			f"Season {self.season}"
		print(f"SEASON FOLDER: {self.season_folder}")
		g.LOG.info(backend.debug_message(631, g, self.season_folder))
		
		self.show_root_path =\
			self.show_dictionary['Show Root Path'] =\
			str(self.episode_dict.pop('path', self.get_show_root_path())).replace(prefix, str())
		
		#self.get_root_folder()[0]['path']
		# TODO: create logic to parse the path if pop fails this should fix most issues
		# should be able to grab all root folders from the api endpoint and test each for a valid path
		# need to add a conditional exit out if no path to find
		# f"{self.get_show_root_path()}/{self.show}" needs to be parsed out the old way
		g.LOG.info(backend.debug_message(632, g, self.show_root_path))
		
		self.relative_show_path = str(self.set_relative_show_path(g, prefix))
		
		self.parsed_episode = \
			self.show_dictionary['Parsed Episode'] = \
			str(self.episode).zfill(self.padding) if self.episode else str()
		print(f"PARSED EPISODE: {self.parsed_episode}")
		g.LOG.info(backend.debug_message(634, g, self.parsed_episode))
		
		self.parsed_absolute_episode = \
			self.show_dictionary['Parsed Absolute Episode'] = \
			str(self.absolute_episode).zfill(self.padding) if self.absolute_episode else str()
		print(f"PARSED ABSOLUTE EPISODE: {self.parsed_absolute_episode}")
		g.LOG.info(backend.debug_message(635, g, self.parsed_absolute_episode))
		
		self.episode_title = \
			self.show_dictionary['Title'] = \
			str(self.episode_dict.pop('title', self.movie_title)).replace(":", "")
		g.LOG.debug(backend.debug_message(636, g, self.episode_title))
		
		self.parsed_title = \
			self.show_dictionary['Parsed Show Title'] = \
			f"{self.show_root_path}/{self.season_folder}/{self.show} - S{self.season}E{self.parsed_episode} - " \
			f"{self.episode_title}"
		g.LOG.info(backend.debug_message(637, g, self.parsed_title))
	
	def set_relative_show_path(self, g, prefix):
		path = self.show_dictionary['Relative Show File Path'] = str(self.parse_relative_episode_file_path(prefix))
		if path == None:
			path = str()
		g.LOG.info(backend.debug_message(633, g, path))
		return path
	
	def parse_relative_episode_file_path(self, prefix):
		if ('hasFile' in self.episode_dict) and (bool(self.episode_dict['hasFile'])):
			return str(self.episode_dict['episodeFile']['path']).replace(prefix, str())
	
	def get_show_root_path(self):
		for item in g.sonarr.get_root_folder():
			item = item['path'].replace(prefix, str())
			if exists(f"{item}/{self.show}/{self.season_folder}"):
				return item
		return str()
	
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
