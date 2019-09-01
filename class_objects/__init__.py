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
from movies.movie.shows.show.episode.episode_gets import get_anime_status_from_dictionary
from movies.movie.shows.show.show_gets import get_show_root_folders_from_parent_dictionary
from movies.movie.shows.shows_gets import get_shows_dictionary_from_parent_dictionary
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
		movies.start_time = time.time()
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
		movie.movie_title = \
			g.movies_dictionary_object[title]['Unparsed Movie Title'] = \
			get_unparsed_movie_title(title,
			                         g)
		movie.absolute_movie_path = \
			g.movies_dictionary_object[title]['Absolute Movie Path'] = \
			get_movie_path(movie,
			               g)
		movie.shows_dictionary_object = \
			g.movies_dictionary_object[title]['Shows'] = \
			set_shows_dictionary_object(movie,
			                            g)
		movie.movie_dictionary_object = \
			g.movies_dictionary_object[title]
		g.movies_dictionary_object[title]['Absolute Movie Path'] = \
			get_movie_path(movie,
			               g)
		movie.relative_movie_path = \
			g.movies_dictionary_object[title]['Relative Movie Path'] = \
			get_relative_movie_path(movie,
			                        g)
		movie.quality = \
			g.movies_dictionary_object[title]['Parsed Movie Quality'] = \
			str("")
		movie.extension = \
			g.movies_dictionary_object[title]['Parsed Movie Extension'] = \
			str("")
		movie.movie_file = \
			g.movies_dictionary_object[title]['Parsed Movie File'] = \
			str("")
		if validated_movie_path_is_not_null(movie,
		                                    g):
			validate_extensions_from_movie_file(movie,
			                                    g)
			set_movie_quality(movie,
			                  g)
			movie.absolute_movie_file_path = \
				g.movies_dictionary_object[title]['Absolute Movie File Path'] = \
				get_absolute_movie_file_path(movie,
				                             g)
			movie.relative_movie_file_path = \
				g.movies_dictionary_object[title]['Relative Movie File Path'] = \
				get_relative_movie_file_path(movie,
				                             g)


class Show(Movie,
           Globals):
	def __init__(show_class_object,
	             show,
	             movie,
	             g):
		super().__init__(movie,
		                 g)
		set_working_directory_to_media_path(g.MEDIA_PATH)
		from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
		show_class_object.title = \
			show_class_object.show = \
			g.movies_dictionary_object[movie]['Shows'][show]['Title'] = str(show)
		show_class_object.season = \
			g.movies_dictionary_object[movie]['Shows'][show]['Parsed Season Folder'] = \
			str(get_alphabetical_specials_string(g))
		show_class_object.episode = \
			g.movies_dictionary_object[movie]['Shows'][show]['Parsed Episode'] = \
			str("")
		from movies.movie.shows.show.episode.episode_gets import get_parsed_absolute_episode_from_parent_dictionary
		show_class_object.absolute_episode = get_parsed_absolute_episode_from_parent_dictionary(g,
		                                                                                        movie,
		                                                                                        show)
		show_class_object.anime_status = \
			get_anime_status_from_dictionary(g,
			                                 movie,
			                                 show)
		show_class_object.dictionary_of_shows = get_shows_dictionary_from_parent_dictionary(show_class_object,
		                                                                                    g)
		show_class_object.root_folders = get_show_root_folders_from_parent_dictionary(show_class_object,
		                                                                              g)
		show_class_object.relative_show_path = ""
		show_class_object.absolute_show_path = ""
		show_class_object.parsed_title = ""
		show_class_object.live_linked_path = ""
		show_class_object.parsed_relative_title = ""
		show_class_object.show_dictionary_object = {}
