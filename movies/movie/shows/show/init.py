def init_show_object(movie, series, g):
	from class_objects import Show
	if not isinstance(movie.shows_dictionary[series], dict):
		return
	show = Show(g,
	            series,
	            str(movie.movie_title),
	            movie.shows_dictionary[series],
	            movie.movie_dictionary)
	return show
