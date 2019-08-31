#!/usr/bin/env python3
from messaging.frontend import (method_launch,
                                method_exit)


def set_shows_dictionary_object(movie,
                                g):
	method_launch(g)
	try:
		movie.shows_dictionary_object = g.movies_dictionary_object[movie.movie_title].get('Shows')
	except AttributeError:
		movie.shows_dictionary_object = None
	method_exit(g)
	return movie.shows_dictionary_object
