import os

from movies.movie.shows.show.episode import validate


def season_value(query, show, season_default=int(os.environ['SEASON_INT'])):
	try:
		for item in query['seasons']:
			if validate.season_value(item, season_default, show):
				show['Season'] = int(season_default)
				break
	except AttributeError:
		pass
	except KeyError:
		pass
