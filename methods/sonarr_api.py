import os
import pathlib
import re
import time

import requests

import messaging.backend


class SonarrAPI(object):
	def __init__(self):
		self.host_url = str(os.environ['SONARR_URL'])
		self.api_key = re.sub('\n', '', pathlib.Path('/run/secrets/sonarr_api_key').read_text())
	
	def get_episodes_by_series_id(self, series_id):
		return self.request_get(f"{self.host_url}/episode?seriesId={series_id}")
	
	def get_episode_by_episode_id(self, episode_id):
		return self.request_get(f"{self.host_url}/episode/{episode_id}")
	
	def get_episode_file_by_episode_id(self, episode_id):
		return self.request_get(f"{self.host_url}/episodefile/{episode_id}")
	
	def get_root_folder(self):
		try:
			get_request = self.request_get(f"{self.host_url}/rootfolder")
		except AttributeError:
			get_request = dict()
		return get_request
	
	def get_series(self):
		series = dict()
		try:
			series = self.request_get(f"{self.host_url}/series")
		except AttributeError:
			pass
		return series
	
	def refresh_series(self, series_id, data = dict()):
		return self.request_post(f"{self.host_url}/command/RefreshSeries&seriesId={series_id}", data)
	
	def rescan_series(self, series_id, data = dict()):
		return self.request_post(f"{self.host_url}/command/RescanSeries&seriesId={series_id}", data)
	
	def lookup_series(self, series, g):
		sonarr_series = self.request_get(f"{self.host_url}/series/lookup?term={series}")
		if type(sonarr_series) == list:
			sonarr_series = sonarr_series[0]
		g.LOG.info(messaging.backend.debug_message(625, g, sonarr_series))
		return sonarr_series
	
	def request_get(self, url, data = dict()):
		backoff_timer = 30
		get_request = dict()
		for i in range(1 - 10):
			try:
				get_request = requests.get(url, headers = { 'X-Api-Key': self.api_key }, json = data)
				get_request = get_request.json()
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
				time.sleep(backoff_timer)
		print(f"GET REQUEST: {get_request}")
		return get_request
	
	def request_post(self, url, data = dict()):
		backoff_timer = 30
		post_request = dict()
		for i in range(1 - 10):
			try:
				post_request = requests.post(url, headers = { 'X-Api-Key': self.api_key }, json = data)
				post_request = post_request.json()
				break
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
				time.sleep(backoff_timer)
		print(f"POST REQUEST: {post_request}")
		return post_request
