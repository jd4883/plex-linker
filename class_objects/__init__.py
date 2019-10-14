#!/usr/bin/env python3.7
import time
import plex_linker.parser.series as parse_series
import plex_linker.fetch.series as fetch_series
import class_objects.sonarr_api
import class_objects.sonarr_class_methods
import messaging.backend as backend

from os.path import abspath
from marshmallow import Schema, fields
from class_objects.misc_get_methods import (
	get_docker_media_path,
	get_host_media_path,
	get_movie_extensions,
	get_movies_dictionary_object,
	get_movies_path,
	get_shows_path,
	)
from class_objects.radarr_api import *
from class_objects.radarr_class_methods import get_parsed_movie_title, parse_relpath
from class_objects.sonarr_api import *
from IO.YAML.yaml_to_object import (get_variable_from_yaml)
from logs.bin.get_parameters import (get_log_name, get_logger, get_method_main)
from movies.movie.movie_gets import (get_absolute_movie_file_path, get_relative_movie_file_path)
from movies.movies_gets import (get_relative_movies_path)
from plex_linker.parser.series import padded_absolute_episode, parsed_show_title, episode_title


class Globals:
	def __init__(self):
		self.sonarr = SonarrAPI()
		self.radarr = RadarrAPI()
		self.sonarr_root_folders = self.sonarr.get_root_folder()
		# self.radarr_root_folders = self.radarr.get_root_folder() # fairly sure this isnt a radarr endpoint
		self.full_sonarr_dict = self.sonarr.get_series()
		self.full_radarr_dict = self.radarr.get_movie_library()
		self.MEDIA_PATH = str(get_docker_media_path())
		self.MEDIA_DIRECTORY = str(get_host_media_path())
		self.LOG = get_logger(get_log_name())
		self.MOVIES_PATH = get_movies_path()
		self.MOVIE_EXTENSIONS = get_movie_extensions()
		self.SHOWS_PATH = get_shows_path()
		self.movies_dict = get_movies_dictionary_object()
		self.method = self.parent_method = get_method_main()
		pass


class Movies:
	def __init__(self, absolute_movies_path = abspath("/".join((str(environ['DOCKER_MEDIA_PATH']),
	                                                            get_variable_from_yaml("Movie Directories")[0])))):
		self.start_time = time.time()
		self.absolute_movies_path = absolute_movies_path
		self.relative_movies_path = get_relative_movies_path(self)


class MovieSchema(Schema):
	unparsed_title = fields.Function()
# movie_dictionary = fields.Movie.movie_dictionary()


class Movie(Movies, Globals):
	def __init__(self,
	             movie,
	             movie_dict,
	             g):
		super().__init__()
		# schema = MovieSchema()
		self.movie_dictionary = movie_dict
		g.LOG.debug(backend.debug_message(627, g, self.movie_dictionary))
		
		self.shows_dictionary = self.movie_dictionary['Shows']
		g.LOG.debug(backend.debug_message(645, g, self.shows_dictionary))
		self.tmbdid = self.movie_dictionary['Movie DB ID']
		g.LOG.debug(backend.debug_message(648, g, self.tmbdid))
		
		self.radarr_dictionary = self.parse_dict_from_radarr(g)
		try:
			self.hasFile = \
				self.movie_dictionary['Has File'] = \
				bool(self.radarr_dictionary['hasFile']) if 'hasFile' in self.radarr_dictionary else False
		except TypeError:
			self.hasFile = self.movie_dictionary['Has File'] = bool()
		g.LOG.debug(backend.debug_message(646, g, self.hasFile))
		try:
			self.monitored = \
				self.movie_dictionary['Monitored'] = \
				bool(self.radarr_dictionary['monitored']) if 'monitored' in self.radarr_dictionary else True
		except TypeError:
			self.monitored = self.movie_dictionary['Monitored'] = bool(True)
		g.LOG.debug(backend.debug_message(647, g, self.monitored))
		if 'Year' in self.movie_dictionary and self.movie_dictionary['Year'] != 0:
			self.year = int(self.movie_dictionary['Year'])
		else:
			self.year = self.movie_dictionary['Year'] = int(self.radarr_dictionary.pop('year', 0))
		self.unparsed_title = self.movie_dictionary['Unparsed Title'] = self.get_unparsed_movie_title(g).replace(' (0)',
		                                                                                                         str())
		self.movie_title = self.movie_dictionary['Title'] = str(get_parsed_movie_title(self, g)).replace(' (0)', str())
		self.relative_movie_path = self.init_relative_movie_path(g)
		self.absolute_movie_path = self.init_absolute_movie_path(g)
		if "movieFile" not in self.radarr_dictionary or not self.relative_movie_path:
			self.movie_file = self.movie_dictionary['Movie File'] = str()
			self.quality = self.movie_dictionary['Parsed Movie Quality'] = str()
			self.extension = self.movie_dictionary['Parsed Movie Extension'] = str()
			self.absolute_movie_file_path = str(self.movie_dictionary['Absolute Movie File Path'])
			self.relative_movie_file_path = str(self.movie_dictionary['Relative Movie File Path'])
			return
		file_dict = self.radarr_dictionary['movieFile']
		self.movie_file = self.movie_dictionary['Movie File'] = str(file_dict['relativePath'])
		g.LOG.debug(backend.debug_message(610, g, self.movie_file))
		self.quality = self.movie_dictionary['Parsed Movie Quality'] = str(file_dict['quality']['quality']['name'])
		g.LOG.debug(backend.debug_message(612, g, self.quality))
		self.extension = self.movie_dictionary['Parsed Extension'] = str(self.movie_file.split().pop()).replace(
				self.quality, str())[1:]
		self.absolute_movie_file_path = self.movie_dictionary['Absolute Movie File Path'] = str(
				get_absolute_movie_file_path(self, g))
		self.relative_movie_file_path = self.movie_dictionary['Relative Movie File Path'] = str(
				get_relative_movie_file_path(self, g))
	
	def get_unparsed_movie_title(self, g):
		result = str(self.radarr_dictionary['title']) \
			if 'title' in self.radarr_dictionary else self.movie_dictionary['Title']
		g.LOG.debug(backend.debug_message(643, g, result))
		return result
	
	def parse_dict_from_radarr(self, g):
		if str(self.movie_dictionary['Movie DB ID']).isdigit() and str(
				self.movie_dictionary['Movie DB ID']).isdigit() != 0:
			try:
				index = \
					[i for i, d in enumerate(g.full_radarr_dict) if (self.movie_dictionary['Movie DB ID'] in d.values())
					 and ("tmdbId" in d.keys() and d['tmdbId'] == self.movie_dictionary['Movie DB ID'])][0]
				g.LOG.debug(backend.debug_message(644, g, g.full_radarr_dict[index]))
				return g.full_radarr_dict[index]
			except IndexError:
				pass
		return dict()
	
	def init_absolute_movie_path(self, g):
		result = self.movie_dictionary['Absolute Movie Path'] = "/".join(
				(os.environ['DOCKER_MEDIA_PATH'], self.relative_movie_path))
		g.LOG.debug(backend.debug_message(614, g, str(result)))
		return result
	
	def init_relative_movie_path(self, g):
		result = self.movie_dictionary['Relative Movie Path'] = str(self.radarr_dictionary['path'])[1:] if 'path' in \
		                                                                                                   self.radarr_dictionary else str()
		g.LOG.debug(backend.debug_message(617, g, result))
		return result
	
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
		if quality.endswith(f"REAL.{self.extension}"):
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
		return str(quality)  # .rsplit( ".", 1 )[ 0 ] ) if it the extension is parsed separately


# TODO: make sure order allows everything to calculate from the API if not well defined

class Show(Movie, Globals):
	def __init__(self,
	             g,
	             series = str(),
	             film = str(),
	             show_dict = dict(),
	             movie_dict = dict()):
		super().__init__(film, movie_dict, g)
		# passed values
		self.show = series; g.LOG.debug(backend.debug_message(604, g, self.show))
		self.movie_dictionary = movie_dict; g.LOG.debug(backend.debug_message(627, g, self.movie_dictionary))
		self.series_dict = show_dict; g.LOG.debug(backend.debug_message(624, g, self.series_dict))
		# sonarr api info
		self.sonarr_series_dict = g.sonarr.lookup_series(self.show, g)
		self.series_id = parse_series.series_id(self.sonarr_series_dict, self.series_dict, g)
		self.tvdbId = parse_series.tvdb_id(self.sonarr_series_dict, self.series_dict, g)
		self.imdbId = parse_series.imdb_id(self.sonarr_series_dict, self.series_dict, g)
		self.show_genres = parse_series.parse_series_genres(self.sonarr_series_dict, self.series_dict, g)
		self.sonarr_api_query = parse_series.episode_dict_from_lookup(self, g)
		# TODO: may need to add episode # calculation first not sure yet
		self.episode_id = parse_series.episode_id(self, g)
		self.episode_dict = parse_series.parse_episode_dict(self, g)
		self.anime_status = bool(parse_series.anime_status(self, g))
		self.padding = parse_series.episode_padding(self, g)
		self.episode_file_id = parse_series.episode_file_id(self, g)
		self.episode_file_dict = parse_series.parse_episode_file_id_dict(self, g)
		link = str(self.episode_file_dict['path']).replace(str(os.environ['SONARR_ROOT_PATH_PREFIX']), str())
		self.has_link = \
			self.series_dict['Show Link Status'] = bool(True) if os.path.islink(str(os.path.exists(link))) else bool()
		self.link_status = fetch_series.symlink_status(self, g)
		print(self.has_link)
		breakpoint()
		# need to add monitored and file status info for episodes to determine this part
		# self.has_link =
		# technically not in use but could be really useful as a means of checking if a link is needed
		self.episode = [parse_series.episode_number(self, g)]
		self.parsed_episode = parse_series.padded_episode_number(self, g)
		self.absolute_episode = [parse_series.absolute_episode_number(self, g)]
		self.parsed_absolute_episode = padded_absolute_episode(self, g)
		self.season = parse_series.season_from_sonarr(self, g)
		self.season_folder = parse_series.season_folder_from_api(self, g)
		self.show_root_path = parse_series.show_root_folder(self, g)
		self.relative_show_path = parse_series.relative_show_path(self, g)
		self.episode_title = episode_title(self, g)
		self.parsed_show_title = parsed_show_title(self, g)
		g.sonarr.rescan_series(self.tvdbId)  # rescan movie in case it was picked up since last scan
		g.sonarr.refresh_series(self.tvdbId)  # to ensure metadata is up to date
