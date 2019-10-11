#!/usr/bin/env python3
def build_movie_name_from_lookup(radarr_dictionary, movie_title):
	return str(radarr_dictionary[0].pop('title', str(movie_title))) + \
	       f"({str(radarr_dictionary[0].pop('year', str(0)))})".replace(" ()", str())
