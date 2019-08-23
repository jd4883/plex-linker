#!/usr/bin/env python3
from jobs.set_path_permissions import set_permissions
from movies.movie.shows.show.show_parser import parse_new_show_class_object


def parse_shows_to_link(shows):
	for _ in shows.shows:
		from movies.movie.shows.show.show_validation import validate_ready_to_link_movie_to_show
		if validate_ready_to_link_movie_to_show(shows.quality):
			for item in shows.shows:
				from jobs.symlinking import symlink_force
				symlink_force(item)
				set_permissions(item)


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
