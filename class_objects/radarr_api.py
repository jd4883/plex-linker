#!/usr/bin/env python3.7
import pathlib
from os import environ

import requests


# noinspection PyUnusedFunction,PyUnusedFunction,PyUnusedFunction
class RadarrAPI(object):
	
	def __init__(self):
		self.host_url = str(environ['RADARR_URL'])
		self.api_key = pathlib.Path('/run/secrets/radarr_api_key').read_text().replace('\n', '')
	
	# def get_movie_file(self, movie_id):
	# 	return self.request_get(f"{self.host_url}/GetMovieFile&seriesId={movie_id}").json()
	
	
	def refresh_movie(self, movie_id):
		return self.request_post(f"{self.host_url}/command/RefreshMovie&seriesId={movie_id}").json()
	
	def rescan_movie(self, movie_id):
		return self.request_post(f"{self.host_url}/command/RescanMovie&seriesId={movie_id}").json()
	
	def movie_search(self, movie_id):
		return self.request_post(f"{self.host_url}/command/MoviesSearch&seriesId={movie_id}").json()
	
	def get_movie_library(self):
		return self.request_get(f"{self.host_url}/movie").json()
	
	def lookup_movie(self, query, g):
		query = self.request_get(f"{self.host_url}/movie/lookup?term={query}").json()
		for i in g.movies_dictionary:
			if 'tmdbId' in query and i['tmdbId'] == query[0]['tmdbId']:
				query[0] = i
				#del g.movies_dictionary[i]
				#print(f"MODIFIED QUERY: {query}")
				return query
		raise KeyError
	
	def request_get(self, url, data=dict()):
		return requests.get(url, headers={'X-Api-Key': self.api_key}, json=data)
	
	def request_post(self, url, data=dict()):
		return requests.post(url, headers={'X-Api-Key': self.api_key}, json=data)
	
	def request_put(self, url, data=dict()):
		return requests.put(url, headers={'X-Api-Key': self.api_key}, json=data)
	
	def request_delete(self, url, data=dict()):
		return requests.delete(url, headers={'X-Api-Key': self.api_key}, json=data)
