def parse_season_using_sonarr_api(show, query, padding = 2, season_default = 0):
	show['Season'] = int(season_default) if not show['Season'] else show['Season']
	try:
		for item in query['seasons']:
			if item == {'monitored': True} or show[item]['seasonNumber'] == season_default:
				show['Season'] = int(season_default)
				break
	except AttributeError:
		pass
	show['Parsed Season'] = str(show['Season']).zfill(padding)
