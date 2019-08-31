#!/usr/bin/env python3.7
import time

from IO.YAML.yaml_to_object import (get_yaml_dictionary,
                                    get_variable_from_yaml)
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
from movies.movie.shows.shows_puts import (set_shows_dictionary_object)
from movies.movies_gets import (get_absolute_movies_path,
                                get_relative_movies_path)
from movies.movies_puts import set_working_directory_to_media_path


class Globals:
	def __init__(self):
		self.MEDIA_PATH = get_variable_from_yaml("Media Directory")
		self.LOG = get_logger(get_log_name())
		self.MOVIES_PATH = get_variable_from_yaml("Movie Directories")
		self.MOVIE_EXTENSIONS = get_variable_from_yaml("Movie Extensions")
		self.MEDIA_DIRECTORY = get_variable_from_yaml("Media Directory")
		self.SHOWS_PATH = get_variable_from_yaml("Show Directories")
		self.movies_dictionary_object = get_yaml_dictionary()
		self.method = get_method_main()
		self.parent_method = get_method_main()
		pass


class Movies:
	def __init__(movies,
	             g):
		# movies.g = Globals()
		# movies.MEDIA_PATH = movies.g.MEDIA_PATH
		# movies.LOG = movies.g.LOG
		# movies.path = movies.g.MEDIA_DIRECTORY
		# movies.MOVIES_PATH = movies.g.MEDIA_PATH
		# movies.MOVIE_EXTENSIONS = movies.g.MOVIE_EXTENSIONS
		# movies.extensions = movies.g.MOVIE_EXTENSIONS
		# movies.SHOWS_PATH = movies.g.MOVIE_EXTENSIONS
		# movies.movies_dictionary_object = movies.g.movies_dictionary_object
		movies.start_time = time.time()
		# movies.method = movies.g.method
		# movies.parent_method = movies.g.parent_method
		movies.absolute_movies_path = get_absolute_movies_path(g)
		movies.relative_movies_path = get_relative_movies_path(movies,
		                                                       g)
		movies.list_of_possible_paths = []


class Movie(Movies,
            Globals):
	def __init__(movie,
	             title,
	             g):
		super().__init__(g)
		movie.relative_movie_path = ""
		movie.movie_title = g.movies_dictionary_object[title]['Unparsed Movie Title'] = get_unparsed_movie_title(title,
		                                                                                                         g)
		movie.absolute_movie_path = get_movie_path(movie,
		                                           g)
		movie.shows_dictionary_object = set_shows_dictionary_object(movie,
		                                                            g)
		movie.movie_dictionary_object = g.movies_dictionary_object[title]
		g.movies_dictionary_object[title]['Absolute Movie Path'] = get_movie_path(movie,
		                                                                          g)
		
		g.movies_dictionary_object[title]['Relative Movie Path'] = get_relative_movie_path(movie,
		                                                                                   g)
		movie.relative_movie_path = get_relative_movie_path(movie,
		                                                    g)
		movie.quality = ""
		movie.extension = ""
		movie.movie_file = ""
		if validated_movie_path_is_not_null(movie,
		                                    g):
			validate_extensions_from_movie_file(movie,
			                                    g)
			set_movie_quality(movie,
			                  g)
			movie.absolute_movie_file_path = get_absolute_movie_file_path(movie,
			                                                              g)
			movie.relative_movie_file_path = get_relative_movie_file_path(movie,
			                                                              g)


class Show(Movie,
           Globals):
	def __init__(show_object,
	             show,
	             movie,
	             g):
		super().__init__(movie,
		                 g)
		set_working_directory_to_media_path(g.MEDIA_PATH)
		from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
		show_object.show = show
		show_object.season = get_alphabetical_specials_string(g)
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
