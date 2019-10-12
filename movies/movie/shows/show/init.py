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
	return show
