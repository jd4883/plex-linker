import pathlib
import os
import requests
import messaging.backend
from jobs.cleanup.cleanup import cleanup_sonarr_api_query


class SonarrAPI(object):
	def __init__(self):
		self.host_url = str(os.environ['SONARR_URL'])
		self.api_key = pathlib.Path('/run/secrets/sonarr_api_key').read_text().replace('\n', '')
	
	def get_episodes_by_series_id(self, series_id):
		return self.request_get(f"{self.host_url}/episode?seriesId={series_id}").json()
	
	# def get_series_by_tvdb_id(self, tvdbId):
	# 	return self.request_get(f"{self.host_url}/lookup?term=tvdb:{tvdbId}").json()
	
	def get_episode_by_episode_id(self, episode_id):
		return self.request_get(f"{self.host_url}/episode/{episode_id}").json()
	
	#
	# def get_all_tag_ids(self):
	# 	return self.request_get(f"{self.host_url}/tag").json()
	
	# def get_episode_files_by_series_id(self, series_id):
	# 	return self.request_get(f"{self.host_url}/episodefile?seriesId={series_id}").json()
	
	def get_episode_file_by_episode_id(self, episode_id):
		return self.request_get(f"{self.host_url}/episodefile/{episode_id}").json()
	
	def get_root_folder(self):
		return self.request_get(f"{self.host_url}/rootfolder").json()
	
	def get_series(self):
		return self.request_get(f"{self.host_url}/series").json()
	
	def get_series_by_series_id(self, series_id, g):
		query = self.request_get(f"{self.host_url}/series/{series_id}").json()
		for i in g.full_sonarr_dict:
			if 'id' in query and i['id'] == series_id or \
					'tvdbId' in query and i['tvdbId'] == query[0]['tvdbId']:
				query[0] = i
				return i
		return
	
	def set_series_tags(self, label, series_id, data = dict()):
		return self.request_post(f"{self.host_url}/series/{series_id}/tag&label={str(label).lower()}", data).json()
	
	def set_new_tag_for_sonarr(self, label, data = dict()):
		return self.request_post(f"{self.host_url}/tag&label={str(label).lower()}", data).json()
	
	def refresh_series(self, series_id, data = dict()):
		return self.request_post(f"{self.host_url}/command/RefreshSeries&seriesId={series_id}", data).json()
	
	def rescan_series(self, series_id, data = dict()):
		return self.request_post(f"{self.host_url}/command/RescanSeries&seriesId={series_id}", data).json()
	
	def constuct_series_json(self, tvdbid, quality_profile):
		res = self.request_get(f"{self.host_url}/series/lookup?term={'tvdbId:' + str(tvdbid)}")
		return {
				'title':            res.json()[0]['title'],
				'seasons':          res.json()[0]['seasons'],
				'path':             self.get_root_folder()[0]['path'] + res.json()[0]['title'],
				'qualityProfileId': quality_profile,
				'seasonFolder':     True,
				'monitored':        True,
				'tvdbId':           tvdbid,
				'images':           res.json()[0]['images'],
				'titleSlug':        res.json()[0]['titleSlug'],
				"addOptions":       {
						"ignoreEpisodesWithFiles":    False,
						"ignoreEpisodesWithoutFiles": False
						}
				}
	
	def lookup_series(self, query, g):
		payload = cleanup_sonarr_api_query(self.request_get(f"{self.host_url}/series/lookup?term={query}").json())
		try:
			payload = payload[0]
		except IndexError:
			pass
		g.LOG.debug(messaging.backend.debug_message(625, g, payload))
		return payload
	
	def request_get(self, url, data = dict()):
		return requests.get(url, headers = { 'X-Api-Key': self.api_key }, json = data)
	
	def request_post(self, url, data = dict()):
		return requests.post(url, headers = { 'X-Api-Key': self.api_key }, json = data)
	
	def request_put(self, url, data = dict()):
		return requests.put(url, headers = { 'X-Api-Key': self.api_key }, json = data)
	
	def request_delete(self, url, data = dict()):
		return requests.delete(url, headers = { 'X-Api-Key': self.api_key }, json = data)
