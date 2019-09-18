#!/usr/bin/env python3
from os import (chdir, environ)
from os.path import (abspath,
                     relpath)

from messaging.frontend import (display_show_class_attributes,
                                method_exit,
                                method_launch)
from movies.movie.shows.show.show_parser import parse_root_path_string


def set_show_root_path(show_object,
                       g):
	method_launch(g)
	from movies.movie.shows.show.show_parser import (get_parsed_show_title,
	                                                 parse_show)
	show_object.absolute_movie_path = abspath(show_object.path)
	show_object.parsed_title = parse_show(show_object,
	                                      g)
	show_object.parsed_title = get_parsed_show_title(show_object)
	show_object.absolute_movie_path = abspath(f"{show_object.parsed_title}", )
	show_object.relative_show_path = \
		g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Relative Show File Path'] = \
		relpath(f"{show_object.parsed_title}")
	method_exit(g)


def set_show(show_object,
             g):
	from movies.movie.shows.show.show_gets import get_show_root_path
	method_launch(g)
	init_show_object(show_object)
	display_show_class_attributes(show_object,
	                              g)
	# noinspection PyUnusedLocal
	try:
		if get_show_root_path(show_object,
		                      g):  # parent_movie_dictionary_object may be worth adding as an arg here
			set_show_root_path(show_object,
			                   g)
	except TypeError as err:
		# print(f"{g.method} had an error: {err}")  # testing
		pass
	method_exit(g)


def init_show_object(show_object):
	show_object.title = show_object.show
	chdir(str(environ['DOCKER_MEDIA_PATH']))


def set_season_dictionary_value(show,
                                sonarr_api_query):
	try:
		show['Season'] = str(0)
	except TypeError:
		show = dict(show)
		show['Season'] = str(0)
	if sonarr_api_query['seasons'][0]['seasonNumber'] == 0:
		try:
			result = sonarr_api_query['seasons'][0].pop('seasonNumber')
			show['Season'] = result
			return show['Season']
		except TypeError:
			pass
	return show['Season']


def set_dictionary_show_root_path(sonarr_api_query,
                                  show,
                                  g,
                                  movie):
	try:
		g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path'] = parse_root_path_string(sonarr_api_query)
	except KeyError or TypeError:
		g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path'] = str()


def set_show_id(show, g):
	from movies.movie.shows.show.show_gets import get_show_id
	return get_show_id(show, g)
