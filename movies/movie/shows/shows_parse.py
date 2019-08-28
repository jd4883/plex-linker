#!/usr/bin/env python3
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)

from movies.movie.shows.show.show_parser import (parse_new_show_class_object)
from movies.movie.shows.show.show_validation import (validate_ready_to_link_movie_to_show)


def parse_shows_to_link(shows):
	for _ in shows.shows:
		if validate_ready_to_link_movie_to_show(shows.quality):
			for item in shows.shows:
				symlink_force(item)
				shows.movies_dictionary_object[shows.movie_title]['Link Target'] = f"{item.absolute_movie_file_path}"
				shows.movies_dictionary_object[shows.movie_title]['Shows'][shows.show]['Link Destination'] = f"{shows.relative_show_path}"
				#f"{show_class_object.absolute_movie_file_path}",
				#f"{show_class_object.relative_show_path}"],
				#set_symlink_status_attributes_for_dictionary(item)
				set_link_target(shows)
				#print(shows.movies_dictionary_object[shows.movie_title])
				# print used for validating inheritence is working for the dictionary ammendments
				set_permissions(item)
			# this area needs some help with the dictionary component


def set_link_target(self):
	self.movies_dictionary_object[self.movie_title].update({'Symlink Target': f"{self.absolute_movie_file_path}"})
	# this seems to not work need to figure out how to update the master dictionary in a better way
	#print(self.movies_dictionary_object[self.movie_title])
	# self.movies_dictionary_object[self.movie_title].update({'Shows': {self.show: {'Symlink Destination': f"{self.relative_show_path}"}}})
	# print(self.movies_dictionary_object[self.movie_title])
	# exit(-1)
	# self.movies_dictionary_object[self.movie_title]['Shows'].update({'Symlink Status': True})
	

def parse_shows_dictionary_object(shows_class_object):
	try:
		for show in shows_class_object.shows_dictionary_object:  # get_shows_object(shows_class_object)
			try:
				parse_new_show_class_object(shows_class_object,
				                            show)
			except TypeError:
				continue
	except TypeError:
		pass
	return shows_class_object.shows
