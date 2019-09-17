#!/usr/bin/env python3
from class_objects import sonarr_api_set_tag
from movies.movie.shows.show.show_gets import *


def create_tv_show_class_object(self,
                                show,
                                g):
	from class_objects import Show
	method_launch(g)
	tv_show_class_object = Show(show,
	                            self.movie_title,
	                            g)
	tv_show_class_object.show = show
	get_show(tv_show_class_object,
	         g)
	tv_show_class_object.raw_episodes = g.sonarr.get_episodes_by_series_id(g.movies_dictionary_object[self.movie_title]['Shows'][tv_show_class_object.show]['Show ID'])
	tv_show_class_object.raw_episode_files = g.sonarr.get_episode_files_by_series_id(g.movies_dictionary_object[self.movie_title]['Shows'][tv_show_class_object.show]['Show ID'])
	sonarr_api_set_tag(g)
	method_exit(g)
	return tv_show_class_object


