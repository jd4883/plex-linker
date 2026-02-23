"""Sonarr and Radarr API clients with a shared HTTP base."""
from __future__ import annotations

import logging
import time
from typing import Any, Optional

import requests

log = logging.getLogger(__name__)


class _ArrClient:
    """Base class for *arr API clients."""

    def __init__(self, base_url: str, api_key: str, *, throttle: float = 0.5) -> None:
        self.base_url = base_url.rstrip("/")
        self._throttle = throttle
        self._session = requests.Session()
        self._session.headers["X-Api-Key"] = api_key

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        time.sleep(self._throttle)
        resp = self._session.request(method, url, params=params, json=json, timeout=30)
        resp.raise_for_status()
        return resp.json()


class SonarrClient(_ArrClient):
    def __init__(self, base_url: str, api_key: str, *, root_path_prefix: str = "/") -> None:
        super().__init__(base_url, api_key)
        self.root_path_prefix = root_path_prefix

    def get_series(self) -> list[dict]:
        return self._request("GET", "series")

    def lookup_series(self, title: str) -> Optional[dict]:
        data = self._request("GET", "series/lookup", params={"term": title})
        if isinstance(data, list) and data:
            return data[0]
        return data if data else None

    def get_episodes(self, series_id: int) -> list[dict]:
        data = self._request("GET", "episode", params={"seriesId": series_id})
        return data if isinstance(data, list) else []

    def get_episode(self, episode_id: int) -> Optional[dict]:
        if not episode_id:
            return None
        return self._request("GET", f"episode/{episode_id}")

    def get_episode_file(self, episode_file_id: int) -> Optional[dict]:
        if not episode_file_id:
            return None
        return self._request("GET", f"episodefile/{episode_file_id}")

    def get_root_folders(self) -> list[dict]:
        return self._request("GET", "rootfolder")

    def rescan_series(self, series_id: int) -> Any:
        return self._request("POST", "command", json={"name": "RescanSeries", "seriesId": series_id})

    def refresh_series(self, series_id: int) -> Any:
        return self._request("POST", "command", json={"name": "RefreshSeries", "seriesId": series_id})


class RadarrClient(_ArrClient):
    def get_movies(self) -> list[dict]:
        return self._request("GET", "movie")

    def rescan_movie(self, movie_id: int) -> Any:
        return self._request("POST", "command", json={"name": "RescanMovie", "movieId": movie_id})

    def refresh_movie(self, movie_id: int) -> Any:
        return self._request("POST", "command", json={"name": "RefreshMovie", "movieId": movie_id})
