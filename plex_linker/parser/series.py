import os
import re
from pprint import pprint

from marshmallow import fields, Schema

from messaging import backend as backend
from plex_linker.fetch import series as fetch_series


def episode_dict_from_lookup(self, g):
	# TODO: should get a new API call here instead of series_dict
	query = episode_index(self, self.sonarr_series_dict)
	g.LOG.info(backend.debug_message(626, g, query))
	return query


def root_folder(self, g):
	folder_root = f"{os.environ['SONARR_DEFAULT_ROOT']}/{self.title}"
	for item in g.sonarr_root_folders:
		item = fetch_series.show_path_string(str(item['path']))
		potential = fetch_series.show_path_string(f"{item}{self.title}/{self.seasonFolder}")
		if os.path.exists(potential) and os.path.isdir(potential):
			folder_root = fetch_series.show_path_string(f"{item}{self.title}")
			break
	return folder_root


def episode_index(self, query = dict()):
	if self.sonarr_series_dict:
		e = 'episodeNumber' in query
		query = [query[x] for x in query if
		         e and (query[x]['episodeNumber'] == self.episode) and (self.season == query[x]['seasonNumber'])]
	return query


def episode_id(self, g):
	sonarr_episode_id = parse_episode_id_from_series_query(g, self)
	g.LOG.info(backend.debug_message(619, g, sonarr_episode_id))
	return sonarr_episode_id


def parse_episode_id_from_series_query(g, show):
	print(show.id)
	print(show.seriesId)
	base = g.sonarr.get_episodes_by_series_id(show.seriesId)
	pprint(base)
	
	breakpoint()
	episode_dict = None
	if not base:
		return str()
	for i in base:
		try:
			for k, v in base[i].items():
				if season(k, v):
					# TODO: maybe try this each time and check the parsed out values?
					pprint(EpisodeBySeriesIdSchema().load(i, id = show.episode_id))
					breakpoint()
					show.episode = str(show.inherited_series_dict["Episode"]).zfill(
							show.padding)
					show.episode_id = show.inherited_series_dict["Episode ID"] = str(i["id"])
					show.episodeFileId = show.inherited_series_dict["episodeFileId"] = str(i["episodeFileId"])
					show.season = show.inherited_series_dict["Season"] = str(i["seasonNumber"]).zfill(2)
					break
			break
		except AttributeError:
			pass
	return show.episode_id


def season(k, v):
	return (k == "seasonNumber") and (str(v) == str(0))


def parse_episode_file_id_dict(self, g):
	try:
		return g.sonarr.get_episode_file_by_episode_id(self.episodeFileId)
	except TypeError:
		g.LOG.error(backend.debug_message(605, g, 0, self.episodeFileId))
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


def absolute_episode_number(self, g):
	# need handling for multi part absolute episodes
	result = self.inherited_series_dict['Absolute Episode'] = self.episode_dict.get('absoluteEpisodeNumber', str())
	g.LOG.info(backend.debug_message(628, g, result))
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
	path = os.path.join(fetch_series.show_path_string(os.environ['DOCKER_MEDIA_PATH']), result, self.seasonFolder)
	os.makedirs(path, exist_ok = True)
	g.LOG.debug(backend.debug_message(632, g, result))
	return result


def relative_show_path(self, g):
	result = self.inherited_series_dict['Relative Show Path'] = f"{self.show_root_path}/{self.seasonFolder}"
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
	root = "/".join([self.show_root_path, self.seasonFolder, self.title])
	parsed_title = f"{root} - S{self.season}E{self.parsed_episode} - {self.episode_title}"
	result = self.inherited_series_dict['Parsed Episode Title'] = re.sub('\(\d+\)$', "",
	                                                                     fetch_series.show_path_string(parsed_title))
	g.LOG.info(backend.debug_message(637, g, result))
	return result

# def episode_title(show, g):
# 	show.episode_title = re.sub('\(\d+\)$', "", fetch_series.show_path_string(show.episode_dict['title']  # if 'title'
# 	# in show.episode_dict else str()))
# 	g.LOG.info(backend.debug_message(636, g, show.episode_title))
class EpisodeBySeriesIdSchema(Schema):
	def __init__(self):
		seriesId = fields.Int()
		episodeFileId = fields.Int()
		seasonNumber = fields.Int()
		episodeNumber = fields.Int()
		title = fields.Str()
		airDate = fields.DateTime()
		airDateUtc = fields.DateTime()
		overview = fields.Str()
		hasFile = fields.Bool()
		monitored = fields.Bool()
		sceneEpisodeNumber = fields.Int()
		sceneSeasonNumber = fields.Int()
		tvDbEpisodeId = fields.Int()
		absoluteEpisodeNumber = fields.Int()
		id = fields.Int()
