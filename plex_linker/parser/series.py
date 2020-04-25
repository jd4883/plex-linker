import os
import re

from messaging import backend as backend
from plex_linker.fetch import series as fetch_series


def parse_series_genres(sonarr_series_dict, series_dict, g):
	series_genres = series_dict['Show Genres'] = sonarr_series_dict.get('genres', list())
	g.LOG.info(backend.debug_message(649, g, series_genres))
	return series_genres


def tvdb_id(sonarr_series_dict, series_dict, g):
	tvdb_id = series_dict['tvdbId'] = sonarr_series_dict.get('tvdbId', 0)
	g.LOG.info(backend.debug_message(618, g, tvdb_id))
	return str(tvdb_id)


def series_id(sonarr_series_dict, series_dict, show, g):
	series_id = series_dict['seriesId'] = sonarr_series_dict.get('id', g.sonarr.lookup_series(show, g).get("id", 0))
	g.LOG.info(backend.debug_message(618, g, series_id))
	return series_id


def imdb_id(sonarr_series_dict, series_dict, g):
	imdb_id = series_dict['imdbId'] = sonarr_series_dict.get('imdbId', 0)
	g.LOG.info(backend.debug_message(650, g, imdb_id))
	return imdb_id


def episode_dict_from_lookup(self, g):
	query = episode_index(self, self.sonarr_series_dict) if self.sonarr_series_dict else dict()
	g.LOG.info(backend.debug_message(626, g, query))
	return query


def root_folder(self, g):
	root_folder = f"{os.environ['SONARR_DEFAULT_ROOT']}/{self.show}"
	for item in g.sonarr_root_folders:
		item = fetch_series.show_path_string(str(item['path']))
		potential = fetch_series.show_path_string(f"{item}{self.show}/{self.season_folder}")
		if os.path.exists(potential) and os.path.isdir(potential):
			root_folder = fetch_series.show_path_string(f"{item}{self.show}")
			break
	return root_folder


def anime_status(show, g):
	show.anime_status = bool()
	series_type = show.sonarr_api_query.get("seriesType", "standard")
	if series_type.lower() == "anime".lower():
		show.anime_status = not bool()
	g.LOG.info(backend.debug_message(621, g, anime_status))


def episode_index(self, query = dict()):
	if self.sonarr_series_dict:
		e = 'episodeNumber' in query
		query = [query[x] for x in query if
		         e and (query[x]['episodeNumber'] == self.episode) and (self.season == query[x]['seasonNumber'])]
	return query


def episode_id(self, g):
	episode_id = parse_episode_id_from_series_query(g, self) if str(self.episode).isdigit() else 0
	g.LOG.info(backend.debug_message(619, g, episode_id))
	return episode_id


def parse_episode_id_from_series_query(g, show):
	base = g.sonarr.get_episodes_by_series_id(show.series_id)
	show.episode_id = 0
	for i in base:
		for k, v in i.items():
			if season(k, v):
				show.episode = str(show.inherited_series_dict["Episode"]).zfill(
					show.padding)  # = str(i["episodeNumber"])
				show.episode_id = show.inherited_series_dict["Episode ID"] = str(i["id"])
				show.episode_file_id = show.inherited_series_dict["episodeFileId"] = str(i["episodeFileId"])
				show.series_id = show.inherited_series_dict["Season"] = str(i["seasonNumber"]).zfill(2)
				break
		if show.series_id:
			break
	return show.episode_id


def season(k, v):
	return (k == "seasonNumber") and (str(v) == str(0))


def episode_padding(self, g):
	result = 3 if self.anime_status else int(os.environ['EPISODE_PADDING'])
	g.LOG.info(backend.debug_message(621, g, result))
	return result


def parse_episode_file_id_dict(self, g):
	try:
		return g.sonarr.get_episode_file_by_episode_id(self.episode_file_id)
	except TypeError:
		g.LOG.error(backend.debug_message(605, g, 0, self.episode_file_id))
		return dict()

def parse_episode_dict(self, g):
	try:
		result = g.sonarr.get_episode_by_episode_id(self.episode_id)
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

def episode_number(self, g):
	result = dict()
	try:
		result = self.inherited_series_dict[
			'Episode'] if 'Episode' in self.inherited_series_dict else self.inherited_series_dict.update(
				{ 'Episode': self.episode_dict.get('episodeNumber', str()) })
	except KeyError or AttributeError:
		pass
	g.LOG.info(backend.debug_message(622, g, result))
	return result


def absolute_episode_number(self, g):
	# need handling for multi part absolute episodes
	result = self.inherited_series_dict['Absolute Episode'] = self.episode_dict.get('absoluteEpisodeNumber', str())
	g.LOG.info(backend.debug_message(628, g, result))
	return result


def season_from_sonarr(self, g):
	result = self.inherited_series_dict['Season'] = str(self.episode_dict.get('seasonNumber', str())).zfill(2)
	g.LOG.info(backend.debug_message(630, g, result))
	return result


def season_folder_from_api(self, g):
	result = self.inherited_series_dict['Parsed Season Folder'] = f"Season {self.season}"
	g.LOG.info(backend.debug_message(631, g, result))
	return result


def show_root_folder(self, g):
	result = \
		self.inherited_series_dict['Show Root Path'] = \
		fetch_series.show_path_string(self.episode_dict.get('path',
		                                                    fetch_series.show_path_string(root_folder(self, g))))
	path = os.path.join(fetch_series.show_path_string(os.environ['DOCKER_MEDIA_PATH']), result, self.season_folder)
	os.makedirs(path, exist_ok = True)
	g.LOG.info(backend.debug_message(632, g, result))
	return result


def relative_show_path(self, g):
	result = self.inherited_series_dict['Relative Show Path'] = f"{self.show_root_path}/{self.season_folder}"
	g.LOG.info(backend.debug_message(633, g, result))
	return str(result)


def padded_episode_number(self, g, result = str()):
	if isinstance(self.episode, list):
		self.parsed_episode = "-".join([str(i).zfill(self.padding) for i in self.episode])
	elif isinstance(self.episode, int):
		self.parsed_episode = str(self.episode).zfill(self.padding)
	elif 'Parsed Absolute Episode' in self.inherited_series_dict:
		del self.inherited_series_dict['Parsed Absolute Episode']
	g.LOG.info(backend.debug_message(634, g, result))


def padded_absolute_episode(self, g):
	result = str()
	if isinstance(self.absolute_episode, list):
		result = "-".join([str(i).zfill(self.padding) for i in self.absolute_episode])
	elif isinstance(self.absolute_episode, int):
		result = str(self.absolute_episode).zfill(self.padding)
	elif 'Parsed Absolute Episode' in self.inherited_series_dict:
		del self.inherited_series_dict['Parsed Absolute Episode']
		result = str()
	elif result in [0, 00, '00', '000', None]:
		return str()
	g.LOG.info(backend.debug_message(635, g, result))
	return result


def compiled_episode_title(self, g):
	root = "/".join([self.show_root_path, self.season_folder, self.show])
	parsed_title = f"{root} - S{self.season}E{self.parsed_episode} - {self.episode_title}"
	result = self.inherited_series_dict['Parsed Episode Title'] = re.sub('\(\d+\)$', "",
	                                                                     fetch_series.show_path_string(parsed_title))
	g.LOG.info(backend.debug_message(637, g, result))
	return result

# def episode_title(show, g):
# 	show.episode_title = re.sub('\(\d+\)$', "", fetch_series.show_path_string(show.episode_dict['title']  # if 'title'
# 	# in show.episode_dict else str()))
# 	g.LOG.info(backend.debug_message(636, g, show.episode_title))
