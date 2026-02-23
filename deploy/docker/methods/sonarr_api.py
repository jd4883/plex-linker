"""Sonarr API client. Base URL is built from SONARR_0_URL + SONARR_0_API_PATH (default /api/v3)."""
import os
import re
import time
from typing import Any, Optional

import requests

from config import sonarr_api_base, sonarr_api_key, sonarr_root_path_prefix


class SonarrAPI:
    def __init__(self) -> None:
        self.base_url = sonarr_api_base().rstrip("/")
        self.api_key = sonarr_api_key()
        self._session = requests.Session()
        self._session.headers["X-Api-Key"] = self.api_key

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict] = None,
        json_body: Optional[dict] = None,
    ) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        time.sleep(0.5)
        if method.upper() == "GET":
            r = self._session.get(url, params=params, timeout=30)
        elif method.upper() == "POST":
            r = self._session.post(url, params=params, json=json_body, timeout=30)
        elif method.upper() == "PUT":
            r = self._session.put(url, params=params, json=json_body, timeout=30)
        elif method.upper() == "DELETE":
            r = self._session.delete(url, params=params, timeout=30)
        else:
            raise ValueError(f"Unsupported method {method}")
        r.raise_for_status()
        return r.json()

    def lookup_series(self, show) -> bool:
        try:
            data = self._request("GET", "series/lookup", params={"term": show.title})
            base = data[0] if isinstance(data, list) and data else data
            if not base:
                return False
            show.id = show.inherited_series_dict["Series ID"] = show.seriesId = int(base.get("id", 0))
            if not show.seriesId:
                return False
            prefix = sonarr_root_path_prefix()
            show.cleanTitle = base.get("cleanTitle", "")
            show.firstAired = base.get("firstAired", "")
            show.genres = base.get("genres", [])
            show.imdbId = base.get("imdbId", "")
            show.languageProfileId = int(base.get("languageProfileId", 0))
            show.path = show.inherited_series_dict["Show Root Path"] = str(base.get("path", "")).replace(prefix, "")
            show.profileId = int(base.get("profileId", 0))
            show.qualityProfileId = int(base.get("qualityProfileId", 0))
            show.ratings = base.get("ratings", {})
            show.runtime = base.get("runtime", 0)
            show.seasonCount = base.get("seasonCount", 0)
            show.seasonFolder = base.get("seasonFolder", True)
            show.seasons = base.get("seasons", [])
            show.seriesType = base.get("seriesType", "")
            show.sortTitle = base.get("sortTitle", "")
            show.status = base.get("status", "")
            show.tags = base.get("tags", [])
            show.title = base.get("title", "")
            show.titleSlug = base.get("titleSlug", "")
            show.tvdbId = base.get("tvdbId", 0)
            show.tvMazeId = base.get("tvMazeId", 0)
            show.tvRageId = base.get("tvRageId", 0)
            show.useSceneNumbering = base.get("useSceneNumbering", False)
            show.year = base.get("year", 0)
            show.anime_status = "anime" in (show.seriesType or "")
            show.padding = 3 if show.anime_status else 2
            show.parseEpisode()
            if show.path:
                os.makedirs(show.path, exist_ok=True)
            return True
        except (KeyError, IndexError, TypeError, requests.RequestException):
            return False

    def get_episodes_by_series_id(self, show) -> None:
        data = self._request("GET", "episode", params={"seriesId": show.seriesId})
        if not isinstance(data, list):
            return
        for i in data:
            try:
                ep_num = int(i.get("episodeNumber", -1))
                season_num = int(i.get("seasonNumber", -1))
            except (TypeError, ValueError):
                continue
            if ep_num != show.inherited_series_dict.get("Episode"):
                continue
            if season_num != 0:
                continue
            show.absoluteEpisodeNumber = i.get("absoluteEpisodeNumber", 0)
            show.episodeId = i.get("id", 0)
            show.episodeTitle = show.inherited_series_dict["Title"] = re.sub(r"\(\d+\)$", "", i.get("title", ""))
            show.hasFile = i.get("hasFile", False)
            show.monitored = False
            show.unverifiedSceneNumbering = i.get("unverifiedSceneNumbering", False)
            show.episodeSize = i.get("size", 0)
            ep_file = i.get("episodeFile")
            if ep_file:
                show.hasFile = True
                show.qualityDict = i.get("quality", {})
                show.absolute_episode_path = ep_file.get("path", "")
                show.episodeFileId = show.inherited_series_dict["episodeFileId"] = ep_file.get("id", 0)
                show.languageDict = ep_file.get("language", {})
                show.qualityCutoffNotMet = ep_file.get("qualityCutoffNotMet", False)
                show.relativeEpisodePath = ep_file.get("relativePath", "")
            break

    def get_episode_by_episode_id(self, episode_id: int) -> Optional[dict]:
        if not episode_id:
            return None
        return self._request("GET", f"episode/{episode_id}")

    def get_episode_file_by_episode_id(self, episode_id: int) -> Any:
        return self._request("GET", f"episodefile/{episode_id}")

    def get_root_folder(self) -> Any:
        return self._request("GET", "rootfolder")

    def get_series(self) -> Any:
        return self._request("GET", "series")

    def refresh_series(self, series_id: int, data: Optional[dict] = None) -> Any:
        body = {"name": "RefreshSeries", "seriesId": series_id}
        if data:
            body.update(data)
        return self._request("POST", "command", json_body=body)

    def rescan_series(self, series_id: int, data: Optional[dict] = None) -> Any:
        body = {"name": "RescanSeries", "seriesId": series_id}
        if data:
            body.update(data)
        return self._request("POST", "command", json_body=body)
