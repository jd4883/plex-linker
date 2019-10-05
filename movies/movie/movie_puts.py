import movies.movie.movie_parser as parser
import movies.movie.movie_gets as get
from messaging.frontend import (method_launch, method_exit)


def absolute_movie_directory(self):
	# self.movie_dictionary['Absolute Movie Path'] =
	try:
		self.movie_dictionary.update({ 'Absolute Movie Path': self.absolute_movie_path })
	except KeyError:
		self.movie_dictionary['Absolute Movie Path'] = str()


def set_movie_file_and_extension(file, file_extension, movie, g):
	method_launch(g)
	movie.movie_file = file
	movie.extension = file_extension
	parser.extension_from_movie_file(movie, g)
	method_exit(g)


def set_movie_quality(movie, g):
	method_launch(g)
	try:
		movie.movie_file = g.movies_dictionary_object[movie.movie_title]['Parsed Movie File'] = get.movie_file(movie)
	except KeyError:
		return
	movie.extension = g.movies_dictionary_object[movie.movie_title]['Parsed Movie Extension'] = get.movie_extension(
		movie.extension)
	movie.quality = g.movies_dictionary_object[movie.movie_title]['Parsed Movie Quality'] = get.movie_quality(
		movie.quality)
	method_exit(g)


def relative_movie_directory(self, g):
	return g.movies_dictionary_object[self.movie_title]['Relative Movie Path']
