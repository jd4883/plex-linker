#!/usr/bin/env python3.7
# heavily based on https://github.com/SLiX69/Sonarr-API-Python-Wrapper
# -*- coding: utf-8 -*-
from os import environ
import requests


# noinspection PyDefaultArgument,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,
# PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction
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
	
	# REQUESTS STUFF
	def request_get(self,
	                url,
	                data = {}):
		headers = {'X-Api-Key': self.api_key}
		return requests.get(url,
		                    headers = headers,
		                    json = data)
	
	def request_post(self,
	                 url,
	                 data):
		return requests.post(url,
		                     headers = {'X-Api-Key': self.api_key},
		                     json = data)
	
	def request_put(self,
	                url,
	                data):
		return requests.put(url,
		                    headers = {'X-Api-Key': self.api_key},
		                    json = data)
	
	def request_delete(self,
	                   url,
	                   data):
		return requests.delete(url,
		                       headers = {'X-Api-Key': self.api_key},
		                       json = data)
