#!/usr/bin/env python3
def set_shows_dictionary_object(movie):
	try:
		movie.shows_dictionary_object = movie.movies_dictionary_object[movie.movie_title].get('Shows')
	except AttributeError:
		movie.shows_dictionary_object = None
	return movie.shows_dictionary_object
