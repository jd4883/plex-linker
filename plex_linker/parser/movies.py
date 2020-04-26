#!/usr/bin/env python3
import methods as media
from messaging import frontend as message
from movies.movie.shows.shows_parse import parse_shows_dictionary_object as parse_shows


def parse_all_movies_in_yaml_dictionary(g):
	message.method_launch(g)
	for movie in sorted(g.movies_dict):
		Movie = media.Movie(g.movies_dict[movie],
		                    g)
		if not Movie:
			continue
		parse_shows(Movie, g)
	message.method_exit(g)
