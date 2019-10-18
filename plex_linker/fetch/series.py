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

# continue testing this seems right but may need more tweaks to properly handle everything
def fetch_link_status(self, episode_file_dict, relative_movie_file_path):
	try:
		root = str(os.environ['DOCKER_MEDIA_PATH'])
		os.chdir(root)
		result = bool()
		parsed_link = str()
		link = str(episode_file_dict.pop(str('path'))).replace(os.environ['SONARR_ROOT_PATH_PREFIX'],str())
		if os.path.exists(str(link).replace('../', str())):
			parsed_link = str(os.readlink(link)).replace('../', str())
		if parsed_link and (relative_movie_file_path) == parsed_link and \
			os.path.exists(self.relative_show_file_path) and \
			os.path.islink(self.relative_show_file_path):
			result = bool(True)
		return result
	except OSError as err:
		print(err)
		print(f"EPISODE FILE DICT {episode_file_dict}")
		print(f"RELATIVE MOVIE FILE PATH: {relative_movie_file_path}")
		return bool()


def title(self, g, series):
	result = series
	g.LOG.debug(backend.debug_message(604, g, result))
	return result


def parent_dict(self, g, movie_dict):
	result = movie_dict;
	g.LOG.debug(backend.debug_message(627, g, result))
	return result


def child_dict(self, g, show_dict):
	result = show_dict
	g.LOG.debug(backend.debug_message(624, g, result))
	return result
