import os
from messaging import backend as backend
from plex_linker.fetch import series as fetch_series
import re


def parse_series_genres(sonarr_series_dict, series_dict, g):
	if isinstance(sonarr_series_dict, dict):
		result = series_dict['Show Genres'] = sonarr_series_dict.pop('genres')
		g.LOG.info(backend.debug_message(649, g, result))
		return list(result)
	return list()


def tvdb_id(sonarr_series_dict, series_dict, g):
	result = 0
	if isinstance(sonarr_series_dict, dict):
		result = series_dict['tvdbId'] = sonarr_series_dict.pop('tvdbId')
	if result == 0:
		result = str()
	g.LOG.info(backend.debug_message(618, g, result))
	return str(result)


def series_id(sonarr_series_dict, series_dict, g):
	result = 0
	if isinstance(sonarr_series_dict, dict):
		if 'seriesId' in sonarr_series_dict and str(sonarr_series_dict['seriesId']).isdigit():
			result = series_dict['seriesId'] = sonarr_series_dict.pop('id')
		elif 'seriesId' in series_dict and str(series_dict['seriesId']).isdigit():
			result = series_dict['seriesId']
		else:
			print(sonarr_series_dict)
			print(series_dict)
	#	raise ValueError("SERIES ID MUST BE SET")
	if result == 0:
		raise ValueError("SERIES ID MUST BE SET")
		result = str()
	# need to readd this raise condition after dict is set, manually correct errors
	
	g.LOG.info(backend.debug_message(618, g, result))
	return result


def imdb_id(sonarr_series_dict, series_dict, g):
	if isinstance(sonarr_series_dict, dict):
		try:
			result = series_dict['imdbId'] = sonarr_series_dict.pop('imdbId')
		except KeyError:
			result = str()
		g.LOG.info(backend.debug_message(650, g, result))
		return result
	return str()


def episode_dict_from_lookup(self, g):
	query = episode_index(self, self.sonarr_series_dict) if self.sonarr_series_dict else dict()
	# series dict
	g.LOG.info(backend.debug_message(626, g, query))
	return query


def root_folder(self, g):
	# default_root = f"tv/staging/{self.show}"  # adjust to be an environ
	default_root = f"{os.environ['SONARR_DEFAULT_ROOT']}/{self.show}"
	
	for item in g.sonarr_root_folders:
		item = fetch_series.show_path_string(str(item['path']))
		potential = fetch_series.show_path_string(f"{item}{self.show}/{self.season_folder}")
		if os.path.exists(potential) and os.path.isdir(potential):
			return fetch_series.show_path_string(f"{item}{self.show}")
	return str(default_root)


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
		for item in query:
			if ('episodeNumber' in query) \
					and (query[item]['episodeNumber'] == self.episode) \
					and (self.season == query[item]['seasonNumber']):
				query = query[item]
	return query


def episode_id(self, g):
	result = self.series_dict['Episode ID'] \
		if 'Episode ID' in self.series_dict and str(self.series_dict['Episode ID']).isdigit() \
		else g.sonarr.get_episodes_by_series_id(self.series_id)
	if result == 0:
		raise ValueError("EPISODE ID MUST BE SET")
	g.LOG.info(backend.debug_message(619, g, result))
	return result


# TODO: missing logic to parse out the episode ID from what I can tell


def episode_padding(self, g):
	result = int(3) if self.anime_status else int(os.environ['EPISODE_PADDING'])
	g.LOG.debug(backend.debug_message(621, g, result))
	return result


def parse_episode_file_id_dict(self, g):
	result = dict()
	if self.episode_file_id == 0 or not self.episode_file_id:
		print("File not found should be parsing out a link")
		return result
	result = g.sonarr.get_episode_file_by_episode_id(self.episode_file_id)
	if result == 0:
		print(f"RESULT = 0 {result} {self.episode_file_id}")
		result = dict()
	g.LOG.info(backend.debug_message(652, g, result))
	return result


def parse_episode_dict(self, g):
	result = g.sonarr.get_episode_by_episode_id(self.episode_id)
	g.LOG.info(backend.debug_message(623, g, result))
	return result


def episode_file_id(self, g):
	result = self.series_dict['episodeFileId'] = self.episode_dict.pop('episodeFileId', str())
	if result == 0:
		result = self.series_dict['episodeFileId'] = str()
	# need episode file presence info for this check to work
	# raise ValueError("EPISODE FILE ID MUST BE SET")
	g.LOG.info(backend.debug_message(653, g, result))
	return result


def episode_number(self, g):
	# need handling for multi part episodes
	if 'Episode' in self.series_dict and self.series_dict['Episode'] and isinstance(self.series_dict['Episode'], list):
		result = self.series_dict['Episode']
	else:
		result = self.series_dict['Episode'] = self.episode_dict.pop('episodeNumber', str())
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
	g.LOG.info(backend.debug_message(628, g, result))
	return result


def season_from_sonarr(self, g):
	result = self.series_dict['Season'] = str(self.episode_dict.pop('seasonNumber', str())).zfill(2)
	g.LOG.info(backend.debug_message(630, g, result))
	return result


def season_folder_from_api(self, g):
	result = self.series_dict['Parsed Season Folder'] = f"Season {self.season}"
	g.LOG.info(backend.debug_message(631, g, result))
	return result


def show_root_folder(self, g):
	result = self.series_dict['Show Root Path'] = \
		fetch_series.show_path_string(self.episode_dict.pop('path', fetch_series.show_path_string(
				root_folder(self, g))))
	path = os.path.join(fetch_series.show_path_string(os.environ['DOCKER_MEDIA_PATH']), result, self.season_folder)
	os.makedirs(path, exist_ok = True)
	g.LOG.info(backend.debug_message(632, g, result))
	return result


def relative_show_path(self, g):
	result = self.series_dict['Relative Show Path'] = f"{self.show_root_path}/{self.season_folder}"
	g.LOG.info(backend.debug_message(633, g, result))
	return str(result)


def padded_episode_number(self, g):
	result = str()
	if isinstance(self.episode, list):
		items = []
		for i in self.episode:
			items.append(str(i).zfill(self.padding))
		result = "-".join(items)
	elif isinstance(self.episode, int):
		result = str(self.episode).zfill(self.padding)
	elif 'Parsed Absolute Episode' in self.series_dict:
		del self.series_dict['Parsed Absolute Episode']
		result = str()
	g.LOG.info(backend.debug_message(634, g, result))
	return result


def padded_absolute_episode(self, g):
	result = str()
	if isinstance(self.absolute_episode, list):
		items = []
		for i in self.absolute_episode:
			items.append(str(i).zfill(self.padding))
		result = "-".join(items)
	elif isinstance(self.absolute_episode, int):
		result = str(self.absolute_episode).zfill(self.padding)
	elif 'Parsed Absolute Episode' in self.series_dict:
		del self.series_dict['Parsed Absolute Episode']
		result = str()
	elif result == 0 or 00 or '00' or '000' or None:
		return str()
	g.LOG.info(backend.debug_message(635, g, result))
	return result


def compiled_episode_title(self, g):
	parsed_title = f"{self.show_root_path}/{self.season_folder}/{self.show} - S{self.season}E{self.parsed_episode} - {self.episode_title}"
	result = self.series_dict['Parsed Episode Title'] = re.sub('\(\d+\)$', "",
	                                                           fetch_series.show_path_string(parsed_title))
	g.LOG.info(backend.debug_message(637, g, result))
	return result


def episode_title(self, g, result = str()):
	# not sure why i cant pop here this was a hacky way to get around it, suspecting a datatype error
	for k, v in self.episode_dict.items():
		if k == 'title':
			result = v
			break
	else:
		self.episode_dict['title'] = str()
	result = re.sub('\(\d+\)$', "", fetch_series.show_path_string(self.episode_dict['title']))
	g.LOG.info(backend.debug_message(636, g, result))
	return result
