import movies.movie.movie_parser as parser
from messaging.frontend import (method_launch, method_exit)


def set_movie_file_and_extension(file, file_extension, movie, g):
	method_launch(g)
	movie.movie_file = file
	print(movie.movie_file)
	movie.extension = file_extension
	parser.extension_from_movie_file(movie, g)
	method_exit(g)
