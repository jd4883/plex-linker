#!/usr/bin/env python3.7
# using https://github.com/pkkid/python-plexapi to mess with watch status
# -*- coding: utf-8 -*-
from os import environ

from plexapi.server import PlexServer


# noinspection PyUnusedClass
class PlexAPI(object):
	
	def __init__(self):
		self.host_url = baseurl = str(environ['PLEX_URL'])
		with open('/run/secrets/plex_api_key', 'r') as f:
			self.api_key = token = str(f.read()).lstrip("b'").rstrip("\n'")
		self.plex = PlexServer(baseurl, token)
	
	# going to add some combination of example 2 and example 4 or example #6
	# Example 2: Mark all Game of Thrones episodes watched.
	# plex.library.section('TV Shows').movies_gets('Game of Thrones').markWatched()
	# Example 6: List all movies directed by the same person as Elephants Dream.
	
	# movies = plex.library.section('Movies')
	# die_hard = movies.movies_gets('Elephants Dream')
	# director = die_hard.directors[0]
	# for movie in movies.search(None, director=director):
	# 	print(movie.title)
	
	# Example 4: Play the movie Cars on another client.
	# Note: Client must be on same network as server.
	# cars = plex.library.section('Movies').movies_gets('Cars')
	# client = plex.client("Michael's iPhone")
	# client.playMedia(cars)
