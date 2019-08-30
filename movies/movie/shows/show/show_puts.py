#!/usr/bin/env python3
from os import (chdir)
from os.path import (abspath,
                     relpath)

from messaging.frontend import (display_show_class_attributes,
                                method_exit,
                                method_launch)
from movies.movie.shows.show.episode.episode_gets import (get_padded_episode_number,
                                                          get_anime_boolean_value_from_movies_dictionary)


def set_show_root_path(show_object):
	method_launch(show_object)
	from movies.movie.shows.show.show_parser import (get_parsed_show_title,
	                                                 parse_show)
	show_object.absolute_movie_path = abspath(show_object.path)
	show_object.parsed_title = parse_show(show_object)
	show_object.parsed_title = get_parsed_show_title(show_object)
	show_object.absolute_movie_path = abspath(f"{show_object.parsed_title}")
	show_object.relative_show_path = relpath(f"{show_object.parsed_title}")
	method_exit(show_object)


def set_show(show_object):
	method_launch(show_object)
	init_show_object(show_object)
	display_show_class_attributes(show_object)
	from movies.movie.shows.show.show_gets import get_show_root_path
	try:
		if get_show_root_path(show_object):  # parent_movie_dictionary_object may be worth adding as an arg here
			set_show_root_path(show_object)
	except TypeError:
		pass
	method_exit(show_object)


def init_show_object(show_object):  # parent_movie_dictionary_object may be worth adding as an arg here
	method_launch(show_object)
	show_object.movies_dictionary_object = {f"{show_object.show}": []}
	show_object.title = show_object.show
	chdir(show_object.MEDIA_PATH)


def set_episode_padding(show_object):
	if show_object.anime_status:
		show_object.episode = "-".join(
			[get_padded_episode_number(e, 3) for e in show_object.episode])
		show_object.absolute_episode = "-".join(
			[get_padded_episode_number(e, 3) for e in show_object.absolute_episode])
	else:
		show_object.episode = "-".join([get_padded_episode_number(e, 2) for e in show_object.episode])
		show_object.absolute_episode = "-".join([get_padded_episode_number(e, 2) for e in show_object.absolute_episode])
