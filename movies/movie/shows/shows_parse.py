#!/usr/bin/env python3
from os import readlink

from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from messaging.frontend import (method_launch,
                                method_exit)
from movies.movie.movie_gets import (get_relative_movie_path,
                                     get_movie_path)
from movies.movie.shows.show.create_class_object import create_tv_show_class_object, get_tag_id
from movies.movie.shows.show.show_puts import set_dictionary_show_root_path
from movies.movie.shows.show.show_validation import (validate_ready_to_link_movie_to_show)
from movies.movie.shows.shows_validation import check_if_valid_symlink_destination, check_if_valid_symlink_target


def parse_show_to_link(show,
                       g):
	method_launch(g)
	for _ in g.movies_dictionary_object[show.movie_title]['Shows'].items():
		if validate_ready_to_link_movie_to_show(show.quality,
		                                        g):
			symlink_force(show,
			              g)
			show.absolute_movie_path = g.movies_dictionary_object[show.movie_title]['Absolute Movie Path'] = \
				str(get_movie_path(show,
				                   g))
			show.relative_movie_path = g.movies_dictionary_object[show.movie_title]['Relative Movie Path'] = \
				str(get_relative_movie_path(show,
				                            g))
			set_permissions(show,
			                g)
	method_exit(g)


# noinspection PyUnusedLocal
def parse_shows_dictionary_object(self,
                                  g):
	method_launch(g)
	for show in g.movies_dictionary_object[self.movie_title]['Shows'].keys():
		show = str(show)
		tv_show = create_tv_show_class_object(self,
		                                      show,
		                                      g)
		
		try:
			if validate_strings_match(
					f'{str(g.movies_dictionary_object[self.movie_title]["Shows"][show]["Relative Show File Path"])} -> {readlink(str(g.movies_dictionary_object[self.movie_title]["Shows"][show]["Relative Show File Path"]))}', \
					g.movies_dictionary_object[self.movie_title]['Shows'][show]['Symlinked']):
				if get_live_link(
						str(g.movies_dictionary_object[self.movie_title]['Shows'][show]['Relative Show File Path'])) and \
						(check_if_valid_symlink_destination(
							str(g.movies_dictionary_object[self.movie_title]['Shows'][show]['Relative Show File Path'])) and
						 (check_if_valid_symlink_target(
							 str(g.movies_dictionary_object[self.movie_title]["Parsed Movie File"])))):
					print(f"No action required for {self.movie_title}")
					# make an official message handler here
					g.list_of_linked_movies.append(self.movie_title)
					continue
		except FileNotFoundError:
			g.movies_dictionary_object[self.movie_title]['Shows'][show]['Symlinked'] = str()
			g.movies_dictionary_object[self.movie_title]['Shows'][show]['Relative Show File Path'] = str()
			g.movies_dictionary_object[self.movie_title]["Parsed Movie File"] = str()
			print(f'Checking for presence of "{self.movie_title}"')
			parse_show_to_link(tv_show,
			                   g)
		try:
			for genre in tv_show.sonarr_api_query['genres']:
				g.sonarr.set_series_tags({'label': str(genre).lower()},
				                         g.movies_dictionary_object[self.movie_title]['Shows'][show]['Show ID'])
				tag_id = get_tag_id(show,
				                    g,
				                    self.movie_title,
				                    genre)
		except AttributeError:
			# this should trigger if the API query is empty, seems to once in a while be the case
			continue


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
