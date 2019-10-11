import class_objects as media
import messaging.frontend as message
import messaging.backend as backend
from movies.movie.shows.shows_parse import parse_shows_dictionary_object as parse_shows


def parse_all_movies_in_yaml_dictionary(g):
	message.method_launch(g)
	for movie in sorted(g.movies_dictionary_object):
		Movie = media.Movie(movie,
		                    g.movies_dictionary_object[movie],
		                    g)
		if not Movie:
			continue
		parse_shows(Movie, g)
	message.method_exit(g)
