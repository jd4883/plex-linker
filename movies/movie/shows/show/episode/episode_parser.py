#!/usr/bin/env python3
def parse_season_using_sonarr_api(show, query):
	show['Season'] = int(0) if not show['Season'] else show['Season']
	if query['seasons']:
		for item in query['seasons']:
			if item == {'monitored': True} or show[item]['seasonNumber'] == 0:
				show['Season'] = int(0)
				break
	else:
		show['Parsed Season'] = str(show['Season']).zfill(2)
