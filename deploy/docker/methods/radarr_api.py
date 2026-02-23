"""Radarr API client. Base URL = RADARR_0_URL + RADARR_0_API_PATH (default /api/v3)."""
import time
from typing import Any, Optional

import requests

from config import radarr_api_base, radarr_api_key


class RadarrAPI:
    def __init__(self) -> None:
        self.base_url = radarr_api_base().rstrip("/")
        self.api_key = radarr_api_key()
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

    def refresh_movie(self, movie_id: int) -> Any:
        return self._request("POST", "command", json_body={"name": "RefreshMovie", "movieId": movie_id})

    def rescan_movie(self, movie_id: int) -> Any:
        return self._request("POST", "command", json_body={"name": "RescanMovie", "movieId": movie_id})

    def movie_search(self, movie_id: int) -> Any:
        return self._request("POST", "command", json_body={"name": "MoviesSearch", "movieIds": [movie_id]})

    def get_movie_library(self) -> Any:
        return self._request("GET", "movie")

    def lookup_movie(self, term: str, g) -> Any:
        data = self._request("GET", "movie/lookup", params={"term": term})
        if not isinstance(data, list) or not data:
            return data
        first = data[0]
        tmdb = first.get("tmdbId")
        if tmdb is not None and g.full_radarr_dict:
            for i in g.full_radarr_dict:
                if i.get("tmdbId") == tmdb:
                    return [i]
        return data
