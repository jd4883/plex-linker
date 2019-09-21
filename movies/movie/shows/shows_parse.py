#!/usr/bin/env python3
from os import readlink

import messaging.frontend as message
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from movies.movie.movie_gets import (get_movie_path, get_relative_movie_path)
from movies.movie.shows.show.create_class_object import init_show_object
from movies.movie.shows.show.show_puts import set_dictionary_show_root_path
from movies.movie.shows.show.show_validation import (validate_ready_to_link_movie_to_show)
from movies.movie.shows.shows_validation import check_if_valid_symlink_destination, check_if_valid_symlink_target


def parse_show_to_link(show, g):
	message.method_launch(g)
	for _ in show.shows_dictionary.items():
		if validate_ready_to_link_movie_to_show(show.quality):
			symlink_force(show, g)
			show.absolute_movie_path = show.movie_dictionary['Absolute Movie Path'] = str(get_movie_path(show, g))
			show.relative_movie_path = show.movie_dictionary['Relative Movie Path'] = str(get_relative_movie_path(show, g))
			set_permissions(show, g)
	message.method_exit(g)


def parse_shows_dictionary_object(movie, g):
	message.method_launch(g)
	for series in movie.shows_dictionary.keys():
		series = str(series)
		show = init_show_object(movie, series, g)
		if show.show_dictionary and \
				show.show_dictionary['Relative Show File Path'] \
				and validate_strings_match(f'{str(show.show_dictionary["Relative Show File Path"])}', \
				                           show.show_dictionary["Symlinked"]):
			if get_live_link(str(show.show_dictionary['Relative Show File Path'])) and \
					(check_if_valid_symlink_destination(str(show.show_dictionary['Relative Show File Path'])) and (
							check_if_valid_symlink_target(str(movie.movie_dictionary["Parsed Movie File"])))):
				print(f"No action required for {movie.movie_title}")
				continue
		try:
			show.show_dictionary['Symlinked'] = str()
		except TypeError:
			continue
		show.show_dictionary['Relative Show File Path'] = str()
		movie.movie_dictionary["Parsed Movie File"] = str()
		print(f'Checking for presence of "{movie.movie_title}"')
		parse_show_to_link(show, g)
		


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
def validate_strings_match(string1, string2):
	if str(string1).lower() == str(string2).lower():
		return True
	return False


def get_live_link(relative_show_path):
	if readlink(relative_show_path):
		return True
	return False


def set_show_root_path(api_query, show, g, movie):
	set_dictionary_show_root_path(api_query, show, g, movie)
	return g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path']
