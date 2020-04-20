import os
import re

from messaging import backend as backend
from plex_linker.fetch import series as fetch_series


def parse_series_genres(sonarr_series_dict, series_dict, g):
	if isinstance(sonarr_series_dict, dict):
		try:
			result = series_dict['Show Genres'] = sonarr_series_dict.pop('genres')
			g.LOG.debug(backend.debug_message(649, g, result))
			return list(result)
		except KeyError:
			pass
	return list()


def tvdb_id(sonarr_series_dict, series_dict, g):
	result = 0
	if isinstance(sonarr_series_dict, dict):
		try:
			result = series_dict['tvdbId'] = sonarr_series_dict.pop('tvdbId')
		except KeyError:
			pass
	if not result:
		result = str()
	g.LOG.debug(backend.debug_message(618, g, result))
	return str(result)


def series_id(sonarr_series_dict, series_dict, show, g):
	result = 0
	if isinstance(sonarr_series_dict, dict):
		if 'seriesId' in sonarr_series_dict and str(sonarr_series_dict['seriesId']).isdigit():
			result = series_dict['seriesId'] = sonarr_series_dict.pop('id')
		elif 'seriesId' in series_dict and str(series_dict['seriesId']).isdigit():
			result = series_dict['seriesId']
		else:
			print(sonarr_series_dict)
			print(series_dict)
	if not result:
		result = g.sonarr.lookup_series(show, g).pop("id")
	g.LOG.debug(backend.debug_message(618, g, result))
	return result


def imdb_id(sonarr_series_dict, series_dict, g):
	if isinstance(sonarr_series_dict, dict):
		try:
			result = series_dict['imdbId'] = sonarr_series_dict.pop('imdbId')
		except KeyError:
			result = str()
		g.LOG.debug(backend.debug_message(650, g, result))
		return result
	return str()


def episode_dict_from_lookup(self, g):
	query = episode_index(self, self.sonarr_series_dict) if self.sonarr_series_dict else dict()
	# series dict
	g.LOG.debug(backend.debug_message(626, g, query))
	return query


def root_folder(self, g):
	# default_root = f"tv/staging/{self.show}"  # adjust to be an environ
	payload = f"{os.environ['SONARR_DEFAULT_ROOT']}/{self.show}"
	
	for item in g.sonarr_root_folders:
		item = fetch_series.show_path_string(str(item['path']))
		potential = fetch_series.show_path_string(f"{item}{self.show}/{self.season_folder}")
		if os.path.exists(potential) and os.path.isdir(potential):
			payload = fetch_series.show_path_string(f"{item}{self.show}")
			break
	return payload


def anime_status(self, g):
	result = self.series_dict['Anime'] = bool()
	if 'seriesType' in self.sonarr_api_query and (self.sonarr_api_query['seriesType'] != 'anime'):
		pass
	# result stays as a False
	elif 'seriesType' in self.sonarr_api_query and (self.sonarr_api_query['seriesType'] == 'anime'):
		result = self.series_dict['Anime'] = bool(True)
	g.LOG.debug(backend.debug_message(621, g, result))
	return result


def episode_index(self, query = dict()):
	if self.sonarr_series_dict:
		e = 'episodeNumber' in query
		query = [query[x] for x in query if
		         e and (query[x]['episodeNumber'] == self.episode) and (self.season == query[x]['seasonNumber'])]
	return query


def episode_id(self, g):
	if str(self.episode).isdigit():
		result = parse_episode_id_from_series_query(g, self)
	else:
		result = self.series_dict['Episode ID'] if 'Episode ID' in self.series_dict and str(
				self.series_dict['Episode ID']).isdigit() else str()
	if not result:
		print(f"COULD NOT SET EID FOR {self.show}")
	# raise ValueError("EPISODE ID MUST BE SET")
	g.LOG.debug(backend.debug_message(619, g, result))
	return result


def parse_episode_id_from_series_query(g, self):
	base = g.sonarr.get_episodes_by_series_id(self.series_id)
	for i in base:
		for k, v in i.items():
			if season(k, v):
				self.episode = str(i["episodeNumber"])
				self.episode_id = str(i["id"])
				self.episode_file_id = str(i["episodeFileId"])
				return self.episode_id


def season(k, v):
	return (k == "seasonNumber") and (str(v) == str(0))


# def episode(k, v, episode):
# 	return (k == "id") and


# TODO: missing logic to parse out the episode ID from what I can tell


def episode_padding(self, g):
	result = 3 if self.anime_status else int(os.environ['EPISODE_PADDING'])
	g.LOG.debug(backend.debug_message(621, g, result))
	return result


def parse_episode_file_id_dict(self, g, payload = dict()):
	# if not (self.episode_file_id or self.episode_file_id):
	# 	g.LOG.info(backend.debug_message(603, g, self.movie_title, self.show))
	# 	return payload
	payload = g.sonarr.get_episode_file_by_episode_id(self.episode_file_id)
	if not payload:
		g.LOG.error(backend.debug_message(605, g, payload, self.episode_file_id))
		payload = dict()
	g.LOG.debug(backend.debug_message(652, g, payload))
	return payload


def parse_episode_dict(self, g):
	try:
		result = g.sonarr.get_episode_by_episode_id(self.episode_id)
		g.LOG.debug(backend.debug_message(623, g, result))
	except KeyError or AttributeError:
		result = dict()
	return result


def episode_file_id(self, g):
	result = self.series_dict['episodeFileId'] = self.episode_dict.pop('episodeFileId', str())
	if not result:
		result = self.series_dict['episodeFileId'] = str()
	g.LOG.debug(backend.debug_message(653, g, result))
	return result

def episode_number(self, g):
	result = dict()
	try:
		result = self.series_dict['Episode'] parse_episode_id_from_series_query() 'Episode' int self.series_dict else self.series_dict.update({ 'Episode': self.episode_dict.pop('episodeNumber', str()) })
	except KeyError or AttributeError:
		pass
	g.LOG.debug(backend.debug_message(622, g, result))
	return result


def absolute_episode_number(self, g):
	# need handling for multi part absolute episodes
	if 'Absolute Episode' not in self.series_dict:
		self.series_dict['Absolute Episode'] = str()
	if 'Absolute Episode' in self.series_dict and not self.series_dict['Absolute Episode']:
		result = self.series_dict['Absolute Episode'] = str()
	elif self.series_dict['Absolute Episode'] and isinstance(self.series_dict['Absolute Episode'], list):
		result = self.series_dict['Absolute Episode']
	else:
		result = self.series_dict['Absolute Episode'] = self.episode_dict.pop('absoluteEpisodeNumber', str())
	g.LOG.debug(backend.debug_message(628, g, result))
	return result


def season_from_sonarr(self, g):
	result = self.series_dict['Season'] = str(self.episode_dict.pop('seasonNumber', str())).zfill(2)
	g.LOG.debug(backend.debug_message(630, g, result))
	return result


def season_folder_from_api(self, g):
	result = self.series_dict['Parsed Season Folder'] = f"Season {self.season}"
	g.LOG.debug(backend.debug_message(631, g, result))
	return result


def show_root_folder(self, g):
	result = \
		self.series_dict['Show Root Path'] = \
		fetch_series.show_path_string(self.episode_dict.pop('path',
		                                                    fetch_series.show_path_string(root_folder(self, g))))
	path = os.path.join(fetch_series.show_path_string(os.environ['DOCKER_MEDIA_PATH']), result, self.season_folder)
	os.makedirs(path, exist_ok = True)
	g.LOG.debug(backend.debug_message(632, g, result))
	return result


def relative_show_path(self, g):
	result = self.series_dict['Relative Show Path'] = f"{self.show_root_path}/{self.season_folder}"
	g.LOG.debug(backend.debug_message(633, g, result))
	return str(result)


def padded_episode_number(self, g, result = str()):
	if isinstance(self.episode, list):
		result = "-".join([str(i).zfill(self.padding) for i in self.episode])
	elif isinstance(self.episode, int):
		result = str(self.episode).zfill(self.padding)
	elif 'Parsed Absolute Episode' in self.series_dict:
		del self.series_dict['Parsed Absolute Episode']
	g.LOG.debug(backend.debug_message(634, g, result))
	return result


def padded_absolute_episode(self, g):
	result = str()
	if isinstance(self.absolute_episode, list):
		result = "-".join([str(i).zfill(self.padding) for i in self.absolute_episode])
	elif isinstance(self.absolute_episode, int):
		result = str(self.absolute_episode).zfill(self.padding)
	elif 'Parsed Absolute Episode' in self.series_dict:
		del self.series_dict['Parsed Absolute Episode']
		result = str()
	elif result in [0, 00, '00', '000', None]:
		return str()
	g.LOG.debug(backend.debug_message(635, g, result))
	return result


def compiled_episode_title(self, g):
	root = "/".join([self.show_root_path, self.season_folder, self.show])
	parsed_title = f"{root} - S{self.season}E{self.parsed_episode} - {self.episode_title}"
	result = self.series_dict['Parsed Episode Title'] = re.sub('\(\d+\)$', "",
	                                                           fetch_series.show_path_string(parsed_title))
	g.LOG.debug(backend.debug_message(637, g, result))
	return result


def episode_title(self, g):
	payload = fetch_series.show_path_string(self.episode_dict['title'] if 'title' in self.episode_dict else str())
	result = re.sub('\(\d+\)$', "", payload)
	g.LOG.debug(backend.debug_message(636, g, result))
	return result
