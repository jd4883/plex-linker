#!/usr/bin/env python3.7
from os import environ

import requests


class RadarrAPI(object):
	
	def __init__(self):
		self.host_url = str(environ['RADARR_URL'])
		self.api_key = str(environ['RADARR_API_KEY'])
	
	def get_movie_library(self):
		return self.request_get(f"{self.host_url}/movie").json()
	
	def lookup_movie(self, query):
		return self.request_get(f"{self.host_url}/movie/lookup?term={query}").json()
	
	def request_get(self, url, data = {}):
		return requests.get(url, headers = {'X-Api-Key': self.api_key}, json = data)
	
	def request_post(self, url, data):
		return requests.post(url, headers = {'X-Api-Key': self.api_key}, json = data)
	
	def request_put(self, url, data):
		return requests.put(url, headers = {'X-Api-Key': self.api_key}, json = data)
	
	def request_delete(self, url, data):
		return requests.delete(url, headers = {'X-Api-Key': self.api_key}, json = data)
