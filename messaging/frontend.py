#!/usr/bin/env python3.7
import os
import logs.bin.get_parameters as parameters

from messaging.backend import debug_message


# TODO: standardize all frontend / backend calls
#
# def print_movie_file_quality(movie, g):
# 	g.LOG.info(debug_message(612, g, movie.quality))


def message_exiting_function(g):
	os.chdir(g.MEDIA_DIRECTORY)
	g.LOG.info(debug_message(601, g))

#
# def print_movie_extension_found_to_parse(movie, g):
# 	g.LOG.info(debug_message(608, g, movie.extension))

#
# def print_movie_file_found_to_parse(movie, g):
# 	g.LOG.info(debug_message(610, g, movie.movie_file))


def method_launch(g):
	os.chdir(str(os.environ['DOCKER_MEDIA_PATH']))
	g.parent_method = parameters.get_parent_method_string()
	g.method = parameters.get_child_method_string()


def method_exit(g):
	os.chdir(g.MEDIA_DIRECTORY)
	message_exiting_function(g)
