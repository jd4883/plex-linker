#!/usr/bin/env python3

from messaging.frontend import (method_launch,
                                print_movie_file_quality,
                                print_movie_file_found_to_parse,
                                print_movie_extension_found_to_parse,
                                method_exit)


def parse_extension(movie):
	method_launch(movie)
	movie.quality = parse_movie_file_quality(movie.movie_file)
	movie.quality = parse_remux_in_quality(movie.quality)
	movie.quality = parse_proper(movie)
	print_movie_file_found_to_parse(movie)
	print_movie_extension_found_to_parse(movie)
	print_movie_file_quality(movie)
	method_exit(movie)


def parse_remux_in_quality(quality):
	if f"{quality}".lower() == "Remux-1080p.mkv".lower():
		quality = "Bluray-1080p Remux.mkv"  # sonarr compatible format for remux bluray quality
	# consider making a framework with this API from sonarr using the ID to identify, if the quality does not match
	# a sonarr or radarr profile it should reject and throw an except: https://github.com/Sonarr/Sonarr/wiki/Profile
	return quality


def parse_movie_file_quality(movie_file):
	return movie_file.split().pop()


def parse_movie_object(movies_dictionary_object,
                       shows_dictionary_object):
	for movie_dict in movies_dictionary_object["Movies"]:
		new_dict = dict(movie_dict)
		for item in new_dict.items():
			shows_dictionary_object.append(item)


def parse_proper(movie_class_object):
	if movie_class_object.quality.endswith(f"Proper.{movie_class_object.extension}"):
		movie_class_object.quality = f"{movie_class_object.movie_file.split().pop(-2)} {movie_class_object.quality}"
	return movie_class_object.quality
