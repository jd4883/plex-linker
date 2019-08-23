#!/usr/bin/env python3
from movies.movie.shows.show.show_gets import *


def create_tv_show_class_object(movie_object,
                                show):
	from class_objects import Show
	method_launch(movie_object)
	tv_show_class_object = Show(show,
	                            movie_object.movie_title)
	tv_show_class_object.show = show
	get_show(tv_show_class_object)
	print_shows_dictionary(movie_object)
	method_exit(movie_object)
	return tv_show_class_object
