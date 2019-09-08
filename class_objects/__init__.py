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
from movies.movies_gets import (get_absolute_movies_path,
                                get_relative_movies_path)
from movies.movies_puts import (set_nested_dictionary_key_value_pair,
                                set_working_directory_to_media_path)


class Globals:
	def __init__(self):
		self.MEDIA_PATH = \
			get_variable_from_yaml("Media Directory")
		self.LOG = \
			get_logger(get_log_name())
		self.MOVIES_PATH = \
			get_variable_from_yaml("Movie Directories")
		self.MOVIE_EXTENSIONS = \
			get_variable_from_yaml("Movie Extensions")
		self.MEDIA_DIRECTORY = \
			get_variable_from_yaml("Media Directory")
		self.SHOWS_PATH = \
			get_variable_from_yaml("Show Directories")
		self.movies_dictionary_object = \
			get_yaml_dictionary()
		self.list_of_linked_movies = list()
		self.list_of_movies_to_locate = list()
		self.method = \
			self.parent_method = \
			get_method_main()
		pass


class Movies:
	def __init__(self,
	             g):
		self.start_time = \
			time.time()
		self.absolute_movies_path = \
			get_absolute_movies_path(g)
		self.relative_movies_path = \
			get_relative_movies_path(self,
			                         g)
		self.list_of_possible_paths = \
			[]


class Movie(Movies,
            Globals):
	def __init__(self,
	             title,
	             g):
		super().__init__(g)
		# globals_class_object.movies_dictionary_object[title]['Absolute Movie File Path'] = str()
		# globals_class_object.movies_dictionary_object[title]['Relative Movie File Path'] = str()
		self.movie_title = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[title]['Unparsed Movie Title'],
			                                     get_unparsed_movie_title(title,
			                                                              g))
		self.shows_dictionary_object = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[title]['Shows'],
			                                     [{}])
		self.movie_dictionary_object = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[title],
			                                     [{}])
		self.absolute_movie_path = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[title]['Absolute Movie Path'],
			                                     get_movie_path(self,
			                                                    g))
		self.relative_movie_path = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[title]['Relative Movie Path'],
			                                     get_relative_movie_path(self,
			                                                             g))
		self.quality = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[title]['Parsed Movie Quality'],
			                                     str())
		# g.movies_dictionary_object[title]['Parsed Movie Extension'] = str()
		self.extension = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[title]['Parsed Movie Extension'],
			                                     str())
		self.movie_file = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[title]['Parsed Movie File'],
			                                     str())
		if validated_movie_path_is_not_null(self,
		                                    g):
			validate_extensions_from_movie_file(self,
			                                    g)
			set_movie_quality(self,
			                  g)
			self.absolute_movie_file_path = \
				set_nested_dictionary_key_value_pair(g,
				                                     g.movies_dictionary_object[title]['Absolute Movie File Path'],
				                                     get_absolute_movie_file_path(self,
				                                                                  g))
			g.movies_dictionary_object[title]['Relative Movie File Path'] = str()
			self.relative_movie_file_path = \
				set_nested_dictionary_key_value_pair(g,
				                                     g.movies_dictionary_object[title]['Relative Movie File Path'],
				                                     get_relative_movie_file_path(self,
				                                                                  g))


# noinspection ProblematicWhitespace
class Show(Movie,
           Globals):
	def __init__(self,
	             show,
	             movie,
	             g):
		super().__init__(movie,
		                 g)
		set_working_directory_to_media_path(g.MEDIA_PATH)
		from movies.movie.shows.show.show_gets import get_alphabetical_specials_string
		# g.movies_dictionary_object[movie]['Shows'][show]['Parsed Season'] = str()
		# globals_class_object.movies_dictionary_object[movie]['Shows'][show]['Parsed Season Folder'] = str()
		# globals_class_object.movies_dictionary_object[movie]['Shows'][show]['Parsed Episode'] = str()
		# globals_class_object.movies_dictionary_object[movie]['Shows'][show]['Parsed Show Root Folder'] = str()
		# globals_class_object.movies_dictionary_object[movie]['Shows'][show]['Absolute Show Path'] = str()
		# globals_class_object.movies_dictionary_object[movie]['Shows'][show]['Parsed Relative Show Title'] = str()
		# globals_class_object.movies_dictionary_object[movie]['Shows'][show]['Show Dictionary Object'] = {}
		
		self.show = show
		self.title = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'][show]['Title'],
			                                     str(show))
		self.season = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'][show]['Parsed Season Folder'],
			                                     str(get_alphabetical_specials_string(g)))
		self.episode = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'][show]['Parsed Episode'],
			                                     str())
		self.parsed_season = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'][show]['Parsed Season'],
			                                     str())
		self.absolute_episode = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'][show]['Absolute Episode'],
			                                     str())
		self.anime_status = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'][show]['Anime'],
			                                     False)
		
		self.dictionary_of_shows = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'],
			                                     [{}])
		self.root_folders = str()
		self.parsed_title = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'][show]['Parsed Show Title'],
			                                     str())
		
		self.parsed_relative_title = \
			set_nested_dictionary_key_value_pair(g,
			                                     g.movies_dictionary_object[movie]['Shows'][show][
				                                     'Parsed Relative Show Title'],
			                                     str())
