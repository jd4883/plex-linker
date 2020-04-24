#!/usr/bin/env python3.7
import pathlib
import re
import time
from os import environ

import requests


# noinspection PyUnusedFunction,PyUnusedFunction,PyUnusedFunction
class RadarrAPI(object):
	
	def __init__(self):
		self.host_url = str(environ['RADARR_URL'])
		self.api_key = re.sub('\n', '', pathlib.Path('/run/secrets/radarr_api_key').read_text())
	
	def refresh_movie(self, movie_id):
		update_movie = self.radarr_api_request(f"{self.host_url}/command/RefreshMovie&seriesId={movie_id}", "post")
		return update_movie
	
	def rescan_movie(self, movie_id):
		rescanned_movie = self.radarr_api_request(f"{self.host_url}/command/RescanMovie&seriesId={movie_id}", "post")
		return rescanned_movie
	
	def movie_search(self, movie_id):
		movie_search = self.radarr_api_request(f"{self.host_url}/command/MoviesSearch&seriesId={movie_id}", "post")
		return movie_search
	
	def get_movie_library(self):
		full_movie_library = self.radarr_api_request(f"{self.host_url}/movie")
		return full_movie_library
	
	def lookup_movie(self, movie_lookup, g):
		movie_lookup = self.radarr_api_request(f"{self.host_url}/movie/lookup?term={movie_lookup}")
		for i in g.full_radarr_dict:
			if 'tmdbId' in movie_lookup and i['tmdbId'] == movie_lookup[0]['tmdbId']:
				movie_lookup[0] = i
				break
		return movie_lookup
	
	def radarr_api_request(self, url, type = "get", data = dict()):
		backoff_timer = 2
		if type not in ["post", "put", "delete"]:
			request_payload = requests.get(url, headers = { 'X-Api-Key': self.api_key }, json = data)
		elif type == "put":
			request_payload = requests.put(url, headers = { 'X-Api-Key': self.api_key }, json = data)
		elif type == "post":
			request_payload = requests.post(url, headers = { 'X-Api-Key': self.api_key }, json = data)
		elif type == "delete":
			request_payload = requests.delete(url, headers = { 'X-Api-Key': self.api_key }, json = data)
		time.sleep(backoff_timer)
		return request_payload.json()
