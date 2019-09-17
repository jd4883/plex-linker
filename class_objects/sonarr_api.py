#!/usr/bin/env python3.7
# heavily based on https://github.com/SLiX69/Sonarr-API-Python-Wrapper
# -*- coding: utf-8 -*-
from os import environ

import requests


# noinspection PyDefaultArgument,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction
class SonarrAPI(object):
	
	def __init__(self):
		self.host_url = str(environ['SONARR_URL'])
		self.api_key = str(environ['SONARR_API_KEY'])
	
	# ENDPOINT EPISODE
	def get_episodes_by_series_id(self,
	                              series_id):
		return self.request_get(f"{self.host_url}/episode?seriesId={series_id}").json()
	
	def get_episode_by_episode_id(self,
	                              episode_id):
		return self.request_get(f"{self.host_url}/episode/{episode_id}").json()
	
	def get_all_tag_ids(self):
		return self.request_get(f"{self.host_url}/tag").json()
	
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
	
	# noinspection PyDefaultArgument
	def set_series_tags(self,
	                    label,
	                    series_id,
	                    data={}):
		label = str(label).lower()
		return self.request_post(f"{self.host_url}/series/{series_id}/tag&label={label}",
		                         data).json()
	
	# noinspection PyDefaultArgument
	def set_new_tag_for_sonarr(self,
	                           label,
	                           data={}):
		label = str(label).lower()
		return self.request_post(f"{self.host_url}/tag&label={label}",
		                         data).json()
	
	def constuct_series_json(self,
	                         tvdbid,
	                         quality_profile):
		res = self.request_get(f"{self.host_url}/series/lookup?term={'tvdbId:' + str(tvdbid)}")
		return {
			'title': res.json()[0]['title'],
			'seasons': res.json()[0]['seasons'],
			'path': self.get_root_folder()[0]['path'] + res.json()[0]['title'],
			'qualityProfileId': quality_profile,
			'seasonFolder': True,
			'monitored': True,
			'tvdbId': tvdbid,
			'images': res.json()[0]['images'],
			'titleSlug': res.json()[0]['titleSlug'],
			"addOptions": {
				"ignoreEpisodesWithFiles": False,
				"ignoreEpisodesWithoutFiles": False
			}
		}
	
	# ENDPOINT SERIES LOOKUP
	def lookup_series(self,
	                  query):
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


