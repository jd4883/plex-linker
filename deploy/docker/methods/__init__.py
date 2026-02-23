"""Shared state and models for the link job (Sonarr/Radarr, media paths, logging)."""
import logging
import os
import re
import time
from os.path import abspath, join

import plex_linker.cleanup.movie as cleanup_movie
import plex_linker.fetch.series as fetch_series
import plex_linker.parser.series as parse_series
from config import logs_dir as config_logs_dir, media_root as config_media_root
from data_provider import get_setting
from messaging.backend import log_debug
from methods.misc_get_methods import (
    get_movie_extensions,
    get_movies_dictionary_object,
    get_movies_path,
    get_shows_path,
)
from methods.radarr_api import RadarrAPI
from methods.sonarr_api import SonarrAPI
from plex_linker.compare.ids import validate_tmdbId
from plex_linker.gets.movie import get_relative_movies_path
from plex_linker.parser.series import padded_absolute_episode


def _log_path():
    d = config_logs_dir()
    return os.path.join(d, "plex_linker.log") if d else ""


def _setup_logging(log_path: str) -> logging.Logger:
    if log_path:
        mode = "a+" if os.path.exists(log_path) else "w+"
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s",
            datefmt="%m-%d %H:%M",
            filename=log_path,
            filemode=mode,
        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(name)-12s:\t%(levelname)-8s\t%(message)s"))
    logger = logging.getLogger("plex_linker")
    logger.addHandler(console)
    return logger


class Globals:
    def __init__(self):
        self.sonarr = SonarrAPI()
        self.radarr = RadarrAPI()
        self.sonarr_root_folders = self.sonarr.get_root_folder()
        self.full_sonarr_dict = self.sonarr.get_series()
        self.full_radarr_dict = self.radarr.get_movie_library()
        self.MEDIA_PATH = str(config_media_root())
        self.MEDIA_DIRECTORY = str(os.environ.get("HOST_MEDIA_PATH", self.MEDIA_PATH))
        self.LOG = _setup_logging(_log_path())
        self.MOVIES_PATH = get_movies_path()
        self.SHOWS_PATH = get_shows_path()
        self.movies_dict = get_movies_dictionary_object()
        self.method = self.parent_method = "main"

    def __repr__(self):
        return "<Globals()>"


class Movies:
    def __init__(self, absolute_movies_path=None):
        if absolute_movies_path is None:
            media_root = os.environ.get("DOCKER_MEDIA_PATH", "")
            dirs = get_setting("Movie Directories")
            first = next(iter(dirs), "") if dirs else ""
            absolute_movies_path = abspath(join(media_root, str(first))) if first else ""
        self.start_time = time.time()
        self.absolute_movies_path = absolute_movies_path
        self.relative_movies_path = get_relative_movies_path(self)

    def __repr__(self):
        return "<Movies()>"


class Movie(Movies, Globals):
    def __init__(self, movie_dict, g):
        super().__init__()
        self.movie_dictionary = movie_dict
        self.shows_dictionary = self.movie_dictionary.get("Shows", {})
        cleanup_movie.cleanup_dict(self.movie_dictionary)
        self.tmbdid = self.movie_dictionary.get("Movie DB ID")
		g.LOG.debug(log_debug(g, "movie dictionary", self.movie_dictionary))
		g.LOG.debug(log_debug(g, "shows dictionary", self.shows_dictionary))
		g.LOG.debug(log_debug(g, "movie db id", self.tmbdid))
        self.alternativeTitles = []
        self.audioLanguages = ""
        self.cleanMovieTitle = ""
        self.downloaded = False
        self.genres = ""
        self.hasFile = False
        self.imdbid = 0
        self.inCinemas = ""
        self.isAvailable = False
        self.mediaInfo = ""
        self.monitored = False
        self.movieFileId = 0
        self.movieId = 0
        self.moviePath = ""
        self.movieQuality = ""
        self.movieRuntime = 0
        self.movieTitle = ""
        self.qualityProfileId = 0
        self.radarrProfileId = 0
        self.relativePath = ""
        self.runtime = 0
        self.sizeonDisk = 0
        self.sortTitle = ""
        self.titleslug = ""
        self.year = 0
        self.absolute_movie_file_path = ""
        self.extension = ".mkv"
        self.quality = ""
        self.relative_movie_path = ""
        self.parse_dict_from_radarr(g)

    @property
    def movie_title(self):
        return self.movieTitle

    def __repr__(self):
        return f"<Movie(name={self.movieTitle!r})>"

    def parse_dict_from_radarr(self, g):
        if not validate_tmdbId(self.tmbdid):
            return
        try:
            index = None
            for i, d in enumerate(g.full_radarr_dict):
                if d.get("tmdbId") == self.movie_dictionary.get("Movie DB ID"):
                    index = i
                    break
            if index is None:
                return
            items = g.full_radarr_dict[index].copy()
			g.LOG.debug(log_debug(g, "radarr movie dict", items))
            title = re.sub(r"\s+\(0\)\s?", "", items.pop("title", ""))
            self.movieTitle = re.sub(r"\s+\(0\)\s?", "", re.sub("/", "+", re.sub(":", "-", f"{title} ({self.year})")))
            self.hasFile = items.pop("hasFile", False)
            self.monitored = items.pop("monitored", False)
            self.year = items.get("year", 0)
            self.movieId = items.get("id", 0)
            self.downloaded = items.get("downloaded", False)
            self.imdbid = items.get("imdbId", 0)
            self.moviePath = items.pop("path", "")
            self.inCinemas = items.get("inCinemas", "")
            self.radarrProfileId = items.pop("profileId", 0)
            self.cleanMovieTitle = items.pop("cleanTitle", "")
            self.movieRuntime = items.pop("runtime", 0)
            self.genres = items.get("genres", "")
            self.titleslug = items.pop("titleSlug", "")
            self.isAvailable = items.pop("isAvailable", False)
            self.alternativeTitles = items.pop("alternativeTitles", [])
            self.sortTitle = items.pop("sortTitle", "")
            self.qualityProfileId = items.pop("qualityProfileId", 0)
            ep_file = items.get("movieFile") if self.hasFile else None
            if ep_file:
                self.movieFileId = ep_file.get("id", 0)
                self.movieId = ep_file.get("movieId", self.movieId)
                self.movieQuality = ep_file.pop("quality", "")
                self.relativePath = self.movie_dictionary["Movie File"] = ep_file.pop("relativePath", "")
                self.quality = self.movie_dictionary["Parsed Movie Quality"] = str(
                    (self.movieQuality.get("quality") or {}).get("name", "")
                )
                self.extension = re.sub(self.quality, "", (self.relativePath.split() or [""])[-1])
                self.mediaInfo = ep_file.pop("mediaInfo", "") or {}
                self.sizeonDisk = ep_file.pop("size", 0)
                self.audioLanguages = (self.mediaInfo or {}).get("audioLanguages", "")
            self.absolute_movie_file_path = self.movie_dictionary["Absolute Movie File Path"] = join(
                self.moviePath, self.relativePath
            ).replace(":", "-")
            g.LOG.debug(log_debug(g, "absolute movie file path", self.absolute_movie_file_path))
            g.LOG.debug(log_debug(g, "hasFile", self.hasFile))
            g.LOG.debug(log_debug(g, "monitored", self.monitored))
            g.LOG.debug(log_debug(g, "movie path", self.moviePath))
            g.LOG.debug(log_debug(g, "relative path", self.relativePath))
            g.LOG.debug(log_debug(g, "quality", self.quality))
            del g.full_radarr_dict[index]
        except (IndexError, KeyError, TypeError):
            pass


class Show(Movie, Globals):
    def __init__(self, g, series="", show_dict=None, movie_dict=None):
        super().__init__(movie_dict or {}, g)
        self.inherited_series_dict = show_dict or {}
        self.episode = self.inherited_series_dict.get("Episode")
        self.movie_dictionary = fetch_series.parent_dict(g, movie_dict or {})
        self.cleanup_input_data()
        self.absoluteEpisodeNumber = 0
        self.anime_status = False
        self.cleanTitle = ""
        self.firstAired = ""
        self.genres = []
        self.id = 0
        self.imdbId = ""
        self.languageProfileId = 0
        self.path = ""
        self.profileId = 0
        self.qualityProfileId = 0
        self.ratings = []
        self.runtime = 0
        self.seasonCount = 0
        self.seasonFolder = False
        self.seasons = []
        self.seriesId = 0
        self.seriesType = ""
        self.sortTitle = ""
        self.status = ""
        self.tags = []
        self.title = str(series)
        self.titleSlug = ""
        self.tvdbId = 0
        self.tvMazeId = 0
        self.tvRageId = 0
        self.useSceneNumbering = False
        self.year = 0
        self.absolute_episode_path = ""
        self.episode_size = 0
        self.episodeFileId = 0
        self.episodeId = 0
        self.episodeNumber = 0
        self.episodeTitle = ""
        self.hasFile = False
        self.language_dict = {}
        self.monitored = False
        self.padding = 0
        self.parsedEpisode = ""
        self.quality_dict = {}
        self.qualityCutoffNotMet = False
        self.relative_episode_path = 0
        self.relativePath = ""
        self.season = self.seasonNumber = "00"
        self.unverifiedSceneNumbering = False
        self.episode_dict = None
        self.episode_file_dict = None
        self.parsed_absolute_episode = ""
        self.parsed_episode_title = ""
        self.relative_show_file_path = ""
        self.relative_show_path = ""
        self.sceneEpisodeNumber = False
        self.sceneSeasonNumber = False
        self.episodeSize = 0
        self.qualityDict = {}
        self.relativeEpisodePath = ""

    def __repr__(self):
        return f"<Show(name={self.title!r})>"

    def initShow(self, movie, g):
        g.sonarr.get_episodes_by_series_id(self)
        self.inherited_series_dict["Episode ID"] = self.episodeId
        self.episode_dict = g.sonarr.get_episode_by_episode_id(self.episodeId)
        if self.episode_dict:
            self.absoluteEpisodeNumber = self.episode_dict.get("absoluteEpisodeNumber", "")
            self.parsed_absolute_episode = padded_absolute_episode(self, g)
        self.seasonFolder = parse_series.season_folder_from_api(self, g)
        self.relative_show_path = self.inherited_series_dict["Relative Show Path"] = parse_series.relative_show_path(
            self, g
        )
        self.episode_file_dict = g.sonarr.get_episode_file_by_episode_id(self.episodeFileId)
        self.parsed_episode_title = self.inherited_series_dict["Parsed Episode Title"] = (
            "/".join([self.path, self.seasonFolder, self.title])
            + f" - S{self.season}E{self.parsedEpisode} - {self.episodeTitle}"
        )
        self.relative_show_file_path = self.inherited_series_dict["Parsed Relative Show File Path"] = (
            f"{self.parsed_episode_title} {movie.quality + movie.extension}"
        )
        g.sonarr.rescan_series(self.seriesId)
        g.sonarr.refresh_series(self.seriesId)

    def parseEpisode(self):
        try:
            result = "-".join([str(e).zfill(self.padding) for e in self.episode])
        except TypeError:
            result = str(self.episode).zfill(self.padding) if self.episode is not None else "00"
        self.parsedEpisode = self.inherited_series_dict["Parsed Episode"] = result

    def cleanup_input_data(self):
        for key in [
            "Absolute Episode",
            "Anime",
            "Has Link",
            "Parsed Episode",
            "Parsed Episode Title",
            "Relative Show File Path",
            "Relative Show Path",
            "Show Genres",
            "Show Root Path",
            "imdbId",
            "seriesId",
            "tvdbId",
        ]:
            self.inherited_series_dict.pop(key, None)
        for key in list(self.inherited_series_dict.keys()):
            if not key:
                self.inherited_series_dict.pop(key, None)
