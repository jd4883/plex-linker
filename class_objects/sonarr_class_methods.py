#!/usr/bin/env python3
import os
from os import environ

from movies.movie.shows.show.get import get_anime_status_from_api


def sonarr_query(show, query, padding):
	for item in query:
		if 'episodeNumber' in query[item]:
			if query[item]['episodeNumber'] == show['Episode']:
				show['Episode'] = query[item]['episodeNumber']
				show['Episode ID'] = int(query[item]['id'])
				show.padding = set_show_type_anime(item, show.padding, query, show)
				if query['absoluteEpisodeNumber']:
					return str(int(query['absoluteEpisodeNumber'])).zfill(show.padding)
		show['Parsed Episode'] = str(show['Episode']).zfill(padding)
		break


def set_show_type_anime(item, padding, query, show):
	show['Anime'] = False
	if get_anime_status_from_api(query[item]):
		show['Anime'] = True
		padding = 3
	return padding


def season_dictionary(show):
	if ('seasons' in show.sonarr_api_query) and (show.sonarr_api_query['seasons'][0]['seasonNumber'] == int(os.environ['SEASON_INT'])):
		return show.sonarr_api_query['seasons'][0].pop('seasonNumber', str(os.environ['SEASON_STR']))
	return str(os.environ['SEASON_STR'])


def get_parsed_relative_show_title(show_dictionary):
	return show_dictionary['Parsed Relative Show Title']


def get_relative_show_path(show_dictionary):
	return show_dictionary['Relative Show File Path']


def get_parsed_show_title(show_dictionary):
	return show_dictionary['Parsed Show Title']


def set_root_path(sonarr_api_query):
	prefix = str(environ['SONARR_ROOT_PATH_PREFIX'])
	return str(sonarr_api_query.pop('path', '')).replace(prefix, str())
