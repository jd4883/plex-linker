import messaging.frontend as message
import messaging.backend as backend
import movies.movie.shows.show.validate as validate
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from movies.movie.shows.show.init import init_show_object
from movies.movie.shows.shows_validation import linking_can_be_skipped


def parse_show_to_link(show, g):
	message.method_launch(g)
	for _ in show.shows_dictionary.items():
		#if validate.link_ready(show.quality):
		symlink_force(show, g)
		set_permissions(show, g)
	message.method_exit(g)


def parse_shows_dictionary_object(movie, g):
	message.method_launch(g)
	if not movie.shows_dictionary:
		return
	for series in movie.shows_dictionary.keys():
		if series not in movie.shows_dictionary:
			g.LOG.warn(backend.debug_message(638, g, movie.movie_title))
			continue
		if not isinstance(movie.shows_dictionary[series], dict):
			# no shows to associate with the movie
			g.LOG.warn(backend.debug_message(639, g, movie.movie_title))
			break
		show = init_show_object(movie, str(series), g)
		if show.has_link:
		#if linking_can_be_skipped(show, movie):
			# not sure why but something is up with this method and it is not doing its job
			g.LOG.info(backend.debug_message(640, g, movie.movie_title))
			continue
		g.LOG.info(backend.debug_message(641, g, movie.movie_title, show.show))
		parse_show_to_link(show, g)
