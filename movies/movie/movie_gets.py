#!/usr/bin/env python3
from os import (listdir, environ)
from os.path import (
	relpath,
	abspath,
	exists,
	)
from string_manipulation.string_methods import getCaseInsensitivePath
from messaging.frontend import (
	method_launch,
	method_exit,
	)
from movies.movie.movie_puts import (
	set_absolute_movie_path,
	set_relative_movie_path,
	)


def get_relative_movie_path(movie,
                            g):
	method_launch(g)
	try:
		movie.relative_movie_path = relpath(movie.absolute_movie_path,
		                                    str(environ['DOCKER_MEDIA_PATH']))
	except ValueError:
		pass
	finally:
		if movie.relative_movie_path:
			set_absolute_movie_path(movie,
			                        g)
			set_relative_movie_path(movie,
			                        g)
			method_exit(g)
			return str(movie.relative_movie_path)
		method_exit(g)
		return str()


def get_absolute_movie_file_path(movie):
	return str("/".join((str(movie.absolute_movie_path).replace('/video/video/', '/video/'),
	                     str(movie.movie_file))))


# noinspection PyUnusedLocal
def get_relative_movie_file_path(movie,
                                 g):
	try:
		movie.absolute_movie_path =\
			abspath(str(movie.relative_movie_path))
		return str(relpath(movie.absolute_movie_path, str(environ['DOCKER_MEDIA_PATH'])))
	except AttributeError:
		pass
	except IndexError:
		pass
	except FileNotFoundError:
		pass
	return str()


def get_movie_quality(quality):
	return str(quality)


# in theory this checks case combinations and titles correct, however, I am not seeing the desired results
def get_movie_path(movie,
                   g):
	method_launch(g)
	for path in listdir(movie.absolute_movies_path):
		movie.absolute_movie_path = '/'.join((movie.absolute_movies_path,
		                                      path,
		                                      movie.movie_title))
		# for item in g.radarr.get_movie_library():
		# 	print(f"ITEM TITLE {item['title']}")
		# 	if (str(item['title']).lower() ==
		# 	    movie.movie_title.lower()) or \
		# 			(str(item['title']).lower() ==
		# 			 ' '.join(str(movie.movie_title).split(' ')[:-1]).lower()) \
		# 			or ' '.join(str(item['title']).split(' ')[:-1]).lower() == \
		# 		' '.join(str(movie.movie_title).split(' ')[:-1]).lower():
		# 		print('we have a match')
		# 		print(f"PARSED TITLE: {item['title']} ({item['year']})")
		# 		break
		# 		# idea here is to replace the base title with whatever is in radarr and not care about the year initally input
		# movie.movie_title = f"{k} ({k['year']})"
		
		movie_string = getCaseInsensitivePath(movie.absolute_movie_path)
		if exists(movie_string):
			movie.absolute_movie_path = movie_string
			method_exit(g)
			return str(movie.absolute_movie_path)
	method_exit(g)
	return str()


def get_movie_file(movie):
	return movie.movie_file


def get_movie_extension(extension):
	return extension
