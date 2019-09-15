#!/usr/bin/env python3
from os import environ

from messaging.frontend import (method_exit,
                                method_launch)
from methods_to_deprecate.init_value import deprecated_set_season_value, deprecated_set_anime_status
from movies.movie.shows.show.episode.episode_gets import (get_season_folder, get_padded_episode_number)
from movies.movies_puts import (create_directory_if_not_present,
                                set_nested_dictionary_key_value_pair)


def parse_show(show_object,
               g):
	from movies.movie.shows.show.show_puts import init_show_object
	method_launch(g)
	init_show_object(show_object)
	deprecated_set_anime_status(g, show_object)
	deprecated_set_season_value(g, show_object)
	show_object.season_folder = \
		g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Season Folder'] = \
		get_season_folder(show_object,
		                  g)
	show_object.episode = \
		set_nested_dictionary_key_value_pair(
			g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Episode'],
			str())
	show_object.absolute_episode = \
		set_nested_dictionary_key_value_pair(g.movies_dictionary_object[show_object.movie_title]['Shows'][
			                                     show_object.show]['Absolute Episode'],
		                                     str())
	method_launch(g)
	if show_object.anime_status:
		show_object.episode = "-".join(
			[get_padded_episode_number(e, 3, g) for e in show_object.episode])
		show_object.absolute_episode = "-".join(
			[get_padded_episode_number(e, 3, g) for e in show_object.absolute_episode])
	else:
		show_object.episode = "-".join([get_padded_episode_number(e, 2, g) for e in show_object.episode])
		show_object.absolute_episode = "-".join(
			[get_padded_episode_number(e, 2, g) for e in show_object.absolute_episode])
	method_exit(g)
	show_object.parsed_relative_title = \
		set_nested_dictionary_key_value_pair(g.movies_dictionary_object[show_object.movie_title]['Shows'][
			                                     show_object.show]['Parsed Relative Show Title'],
		                                     parse_show_title_from_show_dictionary(show_object,
		                                                                           g))
	
	method_exit(g)
	return show_object.parsed_relative_title


def parse_show_title_from_show_dictionary(show_object,
                                          g):
	method_launch(g)
	create_directory_if_not_present("/".join((show_object.path,
	                                          show_object.season_folder)))
	if not show_object.title:  # adjust to be an api call for sonarr
		show_object.title = \
			g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Title'] = \
			show_object.movie_title
	if show_object.absolute_episode:
		show_object.parsed_title = set_nested_dictionary_key_value_pair(
			g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Show Title'],
			f"{show_object.path}/{show_object.season_folder}/{show_object.show} - S{show_object.season}E{show_object.episode} (E{show_object.absolute_episode}) - {show_object.title}")
	else:
		show_object.parsed_title = set_nested_dictionary_key_value_pair(
			g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Show Title'],
			f"{show_object.path}/{show_object.season_folder}/{show_object.show} - " \
			f"S{show_object.season}E{show_object.episode} - {show_object.title}")
	method_exit(g)
	return show_object.parsed_title


def get_parsed_show_title(show_object):
	return " ".join((show_object.parsed_title,
	                 show_object.quality))


def parse_root_path_string(sonarr_api_query):
	return str(sonarr_api_query['path']).replace(str(environ['SONARR_ROOT_PATH_PREFIX']), '')
