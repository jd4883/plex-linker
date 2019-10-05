from movies.movie.shows.show.episode import (sets, init)
from movies.movie.shows.show.get import get_anime_status_from_api


def season_value_from_dictionary(movie, show):
	if not movie['Shows'][show]['Season']:
		movie['Shows'][show]['Season'] = str()
	return movie['Shows'][show]['Season']


def season_from_api(show, query, padding=2):
	init.season_value(show)
	sets.season_value(query, show)
	show['Parsed Season'] = str(show['Season']).zfill(padding)


def sonarr_query(show, query, padding):
	if 'Episode' not in show:
		show['episode'] = str()
		show['Parsed Episode'] = str()
	for item in query:
		if 'episodeNumber' in query[item]:
			set_episode_from_sonarr_api(item, query, show)
		show['Parsed Episode'] = str(show['Episode']).zfill(padding)
		break


def set_episode_from_sonarr_api(item, query, show):
	if query[item]['episodeNumber'] == show['Episode']:
		show['Episode'] = query[item]['episodeNumber']
		show['Episode ID'] = int(query[item]['id'])
		show.padding = set_show_type_anime(item, show.padding, query, show)
		set_show_absolute_episode(show.padding, query, show)


def set_show_absolute_episode(padding, query, show):
	if query['absoluteEpisodeNumber']:
		show['Absolute Episode'] = int(query['absoluteEpisodeNumber'])
		show['Parsed Absolute Episode'] = str(show['Absolute Episode']).zfill(padding)


def set_show_type_anime(item, padding, query, show):
	if get_anime_status_from_api(query[item]):
		show['Anime'] = True
		padding = 3
	return padding
