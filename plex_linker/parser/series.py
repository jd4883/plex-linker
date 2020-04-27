import os
import re

from messaging import backend as backend
from plex_linker.fetch import series as fetch_series


def root_folder(self, g):
	folder_root = f"{os.environ['SONARR_DEFAULT_ROOT']}/{self.title}"
	for item in g.sonarr_root_folders:
		item = fetch_series.show_path_string(str(item['path']))
		potential = fetch_series.show_path_string(f"{item}{self.title}/{self.seasonFolder}")
		if os.path.exists(potential) and os.path.isdir(potential):
			folder_root = fetch_series.show_path_string(f"{item}{self.title}")
			break
	return folder_root


def parse_episode_file_id_dict(self, g):
	try:
		return g.sonarr.get_episode_file_by_episode_id(self.episodeFileId)
	except TypeError:
		g.LOG.error(backend.debug_message(605, g, 0, self.episodeFileId))
		return dict()


def parse_episode_dict(self, g):
	try:
		result = g.sonarr.get_episode_by_episode_id(self.episodeId)
		g.LOG.info(backend.debug_message(623, g, result))
	except KeyError or AttributeError:
		result = dict()
	return result


def episode_file_id(self, g):
	result = self.inherited_series_dict['episodeFileId'] = self.episode_dict.get('episodeFileId', str())
	if not result:
		result = self.inherited_series_dict['episodeFileId'] = str()
	g.LOG.info(backend.debug_message(653, g, result))
	return result


def absolute_episode_number(self, g):
	# need handling for multi part absolute episodes
	result = self.inherited_series_dict['Absolute Episode'] = self.episode_dict.get('absoluteEpisodeNumber', str())
	g.LOG.info(backend.debug_message(628, g, result))
	return result


def season_folder_from_api(self, g):
	result = self.inherited_series_dict['Parsed Season Folder'] = f"Season {self.season}"
	g.LOG.info(backend.debug_message(631, g, result))
	return result


def relative_show_path(self, g):
	result = self.inherited_series_dict['Relative Show Path'] = f"{self.path}/{self.seasonFolder}"
	g.LOG.debug(backend.debug_message(633, g, result))
	return str(result)


def padded_episode_number(self, g, result = str()):
	if str(self.episode) == "<class 'list'>":
		self.parsed_episode = "-".join([str(i).zfill(self.padding) for i in self.episode])
	elif str(self.episode) == "<class 'int'>":
		self.parsed_episode = str(self.episode).zfill(self.padding)
	g.LOG.info(backend.debug_message(634, g, result))


def padded_absolute_episode(self, g):
	result = str()
	if isinstance(self.absoluteEpisodeNumber, list):
		result = "-".join([str(i).zfill(self.padding) for i in self.absoluteEpisodeNumber])
	elif isinstance(self.absoluteEpisodeNumber, int):
		result = str(self.absoluteEpisodeNumber).zfill(self.padding)
	elif 'Parsed Absolute Episode' in self.inherited_series_dict:
		del self.inherited_series_dict['Parsed Absolute Episode']
		result = str()
	elif result in [0, 00, '00', '000', None]:
		return str()
	g.LOG.info(backend.debug_message(635, g, result))
	return result


def compiled_episode_title(self, g):
	parsed_title = '/'.join([self.path, self.seasonFolder, self.title]) \
	               + " - S" \
	               + self.season \
	               + "E" \
	               + self.parsed_episode \
	               + " - " \
	               + self.episodeTitle
	result = self.inherited_series_dict['Parsed Episode Title'] = re.sub('\(\d+\)$', "",
	                                                                     fetch_series.show_path_string(parsed_title))
	g.LOG.info(backend.debug_message(637, g, result))
	return result
