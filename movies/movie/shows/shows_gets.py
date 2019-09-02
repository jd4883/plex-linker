#!/usr/bin/env python3
def get_shows_dictionary_from_parent_dictionary(show_class_object,
                                                g):
	try:
		if not g.movies_dictionary_object[show_class_object.movie_title]['Shows']:
			g.movies_dictionary_object[show_class_object.movie_title]['Shows'] = [{}]
	except KeyError:
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'] = [{}]
	finally:
		return g.movies_dictionary_object[show_class_object.movie_title]['Shows']
