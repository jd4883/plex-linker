#!/usr/bin/env python3
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from messaging.frontend import (method_launch,
                                method_exit)
from movies.movie.movie_gets import (get_relative_movie_path,
                                     get_movie_path)
from movies.movie.shows.show.create_class_object import create_tv_show_class_object
from movies.movie.shows.show.show_validation import (validate_ready_to_link_movie_to_show)


def parse_show_to_link(show,
                       g):
	method_launch(g)
	for _ in g.movies_dictionary_object[show.movie_title]['Shows'].items():
		if validate_ready_to_link_movie_to_show(show.quality,
		                                        g):
			symlink_force(show,
			              g)
			g.movies_dictionary_object[show.movie_title]['Symlink Target'] = \
				str(show.absolute_movie_file_path)
			
			g.movies_dictionary_object[show.movie_title]['Shows'][show.show]['Symlink Destination'] = \
				str(show.relative_show_path)
			
			show.absolute_movie_path = g.movies_dictionary_object[show.movie_title]['Absolute Movie Path'] = \
				str(get_movie_path(show,
				                   g))
			show.relative_movie_path = g.movies_dictionary_object[show.movie_title]['Relative Movie Path'] = \
				str(get_relative_movie_path(show,
				                            g))
			set_link_target(show,
			                g)
			set_permissions(show,
			                g)
	method_exit(g)


def set_link_target(self,
                    g):
	g.movies_dictionary_object[self.movie_title].update({'Symlink Target': f"{self.absolute_movie_file_path}"})


def parse_shows_dictionary_object(movie_class_object,
                                  g):
	method_launch(g)
	for show in g.movies_dictionary_object[movie_class_object.movie_title]['Shows'].keys():
		tv_show = create_tv_show_class_object(movie_class_object,
		                                      show,
		                                      g)
		tv_show.show = show
		# show object not getting created correctly here
		parse_show_to_link(tv_show,
		                   g)
	method_exit(g)
