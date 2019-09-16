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
	try:
		if get_show_root_path(show_object,
		                      g):  # parent_movie_dictionary_object may be worth adding as an arg here
			set_show_root_path(show_object,
			                   g)
	except TypeError:
		pass
	method_exit(g)


def init_show_object(show_object):
	show_object.title = show_object.show
	chdir(str(environ['DOCKER_MEDIA_PATH']))


def set_season_dictionary_value(sonarr_api_query, show, g,
                                movie):
	if sonarr_api_query['seasons'][0]['seasonNumber'] != 0:
		g.movies_dictionary_object[movie]['Shows'][show]['Season'] = 0
	else:
		g.movies_dictionary_object[movie]['Shows'][show]['Season'] = \
			sonarr_api_query['seasons'][0].pop('seasonNumber')
	return g.movies_dictionary_object[movie]['Shows'][show]['Season']


def set_dictionary_show_root_path(sonarr_api_query, show, g,
                                  movie):
	try:
		g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path'] = \
			parse_root_path_string(sonarr_api_query)
	except KeyError:
		g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path'] = str()
