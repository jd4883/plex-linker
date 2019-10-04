import movies.movie.shows.show.episode.parser as episode_parser
import messaging.frontend as message
import jobs.cleanup.cleanup as cleanup
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from movies.movie.movie_gets import (get_movie_path, get_relative_movie_path)
from movies.movie.shows.show.init import init_show_object
import movies.movie.shows.show.validate as validate
from movies.movie.shows.shows_validation import linking_can_be_skipped


def parse_show_to_link(show, g):
	message.method_launch(g)
	for _ in show.shows_dictionary.items():
		if validate.link_ready(show.quality):
			symlink_force(show, g)
			show.absolute_movie_path = show.movie_dictionary['Absolute Movie Path'] = str(get_movie_path(show, g))
			show.relative_movie_path = show.movie_dictionary['Relative Movie Path'] = str(get_relative_movie_path(show, g))
			set_permissions(show, g)
	message.method_exit(g)


def parse_shows_dictionary_object(movie, g):
	message.method_launch(g)
	try:
		for series in movie.shows_dictionary.keys():
			if str(type(movie.movie_dictionary['Shows'][series])) != "<class 'dict'>":
				break
			show = init_show_object(movie, str(series), g)
			try:
				if not show.show_dictionary:
					continue
			except AttributeError:
				continue
			try:
				episode_parser.sonarr_query(show.show_dictionary, show.sonarr_api_query)
			except AttributeError:
				pass
			if linking_can_be_skipped(show, movie):
				continue
			cleanup.link_properties(movie, show)
			parse_show_to_link(show, g)
	except AttributeError:
		pass

# try:
# 	for genre in tv_show.sonarr_api_query['genres']:
# 		# [g.sonarr.set_new_tag_for_sonarr({"label": str(genre).lower()}) for genre in sorted(tv_show.sonarr)]
# 		# [g.sonarr.set_new_tag_for_sonarr(str(genre).lower()) for genre in sorted(g.sonarr_genres)]
# 		# definitely need to validate_show this works as intended
# 		g.sonarr.set_series_tags({'label': str(genre).lower()},
# 		                         g.movies_dictionary_object[self.movie_title]['Shows'][self]['Show ID'])
# 		tag_id = get_tag_id(self,
# 		                    g,
# 		                    self.movie_title,
# 		                    genre)
# except AttributeError:
# 	# this should trigger if the API query is empty, seems to once in a while be the case
# 	continue


# noinspection PySameParameterValue




