#!/usr/bin/env python3
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from movies.movie.movie_gets import (get_relative_movie_path,
                                     get_movie_path)
from movies.movie.shows.show.show_parser import (parse_new_show_class_object)
from movies.movie.shows.show.show_validation import (validate_ready_to_link_movie_to_show)


def parse_shows_to_link(shows):
	for _ in shows.shows:
		if validate_ready_to_link_movie_to_show(shows.quality):
			for item in shows.shows:
				symlink_force(item)
				shows.movies_dictionary_object[shows.movie_title]['Link Target'] = f"{shows.absolute_movie_file_path}"
				shows.movies_dictionary_object[shows.movie_title]['Shows'][shows.show][
					'Link Destination'] = f"{shows.relative_show_path}"
				shows.absolute_movie_path = shows.movies_dictionary_object[title]['Absolute Movie Path'] = get_movie_path(
					movie)
				shows.relative_movie_path = shows.movies_dictionary_object[title][
					'Relative Movie Path'] = get_relative_movie_path(movie)
				# f"{show_class_object.absolute_movie_file_path}",
				# f"{show_class_object.relative_show_path}"],
				# set_symlink_status_attributes_for_dictionary(item)
				set_link_target(shows)
				# print(shows.movies_dictionary_object[shows.movie_title])
				# print used for validating inheritence is working for the dictionary ammendments
				set_permissions(item)
		# this area needs some help with the dictionary component


def set_link_target(self):
	self.movies_dictionary_object[self.movie_title].update({'Symlink Target': f"{self.absolute_movie_file_path}"})


def parse_shows_dictionary_object(movie_class_object,
                                  movie_dictionary):
	for show in movie_dictionary['Shows'].keys():
		parse_new_show_class_object(movie_class_object,
		                            show,
		                            movie_dictionary['Shows'][show])
