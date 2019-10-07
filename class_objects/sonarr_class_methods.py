import os


def season_dictionary(show):
	if ('seasons' in show.sonarr_api_query) and (show.sonarr_api_query['seasons'][0]['seasonNumber'] == int(os.environ['SEASON_INT'])):
		return show.sonarr_api_query['seasons'][0].pop('seasonNumber', str(os.environ['SEASON_STR']))
	return str(os.environ['SEASON_STR'])

def get_parsed_relative_show_title(show_dictionary):
	return show_dictionary['Parsed Relative Show Title']


