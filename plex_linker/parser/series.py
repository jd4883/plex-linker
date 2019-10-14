import os

import plex_linker.sets.series as sets
from messaging import backend as backend
from plex_linker.fetch import series as fetch_series


def parse_series_genres(sonarr_series_dict, series_dict, g):
	if type(sonarr_series_dict) == dict:
		result = series_dict['Show Genres'] = sonarr_series_dict.pop('genres')
		g.LOG.debug(backend.debug_message(649, g, result))
		return list(result)
	return list()


def tvdb_id(sonarr_series_dict, series_dict, g):
	result = 0
	if type(sonarr_series_dict) == dict:
		result = series_dict['tvdbId'] = sonarr_series_dict.pop('tvdbId')
	if result == 0:
		result = str()
		#raise ValueError("TVDB ID MUST BE SET")
		# breakpoint()
	g.LOG.debug(backend.debug_message(618, g, result))
	return str(result)


def series_id(sonarr_series_dict, series_dict, g):
	result = 0
	if type(sonarr_series_dict) == dict:
		if 'seriesId' in sonarr_series_dict and str(sonarr_series_dict['seriesId']).isdigit():
			result = series_dict['seriesId'] = sonarr_series_dict.pop('id')
		elif 'seriesId' in series_dict and str(series_dict['seriesId']).isdigit():
			result = series_dict['seriesId']
		# elif 'seriesId' in series_dict and series_dict['']:
		# 	result = series_dict['seriesId'] =
		else:
			print(sonarr_series_dict)
			print(series_dict)
			raise ValueError("SERIES ID MUST BE SET")
	if result == 0:
		result = str()
		# need to readd this raise condition after dict is set, manually correct errors
		
	g.LOG.debug(backend.debug_message(618, g, result))
	return result


def imdb_id(sonarr_series_dict, series_dict, g):
	if type(sonarr_series_dict) == dict:
		try:
			result = series_dict['imdbId'] = sonarr_series_dict.pop('imdbId')
		except KeyError:
			result = str()
		g.LOG.debug(backend.debug_message(650, g, result))
		return result
	return str()


def episode_dict_from_lookup(self, g):
	query = episode_index(self, self.sonarr_series_dict) if self.sonarr_series_dict else dict()
	g.LOG.debug(backend.debug_message(626, g, query))
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
	if 'Anime' in self.series_dict and self.series_dict['Anime']:
		result = bool(self.series_dict['Anime'])
	elif 'seriesType' in self.sonarr_api_query and self.sonarr_api_query['seriesType'] == 'anime':
		result = bool(True)
	else:
		result = bool(False)
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
		else sets.set_episode_id(self, g)
	if result == 0:
		raise ValueError("EPISODE ID MUST BE SET")
	g.LOG.debug(backend.debug_message(619, g, result))
	return result


# OLD METHOD:
# 		for i in query:
# 			if int(i['seasonNumber']) == int(self.series_dict['Season']):
# 				if int(i['episodeNumber']) == int(self.series_dict['Episode'][0]):
# 					return i['id']
def episode_padding(self, g):
	result = int(3) if self.anime_status else int(os.environ['EPISODE_PADDING'])
	g.LOG.debug(backend.debug_message(621, g, result))
	return result


def parse_episode_file_id_dict(self, g):
	if self.episode_file_id == 0 or not self.episode_file_id:
		print("File not found should be parsing out a link")
		return str()
	result = g.sonarr.get_episode_file_by_episode_id(self.episode_file_id);
	if result == 0:
		result = str()
	g.LOG.debug(backend.debug_message(652, g, result))
	return result


def parse_episode_dict(self, g):
	result = g.sonarr.get_episode_by_episode_id(self.episode_id);
	g.LOG.debug(backend.debug_message(623, g, result))
	return result


def episode_file_id(self, g):
	result = self.series_dict['episodeFileId'] = self.episode_dict.pop('episodeFileId', str())
	if result == 0:
		result = self.series_dict['episodeFileId'] = str()
		# need episode file presence info for this check to work
		#raise ValueError("EPISODE FILE ID MUST BE SET")
	g.LOG.info(backend.debug_message(653, g, result))
	return result


def episode_number(self, g):
	result = self.series_dict['Episode'] \
		if 'Episode' in self.series_dict and self.series_dict['Episode'] \
		else self.episode_dict.pop('episodeNumber', str())
	g.LOG.debug(backend.debug_message(622, g, result))
	return result


def absolute_episode_number(self, g):
	result = self.series_dict['Absolute Episode'] = (self.episode_dict.pop('absoluteEpisodeNumber', str()))
	if not result and 'Absolute Episode' in self.series_dict:
		del self.series_dict['Absolute Episode']
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
	result = self.series_dict['Show Root Path'] = \
		fetch_series.show_path_string(self.episode_dict.pop('path', fetch_series.show_path_string(
				root_folder(self, g))))
	path = os.path.join(fetch_series.show_path_string(os.environ['DOCKER_MEDIA_PATH']), result, self.season_folder)
	os.makedirs(path, exist_ok = True)
	g.LOG.debug(backend.debug_message(632, g, result))
	return result


def relative_show_path(self, g):
	result = self.series_dict['Relative Show Path'] = f"{self.show_root_path}/{self.season_folder}"
	g.LOG.debug(backend.debug_message(633, g, result))
	return str(result)


def padded_episode_number(self, g):
	list = []
	if self.episode:
		for item in self.episode:
			if type(item) == "<class 'list'>":
				for i in item:
					list.append(str(i).zfill(self.padding))
			else:
				list.append(str(item).zfill(self.padding))
		result = "-".join(list)
		if result == ('00' or '000'):
			return str()
	else:
		result = str()
	
	g.LOG.info(backend.debug_message(634, g, result))
	return str(result)


def padded_absolute_episode(self, g):
	if not self.absolute_episode:
		return str()
	if 'Parsed Absolute Episode' in self.series_dict:
		del self.series_dict['Parsed Absolute Episode']
		return str()
	list = []
	for item in self.absolute_episode:
		if type(item) == "<class 'list'>":
			print(f"INNER LOOP TRIGGERED FOR LIST ITEM (item")
			for i in item:
				print(f"SUBITEM = {i}")
				list.append(str(i).zfill(self.padding))
		list.append(str(item).zfill(self.padding))
	result = "-".join(list)
	if result == ('00' or '000'):
		return str()
	g.LOG.info(backend.debug_message(635, g, result))
	return result


def parsed_show_title(self, g):
	result = self.series_dict['Parsed Show Title'] = \
		fetch_series.show_path_string(f"{self.show_root_path}/{self.season_folder}/{self.show} - S{self.season}"
		                                    f"E{self.parsed_episode} - {self.episode_title}")
	g.LOG.debug(backend.debug_message(637, g, result))
	return result


def episode_title(self, g):
	print(self.episode_dict[0])
	result = self.series_dict['Title'] = fetch_series.show_path_string(self.episode_dict.pop('title', self.series_dict['Title']))
	g.LOG.info(backend.debug_message(636, g, result))
	return result
