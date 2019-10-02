#!/usr/bin/env python3
from movies.movie.shows.show.show_puts import set_dictionary_show_root_path


def set_show_root_path(api_query, show, g, movie):
	set_dictionary_show_root_path(api_query, show, g, movie)
	return g.movies_dictionary_object[movie]['Shows'][show]['Show Root Path']
