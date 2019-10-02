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


def sonarr_query(show, query):
	padding = 2
	if not show['Episode']:
		show['episode'] = str()
		show['Parsed Episode'] = str()
	for item in query:
		try:
			if query[item]['episodeNumber'] == show['Episode']:
				show['Episode'] = query[item]['episodeNumber']
				show['Episode ID'] = int(query[item]['id'])
				if get_anime_status_from_api(query[item]):
					show['Anime'] = True
					padding = 3
				if query['absoluteEpisodeNumber']:
					show['Absolute Episode'] = int(query['absoluteEpisodeNumber'])
					show['Parsed Absolute Episode'] = str(show['Absolute Episode']).zfill(padding)
		except KeyError:
			continue
		except TypeError:
			continue
		show['Parsed Episode'] = str(show['Episode']).zfill(padding)
		print(f"Parsed Episode ID {show['Episode ID']} for Show")
		print(f"Episode parsed as {show['Episode']}")
		print(f"Parsed Episode {show['Parsed Episode']} for Show")
		break
