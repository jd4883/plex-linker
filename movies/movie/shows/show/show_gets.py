#!/usr/bin/env python3

from messaging.frontend import (
	method_exit,
	method_launch,
	print_method_shows_dictionary_value,
)
from movies.movie.shows.show.show_puts import set_show
from movies.movie.shows.show.show_validation import (validate_show_path_presence)
from movies.movies_puts import set_nested_dictionary_key_value_pair


def get_show_root_path(show_object,
                       g):
	method_launch(g)
	method_exit(g)
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
	print_method_shows_dictionary_value(show_object,
	                                    g)
	method_exit(g)
	return show_object


def get_fully_parsed_show_with_absolute_episode(show_object,
                                                g):
	return set_nested_dictionary_key_value_pair(g.movies_dictionary_object[show_object.movie_title]['Shows'][
		                                            show_object.show]['Parsed Show Title'],
	                                            f"{show_object.path}/{show_object.season_folder}/{show_object.show} - S{show_object.season}E{show_object.episode} (E{show_object.absolute_episode}) - {show_object.title}")


def get_fully_parsed_show_without_absolute_episode(self,
                                                   g):
	return set_nested_dictionary_key_value_pair(g.movies_dictionary_object[self.movie_title]['Shows'][
		                                            self.show]['Parsed Show Title'],
	                                            f"{self.path}/{self.season_folder}/{self.show} - " \
	                                            f"S{self.season}E{self.episode} - {self.title}")

def get_alphabetical_specials_string():
	return f"Season {str(0).zfill(2)}"  # create sonarr API call here to get the name dynamically


def get_anime_status_from_api(show_lookup):
	if show_lookup['seriesType'] == 'anime':
		status = True
	else:
		status = False
	return status


def get_show_id(show, g,
                movie):
	for item in g.shows_dictionary:
		if item['title'] == show:
			g.movies_dictionary_object[movie]['Shows'][show]['Show ID'] = int(item['id'])
			return g.movies_dictionary_object[movie]['Shows'][show]['Show ID']
