#!/usr/bin/env python3
from class_objects import Show
from movies.movie.shows.show.show_gets import *
from movies.movie.shows.show.show_puts import (init_show_object)


def create_tv_show_class_object(movie_class_object,
                                show,
                                g):
	method_launch(g)
	tv_show_class_object = Show(show,
	                            movie_class_object.movie_title,
	                            g)
	tv_show_class_object.show = show
	get_show(tv_show_class_object,
	         g)
	print_shows_dictionary(movie_class_object,
	                       g)
	method_exit(g)
	return tv_show_class_object
