#!/usr/bin/env python3
import os

from movies.movie.movie_gets import get_movie_path


def parse_relpath(self, g, media_path):
	film = get_movie_path(self, g)
	if os.path.exists(film):
		return str(os.path.relpath(film, media_path))
	return str()


def parse_movie_title(radarr_dictionary, movie):
	movie_title = movie.replace(":", "-")
	try:
		base = str(radarr_dictionary[0].pop('title', str(movie)))
		year = str(radarr_dictionary[0].pop('year', str())).replace(":", "-")
		movie_title = f"{base} ({year})".replace(" ()", str()).replace(":", "-")
	except IndexError:
		pass
	except KeyError:
		pass
	return str(movie_title)
