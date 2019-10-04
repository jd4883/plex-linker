import os


def season_value(item, show, season_default=int(os.environ['SEASON_INT'])):
	if item == {'monitored': True} or show[item]['seasonNumber'] == season_default:
		return True
	return False


def parsed_season_value(self, season=int(os.environ['SEASON_INT'])):
	if (self.show_dictionary['Season'] == int(season)) or str(self.show_dictionary['Season']).isdigit():
		return True
	return False
