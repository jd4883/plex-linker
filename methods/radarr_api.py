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
		for i in g.full_radarr_dict:
			if 'tmdbId' in query and i['tmdbId'] == query[0]['tmdbId']:
				query[0] = i
				break
		return query
	
	def request_get(self, url, data = dict()):
		backoff_timer = 30
		get_request = dict()
		for i in range(1 - 10):
			try:
				get_request = requests.get(url, headers = { 'X-Api-Key': self.api_key }, json = data)
				break
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
				time.sleep(backoff_timer)
		return get_request
	
	def request_post(self, url, data = dict()):
		backoff_timer = 30
		post_request = dict()
		for i in range(1 - 10):
			try:
				post_request = requests.post(url, headers = { 'X-Api-Key': self.api_key }, json = data)
				break
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
				time.sleep(backoff_timer)
		return post_request
	
	def request_put(self, url, data = dict()):
		backoff_timer = 30
		put_request = dict()
		for i in range(1 - 10):
			try:
				put_request = requests.put(url, headers = { 'X-Api-Key': self.api_key }, json = data)
				break
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
				time.sleep(backoff_timer)
		return put_request
	
	def request_delete(self, url, data = dict()):
		backoff_timer = 30
		delete_request = dict()
		for i in range(1 - 10):
			try:
				delete_request = requests.delete(url, headers = { 'X-Api-Key': self.api_key }, json = data)
				break
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
				time.sleep(backoff_timer)
		return delete_request
