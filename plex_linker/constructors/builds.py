#!/usr/bin/env python3
def build_movie_name_from_lookup(radarr_dictionary, movie_title):
	return str(radarr_dictionary[0].pop('title', str(movie_title))) + \
	       f"({str(radarr_dictionary[0].pop('year', str()))})".replace(" ()", str())


def init_show_object(movie, series, g):
	from class_objects import Show
	if not isinstance(movie.shows_dictionary[series], dict):
		return
	show = Show(g,
	            series,
	            str(movie.movie_title),
	            movie.shows_dictionary[series],
	            movie.movie_dictionary)
	return show
