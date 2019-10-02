import movies.movie.shows.show.get as get

def anime_status(self):
	if not self.show_dictionary['Anime']:
		self.show_dictionary['Anime'] = False


def init_show_object(movie, series, g):
	from class_objects import Show
	if str(type(movie.movie_dictionary['Shows'][series])) != "<class 'dict'>":
		# this handles any show with a value of None for the key value pair
		return
	show = Show(g,
	            series,
	            str(movie.movie_dictionary['Unparsed Movie Title']),
	            dict(movie.movie_dictionary),
	            dict(movie.movie_dictionary['Shows'][series]),
	            g.sonarr.lookup_series(series))
	print(g.sonarr.lookup_series)
	exit(-1)
	get.get_show(show, g)
	try:
		show.raw_episodes = g.sonarr.get_episodes_by_series_id(show.show_dictionary['Show ID'])
		show.raw_episode_files = g.sonarr.get_episode_files_by_series_id(show.show_dictionary['Show ID'])
	except KeyError as err:
		print(f"Error grabbing raw episode data from sonarr due to {err}")
	return show
