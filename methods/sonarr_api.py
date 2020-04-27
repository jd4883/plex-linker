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
		episode_by_series_id = self.sonarr_api_request(f"{self.host_url}/episode?seriesId={series_id}")
		return episode_by_series_id
	
	def get_episode_by_episode_id(self, episode_id):
		episode_by_episode_id = self.sonarr_api_request(f"{self.host_url}/episode/{episode_id}")
		return episode_by_episode_id
	
	def get_episode_file_by_episode_id(self, episode_id):
		episode_file_by_id = self.sonarr_api_request(f"{self.host_url}/episodefile/{episode_id}")
		return episode_file_by_id
	
	def get_root_folder(self):
		try:
			get_request = self.sonarr_api_request(f"{self.host_url}/rootfolder")
			return get_request
		except AttributeError as a:
			print(a)
	
	def get_series(self):
		series = self.sonarr_api_request(f"{self.host_url}/series")
		return series
	
	def refresh_series(self, series_id, data = dict()):
		rescan_series = self.sonarr_api_request(f"{self.host_url}/command/RefreshSeries&seriesId={series_id}", "post",
		                                        data)
		return rescan_series
	
	def rescan_series(self, series_id, data = dict()):
		series_scan = self.sonarr_api_request(f"{self.host_url}/command/RescanSeries&seriesId={series_id}", "post",
		                                      data)
		return series_scan
	
	def lookup_series(self, series, g):
		sonarr_series = self.sonarr_api_request(f"{self.host_url}/series/lookup?term={series}")[0]
		exclude_list = [
				"added",
				"airTime",
				"certification",
				"firstAired",
				"images",
				"lastInfoSync",
				"monitored",
				"network",
				"overview",
				"remotePoster",
				]
		temp = sonarr_series
		{ sonarr_series.pop(k, None) for k, v in temp.items() if k in exclude_list }
		del temp
		g.LOG.info(messaging.backend.debug_message(625, g, sonarr_series))
		return sonarr_series
	
	def sonarr_api_request(self, url, request_type = "get", data = dict()):
		backoff_timer = 2
		request_payload = dict()
		if request_type not in ["post", "put", "delete"]:
			request_payload = requests.get(url, headers = { 'X-Api-Key': self.api_key }, json = data)
		elif request_type == "put":
			request_payload = requests.put(url, headers = { 'X-Api-Key': self.api_key }, json = data)
		elif request_type == "post":
			request_payload = requests.post(url, headers = { 'X-Api-Key': self.api_key }, json = data)
		elif request_type == "delete":
			request_payload = requests.delete(url, headers = { 'X-Api-Key': self.api_key }, json = data)
		time.sleep(backoff_timer)
		return request_payload.json()
