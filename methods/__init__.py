from os.path import abspath

import messaging.backend as backend
import methods.sonarr_api
import methods.sonarr_class_methods
import plex_linker.cleanup.movie as cleanup_movie
import plex_linker.cleanup.series as cleanup_series
import plex_linker.fetch.series as fetch_series
import plex_linker.parser.series as parse_series
from IO.YAML.yaml_to_object import (get_variable_from_yaml)
from logs.bin.get_parameters import (get_log_name, get_logger, get_method_main)
from methods.misc_get_methods import (
	get_docker_media_path,
	get_host_media_path,
	get_movie_extensions,
	get_movies_dictionary_object,
	get_movies_path,
	get_shows_path,
	)
from methods.radarr_api import *
from methods.radarr_class_methods import get_parsed_movie_title, parse_relpath
from methods.sonarr_api import *
from plex_linker.compare.ids import validate_tmdbId
from plex_linker.fetch.series import fetch_link_status
from plex_linker.gets.movie import get_relative_movies_path
from plex_linker.gets.path import get_absolute_movie_file_path, get_relative_movie_file_path
from plex_linker.parser.series import padded_absolute_episode


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


# class MovieSchema(Schema):
# 	unparsed_title = fields.Function()


# parent_dict = fields.Movie.parent_dict()


class Movie(Movies, Globals):
	def __init__(self,
	             movie,
	             movie_dict,
	             g):
		super().__init__()
		# schema = MovieSchema()
		self.movie_dictionary = movie_dict
		g.LOG.info(backend.debug_message(627, g, self.movie_dictionary))
		cleanup_movie.cleanup_dict(self.movie_dictionary)
		self.shows_dictionary = self.movie_dictionary['Shows']
		g.LOG.info(backend.debug_message(645, g, self.shows_dictionary))
		self.tmbdid = self.movie_dictionary['Movie DB ID']
		g.LOG.info(backend.debug_message(648, g, self.tmbdid))
		
		self.radarr_dictionary = self.parse_dict_from_radarr(g)
		try:
			self.hasFile = \
				self.movie_dictionary['Has File'] = \
				bool(self.radarr_dictionary['hasFile']) if 'hasFile' in self.radarr_dictionary else False
		except TypeError:
			self.hasFile = self.movie_dictionary['Has File'] = bool()
		g.LOG.info(backend.debug_message(646, g, self.hasFile))
		try:
			self.monitored = \
				self.movie_dictionary['Monitored'] = \
				bool(self.radarr_dictionary['monitored']) if 'monitored' in self.radarr_dictionary else True
		except TypeError:
			self.monitored = self.movie_dictionary['Monitored'] = bool(True)
		g.LOG.info(backend.debug_message(647, g, self.monitored))
		
		self.year = self.movie_dictionary['Year'] = \
			int(self.radarr_dictionary['inCinemas'][0:4]) if 'inCinemas' in self.radarr_dictionary \
				else int(self.radarr_dictionary.get('year', 0))
		self.unparsed_title = re.sub("\s+\(0\)\s?", "", self.get_unparsed_movie_title(g))
		self.movie_title = re.sub("\s+\(0\)\s?", str(), get_parsed_movie_title(self, g))
		self.relative_movie_path = self.init_relative_movie_path(g)
		self.absolute_movie_path = self.init_absolute_movie_path(g)
		if "movieFile" not in self.radarr_dictionary or not self.relative_movie_path:
			self.movie_file = self.movie_dictionary['Movie File'] = str()
			self.quality = self.movie_dictionary['Parsed Quality'] = str()
			self.extension = self.movie_dictionary['Parsed Extension'] = str()
			self.absolute_movie_file_path = self.movie_dictionary['Absolute Movie File Path'] = str()
			self.relative_movie_file_path = self.movie_dictionary['Relative Movie File Path'] = str()
			return
		file_dict = self.radarr_dictionary['movieFile']
		self.movie_file = self.movie_dictionary['Movie File'] = str(file_dict['relativePath'])
		g.LOG.info(backend.debug_message(610, g, self.movie_file))
		self.quality = self.movie_dictionary['Parsed Movie Quality'] = str(file_dict['quality']['quality']['name'])
		g.LOG.info(backend.debug_message(612, g, self.quality))
		baseQuality = re.sub(self.quality, str(), str(self.movie_file.split().pop()))
		self.extension = self.movie_dictionary['Parsed Extension'] = re.sub("\s+REAL\.\W+$", "", baseQuality)
		self.absolute_movie_file_path = str(get_absolute_movie_file_path(self, g))
		self.relative_movie_file_path = str(get_relative_movie_file_path(self, g))
	
	def get_unparsed_movie_title(self, g):
		result = self.radarr_dictionary.get('title', str())
		g.LOG.info(backend.debug_message(643, g, result))
		return result
	
	def init_absolute_movie_path(self, g):
		result = self.movie_dictionary['Absolute Movie Path'] = "/".join((os.environ['DOCKER_MEDIA_PATH'],
		                                                                  self.relative_movie_path))
		g.LOG.info(backend.debug_message(614, g, str(result)))
		return result
	
	def init_relative_movie_path(self, g, result = str()):
		if 'path' in self.radarr_dictionary:
			result = self.movie_dictionary['Relative Movie Path'] = str(self.radarr_dictionary['path'])[1:]
		g.LOG.info(backend.debug_message(617, g, result))
		return result
	
	# def parse_tmdbid(self, g):
	# 	tmdbID = str()
	# 	if 'tmdbId' in self.radarr_dictionary:
	# 		if 'Movie DB ID' in self.movie_dictionary and self.movie_dictionary['Movie DB ID']:
	# 			tmdbID = self.movie_dictionary['Movie DB ID']
	# 		elif 'tmdbId' in self.radarr_dictionary[0] and int(self.radarr_dictionary[0]['tmdbId']) > 0:
	# 			tmdbID = int(self.radarr_dictionary[0]['tmdbId'])
	# 		g.radarr.rescan_movie(int(tmdbID)) if len(self.radarr_dictionary) > 0 else str()
	# 		# rescan movie in case it was picked up since last scan
	# 		g.radarr.refresh_movie(int(tmdbID)) if len(self.radarr_dictionary) > 0 else str()
	# 		# to ensure metadata is up to date
	# 		if len(self.radarr_dictionary) > 0 and self.radarr_dictionary[0]['monitored']:
	# 			g.radarr.movie_search(int(tmdbID))
	# 	return tmdbID
	
	def parse_dict_from_radarr(self, g):
		if validate_tmdbId(self.tmbdid):
			try:
				index = \
					[i for i, d in enumerate(g.full_radarr_dict) if
					 (self.movie_dictionary['Movie DB ID'] in d.values()) and (
							 "tmdbId" in d.keys() and d['tmdbId'] == self.movie_dictionary['Movie DB ID'])][0]
				g.LOG.info(backend.debug_message(644, g, g.full_radarr_dict[index]))
				return g.full_radarr_dict[index]
			except IndexError:
				pass
		return dict()


class Show(Movie, Globals):
	def __init__(self,
	             g,
	             series = str(),
	             film = str(),
	             show_dict = dict(),
	             movie_dict = dict()):
		super().__init__(film, movie_dict, g)
		self.show = series
		self.movie_dictionary = fetch_series.parent_dict(g, movie_dict)
		self.inherited_series_dict = show_dict
		self.season = str(self.inherited_series_dict.get("Season", str(0))).zfill(2)
		self.episode = str(self.inherited_series_dict.get("Episode", 0))
		self.parsed_episode = str(self.inherited_series_dict.get("Parsed Episode", str(00))).zfill(2)  # replace with
		# padding
		self.episode_id = str(self.inherited_series_dict.get("Episode ID", 0))
		self.episode_title = str(self.inherited_series_dict.get("Title", str()))
		self.series_id = str(self.inherited_series_dict.get("seriesId", int()))
		self.episode_dict = dict()
		self.has_link = self.inherited_series_dict['Has Link'] = self.inherited_series_dict.get('Has Link', bool())
		cleanup_series.cleanup_dict(self.inherited_series_dict)
		self.sonarr_series_dict = g.sonarr.lookup_series(self.show, g)
		print(f"SONARR READ IN DICT: {self.sonarr_series_dict}")
		
		self.series_id = parse_series.series_id(self.sonarr_series_dict, self.inherited_series_dict, self.show, g)
		self.tvdbId = parse_series.tvdb_id(self.sonarr_series_dict, self.inherited_series_dict, g)
		self.imdbId = parse_series.imdb_id(self.sonarr_series_dict, self.inherited_series_dict, g)
		self.show_genres = parse_series.parse_series_genres(self.sonarr_series_dict, self.inherited_series_dict, g)
		self.sonarr_api_query = parse_series.episode_dict_from_lookup(self, g)
		# TODO: may need to add episode # calculation first not sure yet
		self.anime_status = bool(parse_series.anime_status(self, g))
		self.padding = parse_series.episode_padding(self, g)
		# self.episode = parse_series.episode_number(self, g)
		parse_series.episode_id(self, g)
		self.episode_dict = parse_series.parse_episode_dict(self, g)
		if self.episode_dict:
			# TODO: anime status should go here
			parse_series.padded_episode_number(self, g)
			self.absolute_episode = parse_series.absolute_episode_number(self, g)
			self.parsed_absolute_episode = padded_absolute_episode(self, g)
			self.episode_title = re.sub('\(\d+\)$', "", self.get_title())
		from pprint import pprint
		pprint(self.episode_dict)
		# TODO: something is up here as many series that are not anime are being marked as anime, suspect the default
		#  false bool is never getting passed
		
		self.episode_file_id = parse_series.episode_file_id(self, g)
		self.episode_file_dict = parse_series.parse_episode_file_id_dict(self, g)
		self.link_status = fetch_series.symlink_status(self, g)
		self.sonarr_monitored = not bool()
		# self.season = parse_series.season_from_sonarr(self, g)
		self.season_folder = parse_series.season_folder_from_api(self, g)
		self.show_root_path = self.setShowRootPath(g)
		# self.show_root_path = parse_series.show_root_folder(self, g)
		self.relative_show_path = parse_series.relative_show_path(self, g)
		
		self.parsed_episode_title = parse_series.compiled_episode_title(self, g)
		self.relative_show_file_path = self.inherited_series_dict['Relative Show File Path'] = \
			(f"{self.parsed_episode_title} {self.quality}.{self.extension}" \
				 if (self.hasFile and self.parsed_episode_title) else str()).replace("..", ".")
		relativeMovieFilePath = fetch_link_status(self,
		                                          self.episode_file_dict,
		                                          self.relative_movie_file_path) if self.episode_file_dict else bool()
		self.has_link = self.inherited_series_dict['Has Link'] = relativeMovieFilePath
		g.sonarr.rescan_series(self.tvdbId)  # rescan movie in case it was picked up since last scan
		g.sonarr.refresh_series(self.tvdbId)  # to ensure metadata is up to date
	
	def get_title(self):
		payload = fetch_series.show_path_string(self.episode_dict['title'] if "title" in self.episode_dict else str())
		return payload
	
	def setShowRootPath(self, g):
		payload = parse_series.show_root_folder(self, g)
		if 'path' in self.sonarr_series_dict and self.sonarr_series_dict["path"]:
			payload = self.sonarr_series_dict["path"]
		return payload
