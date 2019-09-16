#!/usr/bin/env python3.7
from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Globals, \
	Movies
from movies.movies_parser import parse_all_movies_in_yaml_dictionary


if __name__ == "__main__":
	g = Globals()
	full_movie_database = Movies(g)
	parse_all_movies_in_yaml_dictionary(g)
	print(sorted(g.sonarr_genres))
	# for genre in sorted(g.sonarr_genres):
	# 	output = g.sonarr.set_new_tag_for_sonarr({"label": genre})
	# 	print(output)
		# try:
		# 	g.sonarr.set_new_tag_for_sonarr(genre)
		# except:
		# 	print(f'failed to add {genre} to sonarr')
	# add method to add these to the library
	write_python_dictionary_object_to_yaml_file(g)
