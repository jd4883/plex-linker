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
	
	def lookup_series(self, show):
		"""
		Lookup series Method
		:param show: The show to lookup and fill in values for the API
		:type show: class object
		:return: None
		:description: This method calls Sonarr's API and sets class object values seen below. Some of these are
		subject to be prioritized by other API calls later on but can use these as starting points
		"""
		
		prefix = os.environ["SONARR_ROOT_PATH_PREFIX"]
		try:
			base = self.sonarr_api_request(f"{self.host_url}/series/lookup?term={show.title}")[0]
			show.id = show.inherited_series_dict['Series ID'] = show.seriesId = int(base.get("id", 0))
		except KeyError or IndexError or TypeError:
			return False
		if not show.id:
			return False
		show.cleanTitle = base.get("cleanTitle", str())
		show.firstAired = base.get("firstAired", str())
		show.genres = base.get("genres", list())
		show.imdbId = base.get("imdbId", str())
		show.languageProfileId = int(base.get("languageProfileId", 0))
		show.path = show.inherited_series_dict['Show Root Path'] = str(base.pop("path")).replace(prefix, "")
		show.profileId = int(base.get("profileId", 0))
		show.qualityProfileId = int(base.get("qualityProfileId", 0))
		show.ratings = base.get("ratings", dict())
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
		# TODO: this segment should also apply to absolute episodes
		# show.parsed_absolute_episode = "-".join([e.zfill(show.padding) for e in show.absolute_ep])
		show.anime_status = bool("anime" in show.seriesType)
		show.padding = 3 if show.anime_status else 2
		show.parseEpisode()
		os.makedirs(show.path, exist_ok = True)
		return True
	
	def get_episodes_by_series_id(self, show):
		request = self.sonarr_api_request(f"{self.host_url}/episode?seriesId={show.seriesId}")
		if request:
			for i in request:
				try:
					parseEpisode = bool(int(i["episodeNumber"]) == show.inherited_series_dict["Episode"])
				except KeyError:
					print(f"KEY ERROR FOR {show.title} TO {show.movieTitle}")
					break
				parseSeason = bool(int(i["seasonNumber"]) == 0)
				if parseEpisode and parseSeason:
					show.absoluteEpisodeNumber = i.get("absoluteEpisodeNumber", 0)
					show.episodeId = i.pop("id")
					show.episodeTitle = show.inherited_series_dict['Title'] = re.sub('\(''\d+\)$', "", i.pop("title"))
					show.hasFile = i.pop("hasFile")
					show.monitored = False
					show.unverifiedSceneNumbering = i.pop("unverifiedSceneNumbering")
					show.episodeSize = i.get("size", 0)
					if show.hasFile or ("episodeFile" in i and i["episodeFile"]):
						episodeFileDict = i["episodeFile"]
						show.hasFile = True
						show.qualityDict = i.get("quality", dict())
						show.absolute_episode_path = episodeFileDict.pop("path", 0)
						show.episodeFileId = show.inherited_series_dict['episodeFileId'] = episodeFileDict.pop("id", 0)
						show.languageDict = episodeFileDict.pop("language", 0)
						show.qualityCutoffNotMet = episodeFileDict.pop("qualityCutoffNotMet")
						show.relativeEpisodePath = episodeFileDict.pop("relativePath", 0)
					# show.relative_show_file_path = str('/'.join([show.path, show.seasonFolder, show.title])) \
					#                                + " - S" \
					#                                + str(show.season) \
					#                                + "E" \
					#                                + str(show.parsed_episode) \
					#                                + " - " \
					#                                + str(show.episodeTitle)
					break
	
	def get_episode_by_episode_id(self, episode_id):
		# TODO: this is one of the next areas to improve; ensure all properties are parsing correctly
		if episode_id:
			return self.sonarr_api_request(f"{self.host_url}/episode/{episode_id}")
	
	def get_episode_file_by_episode_id(self, episode_id):
		return self.sonarr_api_request(f"{self.host_url}/episodefile/{episode_id}")
	
	def get_root_folder(self):
		return self.sonarr_api_request(f"{self.host_url}/rootfolder")
	
	def get_series(self):
		return self.sonarr_api_request(f"{self.host_url}/series")
	
	def refresh_series(self, series_id, data = dict()):
		return self.sonarr_api_request(f"{self.host_url}/command/RefreshSeries&seriesId={series_id}", "post",
		                               data)
	
	def rescan_series(self, series_id, data = dict()):
		return self.sonarr_api_request(f"{self.host_url}/command/RescanSeries&seriesId={series_id}", "post",
		                               data)
