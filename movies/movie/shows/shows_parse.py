import json.decoder

import messaging.backend as backend
import messaging.frontend as message
import methods
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)


def parse_show_to_link(show, g):
	try:
		message.method_launch(g)
		map(symlink_force(show, g), show.shows_dictionary.items())
		map(set_permissions(show, g), show.shows_dictionary.items())
		# for _ in show.shows_dictionary.items():
		# 	symlink_force(show, g), show.shows_dictionary.items()
		# 	set_permissions(show, g)
		message.method_exit(g)
	except AttributeError:
		pass


def parse_shows_dictionary_object(movie, g):
	message.method_launch(g)
	if not movie.shows_dictionary:
		return
	for series in movie.shows_dictionary.keys():
		if not isinstance(movie.shows_dictionary[series], dict):
			continue
		try:
			show = methods.Show(g,
			                    series,
			                    movie.shows_dictionary[series],
			                    movie.movie_dictionary)
			g.sonarr.lookup_series(show)
			show.initShow(g)
		except json.decoder.JSONDecodeError:
			continue
		parse_show_to_link(show, g)
		try:
			code = 640 if show.has_link or not show.episode else 641
			g.LOG.info(backend.debug_message(code, g, movie.movie_title, show.title))
		except AttributeError:
			code = 641
		if code == 641:
			parse_show_to_link(show, g)
