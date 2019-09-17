#!/usr/bin/env python3.7
# heavily based on https://github.com/SLiX69/Sonarr-API-Python-Wrapper
# -*- coding: utf-8 -*-
from os import environ


# noinspection PyDefaultArgument,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction
class RadarrAPI(object):
	
	def __init__(self):
		self.host_url = str(environ['RADARR_URL'])
		self.api_key = str(environ['RADARR_API_KEY'])
	
	# ENDPOINT MOVIE
	def get_movie_library(self):
		return self.request_get(f"{self.host_url}/movie").json()
	
	# ENDPOINT MOVIE LOOKUP
	def lookup_movie(self,
	                 query):
		return self.request_get(f"{self.host_url}/movie/lookup?term={query}").json()
