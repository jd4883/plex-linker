#!/usr/bin/env python3
import os
from os import chdir, environ

from messaging import frontend as message


def parsed_collection():
	chdir(environ['PLEX_LINKER'])
	return "config_files/media_collection_parsed_last_run.yaml"


def get_media_collection_parsed_archives():
	chdir(environ['PLEX_LINKER'])
	return str(environ['CONFIG_ARCHIVES'])


def get_docker_media_path(g):
	return "/".join((str(os.environ['DOCKER_MEDIA_PATH']), g.MOVIES_PATH[0]))


def get_movie_path(movie, g):
	message.method_launch(g)
	absolute_movie_path = movie.absolute_movie_path
	for path in os.listdir(movie.absolute_movies_path):
		movie_string = '/'.join((movie.absolute_movies_path, path, movie.movieTitle))
		if os.path.exists(movie_string):
			absolute_movie_path = movie_string
			message.method_exit(g)
			break
	message.method_exit(g)
	return str(absolute_movie_path)
