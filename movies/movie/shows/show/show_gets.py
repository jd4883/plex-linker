import messaging.frontend as message
import movies.movie.shows.show.show_puts as set_show
import movies.movie.shows.show.show_validation as validate


def get_show_root_path(show_object, g):
	if validate.show_path_presence(show_object, g):
		return True
	return False


def get_show(show_object, g):
	message.method_launch(g)
	show_object.show_paths = g.SHOWS_PATH
	set_show.set_show(show_object, g)
	message.method_exit(g)
	return show_object


def get_anime_status_from_api(show_lookup):
	if show_lookup['seriesType'] == 'anime':
		return True
	else:
		return False


def get_show_id(show, g):
	# assign at class object level and return
	message.method_launch(g)
	show_id = str()
	for index in g.shows_dictionary:
		if index['title'] == show:
			show_id = int(index['id'])
			break
	message.method_exit(g)
	return show_id


def get_tag_id(show, g, movie, tag):
	api_results = g.sonarr.get_all_tag_ids()['id']
	if not show.show_dictionary['Show Tags']:
		show.show_dictionary['Show Tags'] = list()
	if tag not in g.movies_dictionary_object[movie]['Shows'][show]['Show Tags'] and api_results[tag]:
		show.show_dictionary['Show Tags'].append(api_results[tag])
	return api_results[tag]
