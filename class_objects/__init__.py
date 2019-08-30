#!/usr/bin/env python3.7
import time

from IO.YAML.yaml_to_object import (get_yaml_dictionary,
                                    get_variable_from_yaml)
from logs.bin.get_parameters import (get_method_main,
                                     get_logger,
                                     get_log_name)
from messaging.frontend import (method_launch)
from movies.movie.movie_gets import (get_absolute_movie_file_path,
                                     get_relative_movie_file_path,
                                     get_movie_path,
                                     get_relative_movie_path, get_unparsed_movie_title)
from movies.movie.movie_puts import (set_movie_quality)
from movies.movie.movie_validation import (validate_extensions_from_movie_file,
                                           validated_movie_path_is_not_null)
from movies.movie.shows.shows_puts import (set_shows_dictionary_object)
from movies.movies_gets import (get_absolute_movies_path,
                                get_relative_movies_path)

MEDIA_PATH = get_variable_from_yaml("Media Directory")
MOVIES_PATH = get_variable_from_yaml("Movie Directories")
MOVIE_EXTENSIONS = get_variable_from_yaml("Movie Extensions")
SHOWS_PATH = get_variable_from_yaml("Show Directories")

class Globals:
	def __init__(self):
		pass

class Movies:
	def __init__(movies):
		movies.LOG = \
			movies.LOG = \
			get_logger(get_log_name())
		movies.path = get_variable_from_yaml("Media Directory")
		movies.MOVIES_PATH = MOVIES_PATH
		movies.MEDIA_PATH = MEDIA_PATH
		movies.MOVIE_EXTENSIONS = MOVIE_EXTENSIONS
		movies.extensions = MOVIE_EXTENSIONS
		movies.SHOWS_PATH = SHOWS_PATH
		movies.movies_dictionary_object = get_yaml_dictionary()
		movies.start_time = time.time()
		movies.method = get_method_main()
		movies.parent_method = get_method_main()
		movies.absolute_movies_path = get_absolute_movies_path(movies)
		movies.relative_movies_path = get_relative_movies_path(movies)
		movies.list_of_possible_paths = []
		pass


class Movie(Movies):
	def __init__(movie,
	             title):
		super().__init__()
		movie.relative_movie_path = ""
		method_launch(movie)
		# movie.movies_dictionary_object[title]['Unparsed Movie Title'] = {}
		# movie.movies_dictionary_object[title]['Unparsed Movie Title'] = get_unparsed_movie_title(movie.movies_dictionary_object[title]['Unparsed Movie Title'],		title)
		movie.movie_title = movie.movies_dictionary_object[title]['Unparsed Movie Title'] = get_unparsed_movie_title(
			movie, title)
		movie.shows_dictionary_object = set_shows_dictionary_object(movie)
		movie.movie_dictionary_object = movie.movies_dictionary_object[title]
		movie.movies_dictionary_object[title]['Absolute Movie Path'] = get_movie_path(movie)
		movie.absolute_movie_path = movie.movies_dictionary_object[title]['Absolute Movie Path']
		movie.movies_dictionary_object[title]['Relative Movie Path'] = get_relative_movie_path(movie)
		movie.relative_movie_path = movie.movies_dictionary_object[title]['Relative Movie Path']
		movie.quality = ""
		movie.extension = ""
		movie.movie_file = ""
		if validated_movie_path_is_not_null(movie):
			validate_extensions_from_movie_file(movie)
			set_movie_quality(movie)
			movie.absolute_movie_file_path = get_absolute_movie_file_path(movie)
			movie.relative_movie_file_path = get_relative_movie_file_path(movie)
			movie.shows = []
			try:
				movie.movies_dictionary_object[movie.movie_title]['Link Target'] = ""
			except TypeError:
				print(f'type error for {movie.movies_dictionary_object[movie.movie_title]}')
		pass


class Show(Movie):
	def __init__(show_object,
	             show,
	             movie):
		super().__init__(movie)
		from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
		method_launch(show_object)
		show_object.show = show
		show_object.season = get_alphabetical_specials_string()
		show_object.episode = ""
		show_object.absolute_episode = ""
		show_object.title = ""
		show_object.anime_status = False
		show_object.path = ""
		show_object.show_paths = []
		show_object.dictionary_of_shows = {}
		show_object.root_folders = []
		show_object.relative_show_path = ""
		show_object.absolute_show_path = ""
		show_object.parsed_title = ""
		show_object.live_linked_path = ""
		show_object.parsed_relative_title = ""
		show_object.show_dictionary_object = {}
		pass
