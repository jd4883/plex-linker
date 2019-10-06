def get_anime_status_from_api(show_lookup):
	if show_lookup['seriesType'] == 'anime':
		return True
	else:
		return False


# noinspection PyUnusedFunction
def get_tag_id(show, g, movie, tag):
	api_results = g.sonarr.get_all_tag_ids()['id']
	if not show.show_dictionary['Show Tags']:
		show.show_dictionary['Show Tags'] = list()
	if tag not in g.movies_dictionary_object[movie]['Shows'][show]['Show Tags'] and api_results[tag]:
		show.show_dictionary['Show Tags'].append(api_results[tag])
	return api_results[tag]
