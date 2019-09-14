#!/usr/bin/env python3.7
# heavily based on https://github.com/SLiX69/Sonarr-API-Python-Wrapper
# -*- coding: utf-8 -*-
from os import environ

import requests


class SonarrAPI(object):
	
	def __init__(self):
		self.host_url = str(environ['SONARR_URL'])
		self.api_key = str(environ['SONARR_API_KEY'])
	
	# ENDPOINT COMMAND
	def command(self):
		pass
	
	# ENDPOINT DISKSPACE
	def get_diskspace(self):
		return self.request_get(f"{self.host_url}/diskspace").json()
	
	# ENDPOINT EPISODE
	def get_episodes_by_series_id(self,
	                              series_id):
		return self.request_get(f"{self.host_url}/episode?seriesId={series_id}").json()
	
	def get_episode_by_episode_id(self,
	                              episode_id):
		return self.request_get(f"{self.host_url}/episode/{episode_id}").json()
	
	def get_episode_files_by_series_id(self,
	                                   series_id):
		return self.request_get(f"{self.host_url}/episodefile?seriesId={series_id}").json()
	
	def get_episode_file_by_episode_id(self,
	                                   episode_id):
		return self.request_get(f"{self.host_url}/episodefile/{episode_id}").json()
	
	# ENDPOINT ROOTFOLDER
	def get_root_folder(self):
		return self.request_get(f"{self.host_url}/rootfolder").json()
	
	# ENDPOINT SERIES
	def get_series(self):
		return self.request_get(f"{self.host_url}/series").json()
	
	def get_series_by_series_id(self,
	                            series_id):
		return self.request_get(f"{self.host_url}/series/{series_id}").json()
	
	def constuct_series_json(self, tvdbId, quality_profile):
		res = self.request_get("{}/series/lookup?term={}".format(self.host_url, 'tvdbId:' + str(tvdbId)))
		s_dict = res.json()[0]
		root = self.get_root_folder()[0]['path']
		return {
			'title': s_dict['title'],
			'seasons': s_dict['seasons'],
			'path': root + s_dict['title'],
			'qualityProfileId': quality_profile,
			'seasonFolder': True,
			'monitored': True,
			'tvdbId': tvdbId,
			'images': s_dict['images'],
			'titleSlug': s_dict['titleSlug'],
			"addOptions": {
				"ignoreEpisodesWithFiles": False,
				"ignoreEpisodesWithoutFiles": False
			}
		}
	
	# ENDPOINT SERIES LOOKUP
	def lookup_series(self, query):
		return self.request_get(f"{self.host_url}/series/lookup?term={query}").json()
	
	# REQUESTS STUFF
	def request_get(self,
	                url,
	                data={}):
		headers = {'X-Api-Key': self.api_key}
		return requests.get(url,
		                    headers=headers,
		                    json=data)
	
	def request_post(self,
	                 url,
	                 data):
		return requests.post(url,
		                     headers={'X-Api-Key': self.api_key},
		                     json=data)
	
	def request_put(self,
	                url,
	                data):
		return requests.put(url,
		                    headers={'X-Api-Key': self.api_key},
		                    json=data)
	
	def request_delete(self,
	                   url,
	                   data):
		return requests.delete(url,
		                       headers={'X-Api-Key': self.api_key},
		                       json=data)
