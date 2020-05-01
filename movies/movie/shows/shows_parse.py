import messaging.frontend as message
import methods
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)


def parse_show_to_link(show, g):
	message.method_launch(g)
	map(symlink_force(show, g), show.shows_dictionary.items())
	map(set_permissions(show, g), show.shows_dictionary.items())
	message.method_exit(g)


def parse_shows_dictionary_object(movie, g):
	message.method_launch(g)
	if not movie.shows_dictionary:
		return
	for series in movie.shows_dictionary.keys():
		if not isinstance(movie.shows_dictionary[series], dict):
			continue
		show = methods.Show(g,
		                    series,
		                    movie.shows_dictionary[series],
		                    movie.movie_dictionary)
		g.sonarr.lookup_series(show)
		show.initShow(g)
		parse_show_to_link(show, g)
