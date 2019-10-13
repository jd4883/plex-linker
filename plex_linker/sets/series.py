#!/usr/bin/env python3
from messaging import backend as backend
from plex_linker.parser.path import parse_relative_episode_file_path
from plex_linker.parser.series import episode_id


def set_relative_show_path(self, g):
	path = self.series_dict['Relative Show File Path'] \
		if self.series_dict \
		else self.show_path_string(parse_relative_episode_file_path(self, self.episode_dict))
	if (not path) or (path == (None or str(None) or str())):
		return str()
	g.LOG.debug(backend.debug_message(633, g, path))
	return path


def set_episode_id(self, g):
	return self.series_dict['Episode ID'] \
		if 'Episode ID' in self.series_dict \
		else str(episode_id(self, g.sonarr.get_episodes_by_series_id(int(self.tvdbId))))
