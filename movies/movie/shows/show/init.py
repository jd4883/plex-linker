def init_show_object(movie, series, g):
	from class_objects import Show
	if str(type(movie.shows_dictionary[series])) != "<class 'dict'>":
		return
	show = Show(g,
	            series,
	            str(movie.movie_title),
	            movie.movie_dictionary,
	            movie.movie_dictionary['Shows'][series],
	            g.sonarr.lookup_series(series))
	try:
		show.raw_episodes = g.sonarr.get_episodes_by_series_id(show.show_dictionary['Show ID'])
		show.raw_episode_files = g.sonarr.get_episode_files_by_series_id(show.show_dictionary['Show ID'])
	except KeyError:
		pass
	return show
