#!/usr/bin/env python3
from os import readlink

from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from messaging.frontend import (method_launch,
                                method_exit)
from movies.movie.movie_gets import (get_relative_movie_path,
                                     get_movie_path)
from movies.movie.shows.show.create_class_object import init_show_object
from movies.movie.shows.show.show_puts import set_dictionary_show_root_path
from movies.movie.shows.show.show_validation import (validate_ready_to_link_movie_to_show)
from movies.movie.shows.shows_validation import check_if_valid_symlink_destination, check_if_valid_symlink_target


def parse_show_to_link(self,
                       g):
	method_launch(g)
	for _ in self.shows_dictionary.items():
		if validate_ready_to_link_movie_to_show(self.quality, g):
			symlink_force(self, g)
			self.absolute_movie_path = self.movie_dictionary['Absolute Movie Path'] = str(get_movie_path(self, g))
			self.relative_movie_path = self.movie_dictionary['Relative Movie Path'] = str(get_relative_movie_path(self, g))
			set_permissions(self, g)
	method_exit(g)


# noinspection PyUnusedLocal
def parse_shows_dictionary_object(self,
                                  g):
	method_launch(g)
	for show in self.shows_dictionary.keys():
		show = str(show)
		tv = init_show_object(self, show, g)
		try:
			if tv.show_dictionary and tv.show_dictionary['Relative Show File Path'] and \
					validate_strings_match(f'{str(tv.show_dictionary["Relative Show File Path"])}', \
					                       tv.show_dictionary['Symlinked']):
				if get_live_link(str(tv.show_dictionary['Relative Show File Path'])) and \
						(check_if_valid_symlink_destination(str(tv.show_dictionary['Relative Show File Path'])) and
						 (check_if_valid_symlink_target(str(self.movie_dictionary["Parsed Movie File"])))):
					print(f"No action required for {self.movie_title}")
					continue
		except (FileNotFoundError or TypeError or KeyError) as err:
			pass
		try:
			tv.show_dictionary['Symlinked'] = str()
			tv.show_dictionary['Relative Show File Path'] = str()
			self.movie_dictionary["Parsed Movie File"] = str()
			print(f'Checking for presence of "{self.movie_title}"')
			parse_show_to_link(tv,
			                   g)
		except TypeError or KeyError as err:
			print(f"ERROR PARSING {show} with message {err}")
	# try:
	# 	for genre in tv_show.sonarr_api_query['genres']:
	# 		# [g.sonarr.set_new_tag_for_sonarr({"label": str(genre).lower()}) for genre in sorted(tv_show.sonarr)]
	# 		# [g.sonarr.set_new_tag_for_sonarr(str(genre).lower()) for genre in sorted(g.sonarr_genres)]
	# 		# definitely need to validate this workas as intended
	# 		g.sonarr.set_series_tags({'label': str(genre).lower()},
	# 		                         g.movies_dictionary_object[self.movie_title]['Shows'][self]['Show ID'])
	# 		tag_id = get_tag_id(self,
	# 		                    g,
	# 		                    self.movie_title,
	# 		                    genre)
	# except AttributeError:
	# 	# this should trigger if the API query is empty, seems to once in a while be the case
	# 	continue


# noinspection PySameParameterValue
def validate_strings_match(string1,
                           string2):
	if str(string1).lower() == str(string2).lower():
		return True
	return False


def get_live_link(relative_show_path):
	# probably can make the logic a bit more clever here and check if the path put together from the parsed elements
	# already has a valid link, if not parse else continue to next item
	# noinspection PyUnusedLocal
	try:
		readlink(relative_show_path)
	except FileNotFoundError as err:
		# print(f"{g.method} had a AttributeError: {err}") # testing
		return False
	return True


def set_show_root_path(sonarr_api_query, show, g,
                       movie):
	set_dictionary_show_root_path(sonarr_api_query,
	                              show,
	                              g,
	                              movie)
	return g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path']
