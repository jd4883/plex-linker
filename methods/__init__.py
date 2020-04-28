from os.path import abspath

import methods.sonarr_api
import methods.sonarr_class_methods
import plex_linker.cleanup.movie as cleanup_movie
import plex_linker.fetch.series as fetch_series
import plex_linker.parser.series as parse_series
from IO.YAML.yaml_to_object import (get_variable_from_yaml)
from logs.bin.get_parameters import (get_log_name, get_logger, get_method_main)
from messaging import backend as backend
from methods.misc_get_methods import (
	get_docker_media_path,
	get_host_media_path,
	get_movie_extensions,
	get_movies_dictionary_object,
	get_movies_path,
	get_shows_path,
	)
from pprint import pprint
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
		# self.radarr_root_folders = self.radarr.get_root_folder()  # fairly sure this isnt a radarr endpoint
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


# def __repr__(self):
# 	return "<Globals(name={self.name!r})>".format(self = self)


class Movies:
	def __init__(self, absolute_movies_path = abspath("/".join((str(environ['DOCKER_MEDIA_PATH']),
	                                                            get_variable_from_yaml(
			                                                            "Movie Directories").__iter__().__next__())))):
		self.start_time = time.time()
		self.absolute_movies_path = absolute_movies_path
		self.relative_movies_path = get_relative_movies_path(self)


# def __repr__(self):
# 	return "<Show(name={self.name!r})>".format(self = self)


class Movie(Movies, Globals):
	def __init__(self,
	             movie_dict,
	             g):
		super().__init__()
		# schema = MovieSchema()
		self.movie_dictionary = movie_dict
		self.shows_dictionary = self.movie_dictionary['Shows']
		cleanup_movie.cleanup_dict(self.movie_dictionary)
		self.tmbdid = self.movie_dictionary['Movie DB ID']
		g.LOG.debug(backend.debug_message(627, g, self.movie_dictionary))
		g.LOG.debug(backend.debug_message(645, g, self.shows_dictionary))
		g.LOG.debug(backend.debug_message(648, g, self.tmbdid))
		### FROM RADARR API FULL DICT
		self.radarr_dictionary = None
		self.hasFile = bool
		self.monitored = bool
		self.year = int
		
		################################################
		
		### NOT BY API CALL FOR NOW
		self.absolute_movie_file_path = str
		self.absolute_movie_path = str
		self.extension = str
		self.movieFile = str
		self.movie_title = str
		self.quality = str
		self.relative_movie_file_path = str
		self.relative_movie_file_path = str
		self.relative_movie_path = str
		self.unparsed_title = str
		################################################
		self.radarr_dictionary = self.parse_dict_from_radarr(g)
		self.init(g)
	
	def init(self, g):
		self.unparsed_title = re.sub("\s+\(0\)\s?", str(), self.radarr_dictionary.get('title', str()))
		self.movie_title = re.sub("\s+\(0\)\s?", str(), re.sub("/", "+", re.sub(":", "-", f"{self.unparsed_title} ({self.year})")))
		g.LOG.debug(backend.debug_message(643, g, self.unparsed_title))
		self.relative_movie_path = self.init_relative_movie_path(g)
		self.absolute_movie_path = self.init_absolute_movie_path(g)
		if self.movieFile:
			file_dict = self.radarr_dictionary['movieFile']
			self.movieFile = self.movie_dictionary['Movie File'] = str(file_dict['relativePath'])
			self.quality = self.movie_dictionary['Parsed Movie Quality'] = str(file_dict['quality']['quality']['name'])
			baseQuality = re.sub(self.quality, str(), str(self.movieFile.split().pop()))
			self.extension = self.movie_dictionary['Parsed Extension'] = re.sub("\s+REAL\.\W+$", "", baseQuality)
			self.absolute_movie_file_path = str(get_absolute_movie_file_path(self, g))
			self.relative_movie_file_path = str(get_relative_movie_file_path(self, g))
		g.LOG.debug(backend.debug_message(610, g, self.movieFile))
		g.LOG.debug(backend.debug_message(612, g, self.quality))
	
	def __repr__(self):
		return "<Movie(name={self.movie_title!r})>".format(self = self)
		
	def init_absolute_movie_path(self, g):
		result = self.movie_dictionary['Absolute Movie Path'] = "/".join((os.environ['DOCKER_MEDIA_PATH'],
		                                                                  self.relative_movie_path))
		g.LOG.debug(backend.debug_message(614, g, str(result)))
		return result
	
	def init_relative_movie_path(self, g, result = str()):
		if 'path' in self.radarr_dictionary:
			result = self.movie_dictionary['Relative Movie Path'] = str(self.radarr_dictionary['path'])[1:]
		g.LOG.debug(backend.debug_message(617, g, result))
		return result
	
	def parse_dict_from_radarr(self, g):
		if validate_tmdbId(self.tmbdid):
			try:
				index = \
					[i for i, d in enumerate(g.full_radarr_dict) if
					 (self.movie_dictionary['Movie DB ID'] in d.values()) and (
							 "tmdbId" in d.keys() and d['tmdbId'] == self.movie_dictionary['Movie DB ID'])][0]
				g.LOG.debug(backend.debug_message(644, g, g.full_radarr_dict[index]))
				
				items = g.full_radarr_dict[index]
				self.hasFile = items.get("hasFile", False)
				self.monitored = items.get("monitored", False)
				self.year = items.get('year', 0)# if 'inCinemas' not in items else items.pop('inCinemas')[0:4]
				pprint(self.radarr_dictionary)
				g.LOG.debug(backend.debug_message(646, g, self.hasFile))
				g.LOG.debug(backend.debug_message(647, g, self.monitored))
				self.radarr_dictionary = items
			except IndexError:
				pass
		return dict()


class Show(Movie, Globals):
	def __repr__(self):
		return "<Show(name={self.name!r})>".format(self = self)
	
	def __init__(self,
	             g,
	             series = str(),
	             show_dict = dict(),
	             movie_dict = dict()):
		super().__init__(movie_dict, g)
		self.inherited_series_dict = show_dict
		self.episode = self.inherited_series_dict.get('Episode')
		self.movie_dictionary = fetch_series.parent_dict(g, movie_dict)
		self.cleanup_input_data()
		self.absoluteEpisodeNumber = int
		
		### SET BY LOOKUP SERIES METHOD ###
		self.anime_status = bool
		self.cleanTitle = str
		self.firstAired = str
		self.genres = list
		self.id = int
		self.imdbId = str
		self.languageProfileId = int
		self.path = str
		self.profileId = int
		self.qualityProfileId = int
		self.ratings = list
		self.runtime = int
		self.seasonCount = int
		self.seasonFolder = bool
		self.seasons = list
		self.seriesId = int
		self.seriesType = str
		self.sortTitle = str
		self.status = str
		self.tags = list
		self.title = str(series)
		self.titleSlug = str
		self.tvdbId = int
		self.tvMazeId = int
		self.tvRageId = int
		self.useSceneNumbering = bool
		self.year = int
		
		### FIELDS PULLED GET EPISODES FROM SERIES ID ###
		self.absolute_episode_path = int
		self.episode_size = int
		self.episodeFileId = int
		self.episodeId = int
		self.episodeNumber = int
		self.episodeTitle = str()
		self.hasFile = bool
		self.language_dict = dict
		self.monitored = bool
		self.padding = int
		self.parsedEpisode = str
		self.quality_dict = dict
		self.qualityCutoffNotMet = bool
		self.relative_episode_path = int
		self.relativePath = str
		self.season = self.seasonNumber = str(int()).zfill(2)
		# TODO: this should be dynamic to handle unusual edge cases
		self.unverifiedSceneNumbering = bool
		#######################################
		
		### PARSED OUTSIDE OF API CALLS
		### THIS SEGMENT MAYBE CAN BE FACTORED OUT
		self.episode_dict = None
		self.episode_file_dict = None
		self.has_link = bool
		self.parsed_absolute_episode = str
		self.parsed_episode_title = str
		self.relative_show_file_path = str
		self.relative_show_path = str
		self.sceneEpisodeNumber = bool
		self.sceneSeasonNumber = bool
		
		self.path = str
		self.sonarr_series_dict = dict
	
	#######################################
	
	def init(self, g):
		g.LOG.debug(backend.debug_message(618, g, self.tvdbId))
		g.sonarr.get_episodes_by_series_id(self)
		self.inherited_series_dict['Episode ID'] = self.episodeId
		self.episode_dict = parse_series.parse_episode_dict(self, g)
		if self.episode_dict:
			self.absoluteEpisodeNumber = parse_series.absolute_episode_number(self, g)
			self.parsed_absolute_episode = padded_absolute_episode(self, g)
		# * general ease of readability cleanup
		# * DB integration will make a world of a difference here
		
		self.has_link = self.inherited_series_dict['Has Link'] = self.inherited_series_dict.get('Has Link', bool())
		self.seasonFolder = parse_series.season_folder_from_api(self, g)
		self.relative_show_path = self.inherited_series_dict['Relative Show Path'] = parse_series.relative_show_path(
				self, g)
		self.episode_file_dict = parse_series.parse_episode_file_id_dict(self, g)
		self.parsed_episode_title = self.inherited_series_dict['Parsed Episode Title'] = \
			parse_series.compiled_episode_title(self, g)
		self.relative_show_file_path = self.inherited_series_dict['Parsed Relative Show File Path'] = \
			(f"{self.parsed_episode_title} {self.quality}.{self.extension}" \
				 if (self.hasFile and self.parsed_episode_title) else str()).replace("..", ".")
		relativeMovieFilePath = fetch_link_status(self,
		                                          self.episode_file_dict,
		                                          self.relative_movie_file_path) if self.episode_file_dict else bool()
		# TODO: this spot seems to not parse out link status correctly
		self.has_link = self.inherited_series_dict['Has Link'] = relativeMovieFilePath
		g.sonarr.rescan_series(self.tvdbId)
		g.sonarr.refresh_series(self.tvdbId)
	
	def parseEpisode(self):
		try:
			result = "-".join([str(e).zfill(self.padding) for e in self.episode])
		except TypeError:
			result = str(self.episode).zfill(self.padding)
		self.parsedEpisode = self.inherited_series_dict['Parsed Episode'] = result
		print(f"EPISODE PARSED OUT: {self.parsedEpisode}")
		
	
	def cleanup_input_data(self):
		"""
			PROTOTYPE CLEANUP METHOD FOR EMPTY KEYS
			"""
		dict_fields = [
				"Absolute Episode",
				"Anime",
				"Has Link",
				"Parsed Episode",
				"Parsed Episode Title",
				"Relative Show File Path",
				"Relative Show Path",
				"Show Genres",
				"Show Root Path",
				"imdbId",
				"seriesId",
				"tvdbId"]
		for i in dict_fields:
			try:
				del self.inherited_series_dict[i]
			except KeyError:
				pass
		for i in self.inherited_series_dict:
			if not i:
				try:
					del self.inherited_series_dict[i]
				except KeyError:
					pass
