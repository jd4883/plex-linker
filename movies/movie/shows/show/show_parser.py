#!/usr/bin/env python3
from messaging.frontend import (method_exit,
                                method_launch)
from movies.movie.shows.show.episode.episode_gets import (get_anime_boolean_value_from_movies_dictionary,
                                                          get_season,
                                                          get_season_folder,
                                                          get_show_episode_number_value_from_movies_dictionary,
                                                          get_show_episode_title_value_from_movies_dictionary,
                                                          get_absolute_episode_value_from_movies_dictionary)
from movies.movie.shows.show.show_gets import (get_fully_parsed_show_with_absolute_episode,
                                               get_fully_parsed_show_without_absolute_episode)
from movies.movie.shows.show.show_puts import (init_show_object,
                                               set_episode_padding)
from movies.movies_puts import (create_directory_if_not_present)


def parse_show(show_object,
               g):
	method_launch(g)
	init_show_object(show_object,
	                 g)
	show_object.anime_status = get_anime_boolean_value_from_movies_dictionary(show_object,
	                                                                          g)
	show_object.season = get_season(show_object,
	                                g)
	show_object.season_folder = get_season_folder(show_object,
	                                              g)
	show_object.episode = get_show_episode_number_value_from_movies_dictionary(show_object.movie_dictionary_object,
	                                                                           show_object.show,
	                                                                           g)
	show_object.absolute_episode = get_absolute_episode_value_from_movies_dictionary(show_object,
	                                                                                 g)
	set_episode_padding(show_object,
	                    g)
	show_object.title = get_show_episode_title_value_from_movies_dictionary(show_object.movie_dictionary_object,
	                                                                        show_object.show,
	                                                                        g)
	show_object.parsed_relative_title = parse_show_title_from_show_dictionary(show_object,
	                                                                          g)
	method_exit(g)
	return show_object.parsed_relative_title


def parse_show_title_from_show_dictionary(show_object,
                                          g):
	method_launch(g)
	create_directory_if_not_present("/".join((show_object.path,
	                                          show_object.season_folder)),
	                                g)
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
	method_launch(g)
	method_exit(g)
	return " ".join((show_object.parsed_title,
	                 show_object.quality))
