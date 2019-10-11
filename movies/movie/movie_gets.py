import os
import messaging.frontend as message


def get_absolute_movie_file_path(movie):
	if movie.absolute_movie_path:
		return "/".join((movie.absolute_movie_path, movie.movie_file))
	return str()

def get_relative_movie_file_path(movie):
	relpath = "/".join((movie.relative_movie_path, movie.movie_file))
	if movie.movie_file and os.path.exists(relpath):
		return relpath
	else:
		return str()

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
