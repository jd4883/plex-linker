import os


def season_value(show, season=int(os.environ['SEASON_INT'])):
	show['Season'] = int(season) if not show['Season'] else show['Season']
