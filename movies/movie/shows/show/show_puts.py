#!/usr/bin/env python3
from os import (chdir)
from os.path import (abspath,
                     relpath)

from messaging.frontend import (display_show_class_attributes,
                                method_exit,
                                method_launch)
from movies.movie.shows.show.episode.episode_gets import (get_padded_episode_number)


def set_show_root_path(show_object,
                       g):
	method_launch(g)
	from movies.movie.shows.show.show_parser import (get_parsed_show_title,
	                                                 parse_show)
	show_object.absolute_movie_path = abspath(show_object.path)
	show_object.parsed_title = parse_show(show_object,
	                                      g)
	show_object.parsed_title = get_parsed_show_title(show_object,
	                                                 g)
	show_object.absolute_movie_path = abspath(f"{show_object.parsed_title}",)
	show_object.relative_show_path = relpath(f"{show_object.parsed_title}")
	method_exit(g)


def set_show(show_object,
             g):
	from movies.movie.shows.show.show_gets import get_show_root_path
	method_launch(g)
	init_show_object(show_object,
	                 g)
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


def init_show_object(show_object,
                     g):
	method_launch(g)
	show_object.title = show_object.show
	chdir(g.MEDIA_PATH)
	method_exit(g)


def set_episode_padding(show_object,
                        g):
	method_launch(g)
	if show_object.anime_status:
		show_object.episode = "-".join(
			[get_padded_episode_number(e, 3, g) for e in show_object.episode])
		show_object.absolute_episode = "-".join(
			[get_padded_episode_number(e, 3, g) for e in show_object.absolute_episode])
	else:
		show_object.episode = "-".join([get_padded_episode_number(e, 2, g) for e in show_object.episode])
		show_object.absolute_episode = "-".join([get_padded_episode_number(e, 2, g) for e in show_object.absolute_episode])
	method_exit(g)
