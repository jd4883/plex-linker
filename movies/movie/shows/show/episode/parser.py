from movies.movie.shows.show.episode import (sets, init)


def season_value_from_dictionary(movie, show):
	if not movie['Shows'][show]['Season']:
		movie['Shows'][show]['Season'] = str()
	return movie['Shows'][show]['Season']


def season_from_api(show, query, padding=2):
	init.season_value(show)
	sets.season_value(query, show)
	show['Parsed Season'] = str(show['Season']).zfill(padding)
