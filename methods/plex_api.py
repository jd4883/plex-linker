#!/usr/bin/env python3.7
# using https://github.com/pkkid/python-plexapi to mess with watch status
import pathlib
from os import environ
from plexapi.myplex import MyPlexAccount


class PlexAPI:
	
	def __init__(self):
		#self.host_url = str(environ['PLEX_URL'])
		self.serverName = str(environ['PLEX_SERVER'])
		self.api_key = pathlib.Path('/run/secrets/plex_api_key').read_text().strip()
		
		# TODO: was having trouble with an API key instead, will play with that further. Username paswword works for
		# now
		self.username = str(environ['PLEX_USERNAME'])
		self.password = str(environ['PLEX_PASSWORD'])
		# make a method to handle either secrets or envars
		self.account = MyPlexAccount(self.username, self.password)
		self.plex = self.account.resource(self.serverName).connect()
		self.movieLibrary = self.getMovies()
		self.movies = self.plex.library.section(str(environ['PLEX_MOVIES']))
		self.anime = self.plex.library.section(str(environ['PLEX_ANIME']))
		self.tv = self.plex.library.section(str(environ['PLEX_SHOWS']))
		print("THIS SEGMENTS FOR TESTING ONLY")
		print(self.plex._token)
		print(self.plex._baseurl)
		print(self.plex._session)
		self.setWatched()
	
	def getMovies(self):
		return self.plex.movies.search(unwatched = True)
	
	def setWatched(self):
		print(self.library.section('TV Shows').movies_gets("Game of Thrones"))
		print(self.library.section('Movies: All').movies_gets("Game of Thrones"))

# going to add some combination of example 2 and example 4 or example #6
# Example 2: Mark all Game of Thrones episodes watched.
# plex.library.section('TV Shows').movies_gets('Game of Thrones').markWatched()
