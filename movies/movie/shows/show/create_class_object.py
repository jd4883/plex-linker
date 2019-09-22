#!/usr/bin/env python3
from movies.movie.shows.show.show_gets import *


def init_show_object(movie,
                     series,
                     g):
	from class_objects import Show
	method_launch(g)
	try:
		show = Show(series, movie.movie_title, movie.movie_dictionary, g)
	except AttributeError:
		return
	get_show(show, g)
	# try:
	# 	tv_show_class_object.raw_episodes = g.sonarr.get_episodes_by_series_id(g.movies_dictionary_object[movie.movie_title]['Shows'][tv_show_class_object.movie]['Show ID'])
	# 	tv_show_class_object.raw_episode_files = g.sonarr.get_episode_files_by_series_id(g.movies_dictionary_object[movie.movie_title]['Shows'][tv_show_class_object.movie]['Show ID'])
	# except KeyError as err:
	# 	print(f"Error grabbing raw episode data from sonarr due to {err}")
	method_exit(g)
	return show


