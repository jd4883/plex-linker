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
