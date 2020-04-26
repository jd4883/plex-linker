from methods.class_schemas import ShowLookupSchema


#
# def build_movie_name_from_lookup(radarr_dictionary, movie_title):
# 	title = str(radarr_dictionary[0].get('title', str(movie_title)))
# 	year = re.sub(" ()", str(), str(radarr_dictionary[0].get('year', str())))
# 	return title + year


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
	print("TESTING HERE")
	lookup = iter(g.sonarr.lookup_series(show.show, g)).__next__()
	# lookup = g.sonarr.lookup_series(show.show, g)[0]
	ShowLookupSchema().load(lookup)
	ShowLookupSchema().dump(show)
	show.init_show()
