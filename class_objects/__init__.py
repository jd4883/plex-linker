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
from class_objects.sonarr_class_methods import (
	get_parsed_relative_show_title,
	get_relative_show_path,
	get_parsed_show_title,
	set_root_path,
	)
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
			self.movie_dictionary['Title'] = \
			self.movie_dictionary['Unparsed Movie Title'] = \
			str(parse_movie_title(self.radarr_dictionary, movie))
		self.shows_dictionary = get_shows_dictionary(self.movie_dictionary)
		self.absolute_movie_path = \
			self.movie_dictionary['Absolute Movie Path'] = str(get_movie_path(self, g))
		# from API
		# seem to be having buggy behavior with aphrodite API, all my API calls give inaccurate info about files on disk
		# print(self.radarr_dictionary)
		self.relative_movie_path = self.movie_dictionary['Relative Movie Path'] = str(parse_relpath(self, g, media_path))
		self.quality = str(self.movie_dictionary['Parsed Movie Quality'])
		self.extension = str(self.movie_dictionary['Parsed Movie Extension'])
		self.movie_file = str(self.movie_dictionary['Parsed Movie File'])
		validate_extensions_from_movie_file(self, g)
		self.absolute_movie_file_path = \
			self.movie_dictionary['Absolute Movie File Path'] = str(get_absolute_movie_file_path(self))
		self.relative_movie_file_path = \
			self.movie_dictionary['Relative Movie File Path'] = str(get_relative_movie_file_path(self))


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
		self.show_root_path = self.show_dictionary['Show Root Path'] = set_root_path(self.sonarr_api_query)
		self.parsed_title = str(get_parsed_show_title(self.show_dictionary))
		self.relative_show_path = str(get_relative_show_path(self.show_dictionary))
		self.parsed_relative_title = str(get_parsed_relative_show_title(self.show_dictionary))
		# assign at class object level and return
		self.show_id = self.show_dictionary['Show ID'] = parse_show_id(self.show, g)
		self.raw_episodes = list(g.sonarr.get_episodes_by_series_id(self.show_dictionary['Show ID']))
		self.raw_episode_files = g.sonarr.get_episode_files_by_series_id(self.show_dictionary['Show ID'])
		self.season = self.show_dictionary['Season'] = str(class_objects.sonarr_class_methods.season_dictionary(self)).zfill(2)
		self.episode = str(self.show_dictionary['Parsed Episode'])
		self.absolute_episode = str(self.show_dictionary['Absolute Episode'])
