#!/usr/bin/env python3
import os
import re

from messaging import backend as backend


def symlink_status(self, g, result = str()):
	if ('Symlinked' in self.series_dict) and self.series_dict['Symlinked']:
		result = str(self.series_dict['Symlinked'])
		g.LOG.info(backend.debug_message(651, g, result))
	return result


def show_path_string(string):
	result = re.sub('//', '/', string)
	result = re.sub(str(os.environ['SONARR_ROOT_PATH_PREFIX']), str(), result)
	result = re.sub(':', str(), result)
	return result


# continue testing this seems right but may need more tweaks to properly handle everything
def fetch_link_status(self, episode_file_dict, relative_movie_file_path):
	try:
		root = str(os.environ['DOCKER_MEDIA_PATH'])
		os.chdir(root)
		result = bool()
		parsed_link = str()
		path = str(episode_file_dict.pop('path')) if 'path' in episode_file_dict else str()
		prefix = str(os.environ['SONARR_ROOT_PATH_PREFIX'])
		link = re.sub(prefix, str(), path)
		if os.path.exists(re.sub('../', str(), str(link))):
			parsed_link = re.sub('../', str(), str(os.readlink(link)))
		if parsed_link and relative_movie_file_path == parsed_link and \
				os.path.exists(self.relative_show_file_path) and \
				os.path.islink(self.relative_show_file_path):
			result = bool(True)
		return result
	except OSError as err:
		print(err)
		print(f"EPISODE FILE DICT {episode_file_dict}")
		print(f"RELATIVE MOVIE FILE PATH: {relative_movie_file_path}")
		return bool()


def title(g, series):
	result = series
	g.LOG.debug(backend.debug_message(604, g, result))
	return result


def parent_dict(g, movie_dict):
	result = movie_dict
	g.LOG.debug(backend.debug_message(627, g, result))
	return result


def child_dict(g, show_dict):
	result = show_dict
	g.LOG.debug(backend.debug_message(624, g, result))
	return result
