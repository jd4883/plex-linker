import re

from messaging import backend as backend
from plex_linker.fetch import series as fetch_series


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
