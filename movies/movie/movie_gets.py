import os

import messaging.backend as backend
import messaging.frontend as message


def get_absolute_movie_file_path(movie, g):
	abspath = "/".join((movie.absolute_movie_path, movie.movie_file))
	g.LOG.debug(backend.debug_message(615, g, abspath))
	return abspath


def get_relative_movie_file_path(movie, g):
	relpath = "/".join((movie.relative_movie_path, movie.movie_file))
	g.LOG.debug(backend.debug_message(616, g, relpath))
	return relpath


# in theory this checks case combinations and titles correct, however, I am not seeing the desired results
def get_movie_path(movie, g):
	message.method_launch(g)
	absolute_movie_path = movie.absolute_movie_path
	for path in os.listdir(movie.absolute_movies_path):
		movie_string = '/'.join((movie.absolute_movies_path, path, movie.movie_title))
		if os.path.exists(movie_string):
			absolute_movie_path = movie_string
			message.method_exit(g)
			break
	message.method_exit(g)
	return str(absolute_movie_path)
