#!/usr/bin/env python3
from messaging.frontend import (print_ready_to_link_absolute_movie_path_to_relative_show_path,
                                method_exit,
                                method_launch)
from movies.movie.shows.show.create_class_object import (create_tv_show_class_object)
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


def parse_show(show_object):
	method_launch(show_object)
	init_show_object(show_object)
	show_object.anime_status = get_anime_boolean_value_from_movies_dictionary(show_object)
	show_object.season = get_season(show_object)
	show_object.season_folder = get_season_folder(show_object)
	show_object.episode = get_show_episode_number_value_from_movies_dictionary(show_object.movie_dictionary_object,
	                                                                           show_object.show)
	show_object.absolute_episode = get_absolute_episode_value_from_movies_dictionary(show_object)
	set_episode_padding(show_object)
	show_object.title = get_show_episode_title_value_from_movies_dictionary(show_object.movie_dictionary_object,
	                                                                        show_object.show)
	show_object.parsed_relative_title = parse_show_title_from_show_dictionary(show_object)
	print_ready_to_link_absolute_movie_path_to_relative_show_path(show_object)
	method_exit(show_object)
	return show_object.parsed_relative_title


def parse_new_show_class_object(shows_object,
                                show):
	from movies.movie.shows.shows_parse import parse_shows_to_link
	method_launch(shows_object)
	try:
		shows_object.shows.append(create_tv_show_class_object(shows_object,
		                                                      show))
		shows_object.show = show
		# suspect here is where the inheritence problem begins
		parse_shows_to_link(shows_object)
		#shows_object.movies_dictionary_object.update(show.movies_dictionary_object)
	except AttributeError:
		pass  # this may make sense to update with messaging, it should be a normal condition to see when importing movies


def parse_show_title_from_show_dictionary(show_object):
	method_launch(show_object)
	create_directory_if_not_present("/".join((show_object.path,
	                                          show_object.season_folder)))
	if show_object.absolute_episode:
		show_object.parsed_title = get_fully_parsed_show_with_absolute_episode(show_object)
	else:
		show_object.parsed_title = get_fully_parsed_show_without_absolute_episode(show_object)
	return show_object.parsed_title


def get_parsed_show_title(show_object):
	return " ".join((show_object.parsed_title,
	                 show_object.quality))
