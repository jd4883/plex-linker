#!/usr/bin/env python3.7
from os import environ
import json
import pathlib
import re
import requests
import time


# noinspection PyUnusedFunction,PyUnusedFunction,PyUnusedFunction
class RadarrAPI(object):
	def __init__(self):
		self.host_url = str(environ['RADARR_URL'])
		self.api_key = str(environ['RADARR_API_KEY'])
	
	def radarr_api_request(self, url, request_type = "get", data = dict()):
		backoff_timer = 2
		payload = json.dumps(data)
		request_payload = dict()
		if request_type not in ["post", "put", "delete"]:
			request_payload = requests.get(url, headers = { 'X-Api-Key': self.api_key }, data = payload)
		elif request_type == "put":
			request_payload = requests.put(url, headers = { 'X-Api-Key': self.api_key }, data = payload)
		elif request_type == "post":
			request_payload = requests.post(url, headers = { 'X-Api-Key': self.api_key }, data = payload)
		elif request_type == "delete":
			request_payload = requests.delete(url, headers = { 'X-Api-Key': self.api_key }, data = payload)
		time.sleep(backoff_timer)
		return request_payload.json()
	
	def refresh_movie(self, movie_id):
		return self.radarr_api_request(f"{self.host_url}/command?name=RefreshMovie&movieId={movie_id}", "post")
	
	def rescan_movie(self, movie_id):
		return self.radarr_api_request(f"{self.host_url}/command?name=RescanMovie&movieId={movie_id}", "post")
	
	def movie_search(self, movie_id):
		return self.radarr_api_request(f"{self.host_url}/command?name=MoviesSearch&movieIds={movie_id}", "post")
	
	def get_movie_library(self):
		return self.radarr_api_request(f"{self.host_url}/movie")
	
	def lookup_movie(self, movie_lookup, g):
		movie_lookup = self.radarr_api_request(f"{self.host_url}/movie/lookup?term={movie_lookup}")
		for i in g.full_radarr_dict:
			if 'tmdbId' in movie_lookup and i['tmdbId'] == iter(movie_lookup).__next__()['tmdbId']:
				movie_lookup[0] = i
				break
		return movie_lookup
