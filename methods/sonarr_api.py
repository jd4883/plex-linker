import os
import pathlib
import re
import time

import requests


class SonarrAPI(object):
	def __init__(self):
		self.host_url = str(os.environ['SONARR_URL'])
		self.api_key = re.sub('\n', '', pathlib.Path('/run/secrets/sonarr_api_key').read_text())
	
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
	
	def lookup_series(self, show, g):
		"""
		Lookup series Method
		:param show: The show to lookup and fill in values for the API
		:type show: class object
		:param g: globals object
		:type g: Globals object
		:return: None
		:description: This method calls Sonarr's API and sets class object values seen below. Some of these are
		subject to be prioritized by other API calls later on but can use these as starting points
		"""
		
		base = self.sonarr_api_request(f"{self.host_url}/series/lookup?term={show.title}")[0]
		show.cleanTitle = base.pop("cleanTitle")
		show.firstAired = base.pop("firstAired")
		show.genres = base.pop("genres")
		show.id = show.seriesId = int(base.pop("id"))
		show.imdbId = base.pop("imdbId")
		show.languageProfileId = int(base.pop("languageProfileId"))
		show.path = str(base.pop("path"))
		show.profileId = int(base.pop("profileId"))
		show.qualityProfileId = int(base.pop("qualityProfileId"))
		show.ratings = base.pop("ratings")
		show.runtime = base.pop("runtime")
		show.seasonCount = base.pop("seasonCount")
		show.seasonFolder = base.pop("seasonFolder")
		show.seasons = base.pop("seasons")
		show.seriesType = base.pop("seriesType")
		show.sortTitle = base.pop("sortTitle")
		show.status = base.pop("status")
		show.tags = base.pop("tags")
		show.title = base.pop("title")
		show.titleSlug = base.pop("titleSlug")
		show.tvdbId = base.pop("tvdbId")
		show.tvMazeId = base.pop("tvMazeId")
		show.tvRageId = base.pop("tvRageId")
		show.useSceneNumbering = base.pop("useSceneNumbering")
		show.year = base.pop("year")
		del base
		show.anime_status = bool("anime" in show.seriesType)
	
	def get_episodes_by_series_id(self, show):
		dictOfEpisodesFromSeriesId = self.sonarr_api_request(f"{self.host_url}/episode?seriesId={show.seriesId}")
		for i in dictOfEpisodesFromSeriesId:
			parseEpisode = bool(int(i["episodeNumber"]) == int(show.inherited_series_dict["Episode"]))
			parseSeason = bool(int(i["seasonNumber"]) == (0 or show.seasonNumber))
			if parseEpisode and parseSeason:
				print(i)
				show.absoluteEpisodeNumber = i.get("absoluteEpisodeNumber", 0)
				show.episodeId = i.pop("id")
				show.episodeTitle = i.pop("title")
				show.hasFile = i.pop("hasFile")
				show.monitored = False
				show.unverifiedSceneNumbering = i.pop("unverifiedSceneNumbering")
				show.episodeSize = i.get("size", 0)
				if show.hasFile or ("episodeFile" in i and i["episodeFile"]):
					episodeFileDict = i["episodeFile"]
					show.hasFile = True
					show.qualityDict = i.pop("quality")
					show.absolute_episode_path = episodeFileDict.pop("path", 0)
					show.episodeFileId = episodeFileDict.pop("id", 0)
					show.languageDict = episodeFileDict.pop("language", 0)
					show.qualityCutoffNotMet = episodeFileDict.pop("qualityCutoffNotMet")
					show.relativeEpisodePath = episodeFileDict.pop("relativePath", 0)
				break
	
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
