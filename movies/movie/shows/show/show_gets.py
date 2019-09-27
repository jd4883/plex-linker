#!/usr/bin/env python3

from messaging.frontend import (
	method_exit,
	method_launch,
	)
from movies.movie.shows.show.show_puts import (set_show)
from movies.movie.shows.show.show_validation import (validate_show_path_presence)


def get_show_root_path(show_object,
                       g):
	if validate_show_path_presence(show_object,
	                               g):
		return True
	return False


def get_show(show_object,
             g):
	method_launch(g)
	show_object.show_paths = g.SHOWS_PATH
	set_show(show_object,
	         g)
	method_exit(g)
	return show_object


def get_alphabetical_specials_string():
	return f"Season {str(0).zfill(2)}"  # create sonarr API call here to movies_gets the name dynamically


def get_anime_status_from_api(show_lookup):
	if show_lookup['seriesType'] == 'anime':
		status = True
	else:
		status = False
	return status


def get_show_id(show,
                g):
	for item in g.shows_dictionary:
		if item['title'] == show:
			return int(item['id'])
	return str()


def get_tag_id(show,
               g,
               movie,
               tag):
	api_results = g.sonarr.get_all_tag_ids()['id']
	if not g.movies_dictionary_object[movie]['Shows'][show]['Show Tags']:
		g.movies_dictionary_object[movie]['Shows'][show]['Show Tags'] = list()
	if tag not in g.movies_dictionary_object[movie]['Shows'][show]['Show Tags'] and api_results[tag]:
		g.movies_dictionary_object[movie]['Shows'][show]['Show Tags'].append(api_results[tag])
	return api_results[tag]
