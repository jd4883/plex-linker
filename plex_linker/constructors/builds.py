def init_show_object(movie, series, g):
	from methods import Show
	if not isinstance(movie.shows_dictionary[series], dict):
		return
	show = Show(g,
	            series,
	            movie.shows_dictionary[series],
	            movie.movie_dictionary)
	init_show(show, g)
	return show


def init_show(show, g):
	g.sonarr.lookup_series(show, g)
	# result = ShowLookupSchema(many = False, partial = True).load(lookup)
	# TODO: fairly sure this is just shy of working, but I got lazy and did it a bit more manually
	show.init(g)
