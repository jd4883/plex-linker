#!/usr/bin/env python3
from os import (chdir, environ)
from os.path import (abspath,
                     relpath)
from movies.movie.shows.show.show_parser import (get_parsed_show_title, parse_show, parse_root_path_string)
import messaging.frontend as message


def set_show_root_path(show,
                       g):
	message.method_launch(g)
	show.absolute_movie_path = abspath(show.path)
	show.parsed_title = parse_show(show,
	                               g)
	show.parsed_title = get_parsed_show_title(show)
	show.absolute_movie_path = abspath(f"{show.parsed_title}")
	show.relative_show_path = \
		show.show_dictionary['Relative Show File Path'] = relpath(f"{show.parsed_title}")
	message.method_exit(g)


def set_show(show,
             g):
	from movies.movie.shows.show.show_gets import get_show_root_path
	message.method_launch(g)
	init_show_object(show)
	# noinspection PyUnusedLocal
	try:
		if get_show_root_path(show,
		                      g):  # parent_movie_dictionary_object may be worth adding as an arg here
			set_show_root_path(show,
			                   g)
	except TypeError as err:
		# print(f"{g.method} had an error: {err}")  # testing
		pass
	message.method_exit(g)


def init_show_object(show):
	show.title = show.show
	chdir(str(environ['DOCKER_MEDIA_PATH']))


def set_season_dictionary_value(show):
	if show.sonarr_api_query['seasons'][0]['seasonNumber'] == 0:
		try:
			result = show.sonarr_api_query['seasons'][0].pop('seasonNumber')
			show.show['Season'] = result
			return show.show['Season']
		except TypeError:
			return str(0)
	return show.show['Season']


def set_dictionary_show_root_path(sonarr_api_query, show, g, movie):
	try:
		g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path'] = parse_root_path_string(sonarr_api_query)
	except (KeyError or TypeError):
		g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path'] = str()


def set_show_id(show, g):
	from movies.movie.shows.show.show_gets import get_show_id
	return get_show_id(show, g)
