#!/usr/bin/env python3
import os

from messaging import backend as backend


def symlink_status(self, g):
	result = str(self.series_dict['Symlinked']) \
		if ('Symlinked' in self.series_dict) and self.series_dict['Symlinked'] \
		else str()
	g.LOG.debug(backend.debug_message(651, g, result))
	return result


def show_path_string(string):
	return str((str(string).replace('//', '/')).replace(":", "")).replace(str(os.environ['SONARR_ROOT_PATH_PREFIX']),
	                                                                      str())


def fetch_link_status(self, episode_file_dict, relative_movie_file_path):
	result = bool()
	try:
		link = str(episode_file_dict.pop(str('path'))).replace(os.environ['SONARR_ROOT_PATH_PREFIX'],str())
	except AttributeError:
		return bool()
	parsed_link = str(os.readlink(link)).replace('../', str())
	if str(relative_movie_file_path) == parsed_link:
		result = os.path.islink(link)
	return result