#!/usr/bin/env python3

from messaging.frontend import (method_launch,
                                print_movie_file_quality,
                                print_movie_file_found_to_parse,
                                print_movie_extension_found_to_parse,
                                method_exit)


def parse_extension(movie,
                    g):
	method_launch(g)
	movie.quality = parse_movie_file_quality(movie.movie_file)
	movie.quality = parse_remux_in_quality(movie.quality,
	                                       g)
	movie.quality = parse_proper(movie,
	                             g)
	print_movie_file_found_to_parse(movie,
	                                g)
	print_movie_extension_found_to_parse(movie,
	                                     g)
	print_movie_file_quality(movie,
	                         g)
	method_exit(g)


def parse_remux_in_quality(quality,
                           g):
	method_launch(g)
	if str(quality).lower() == "Remux-1080p.mkv".lower():
		quality = "Bluray-1080p Remux.mkv"  # sonarr compatible format for remux bluray quality
	# consider making a framework with this API from sonarr using the ID to identify, if the quality does not match
	# a sonarr or radarr profile it should reject and throw an except: https://github.com/Sonarr/Sonarr/wiki/Profile
	method_exit(g)
	return quality


def parse_movie_file_quality(movie_file):
	return movie_file.split().pop()

def parse_proper(movie_class_object,
                 g):
	method_launch(g)
	if movie_class_object.quality.endswith(f"Proper.{movie_class_object.extension}"):
		movie_class_object.quality = f"{movie_class_object.movie_file.split().pop(-2)} {movie_class_object.quality}"
	method_exit(g)
	return movie_class_object.quality
