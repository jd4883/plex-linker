#!/usr/bin/env python3
from messaging.frontend import (method_exit,
                                method_launch)
from movies.movie.shows.show.episode.episode_gets import (get_season,
                                                          get_season_folder)
from movies.movie.shows.show.show_gets import (get_fully_parsed_show_with_absolute_episode,
                                               get_fully_parsed_show_without_absolute_episode)
from movies.movie.shows.show.show_puts import (init_show_object,
                                               set_episode_padding)
from movies.movies_puts import (create_directory_if_not_present,
                                set_nested_dictionary_key_value_pair)


def parse_show(show_object,
               g):
	method_launch(g)
	init_show_object(show_object,
	                 g)
	show_object.anime_status = set_nested_dictionary_key_value_pair(g,
	                                                                g.movies_dictionary_object[show_object.movie_title][
		                                                                'Shows'][show_object.show]['Anime'],
	                                                                False)
	show_object.season = \
		get_season(show_object,
		           g)
	
	show_object.season_folder = \
		g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Parsed Season Folder'] = \
		get_season_folder(show_object,
		                  g)
	show_object.episode = set_nested_dictionary_key_value_pair(g,
	                                                           g.movies_dictionary_object[show_object.movie_title][
		                                                           'Shows'][show_object.show]['Episode'],
	                                                           str())
	show_object.absolute_episode = \
		set_nested_dictionary_key_value_pair(g,
		                                     g.movies_dictionary_object[show_object.movie_title]['Shows'][
			                                     show_object.show]['Absolute Episode'],
		                                     str())
	set_episode_padding(show_object,
	                    g)
	show_object.parsed_relative_title = \
		set_nested_dictionary_key_value_pair(g,
		                                     g.movies_dictionary_object[show_object.movie_title]['Shows'][
			                                     show_object.show][
			                                     'Parsed Relative Show Title'],
		                                     parse_show_title_from_show_dictionary(show_object,
		                                                                           g))
	
	method_exit(g)
	return show_object.parsed_relative_title


def parse_show_title_from_show_dictionary(show_object,
                                          g):
	method_launch(g)
	create_directory_if_not_present("/".join((show_object.path,
	                                          show_object.season_folder)),
	                                g)
	if not show_object.title: # adjust to be an api call for sonarr
		show_object.title = \
			g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Title'] = \
			show_object.movie_title
	if show_object.absolute_episode:
		show_object.parsed_title = get_fully_parsed_show_with_absolute_episode(show_object,
		                                                                       g)
	else:
		show_object.parsed_title = get_fully_parsed_show_without_absolute_episode(show_object,
		                                                                          g)
	method_exit(g)
	return show_object.parsed_title


def get_parsed_show_title(show_object,
                          g):
	return " ".join((show_object.parsed_title,
	                 show_object.quality))
