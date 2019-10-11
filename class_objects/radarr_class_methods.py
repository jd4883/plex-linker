#!/usr/bin/env python3
import os

from movies.movie.movie_gets import get_movie_path


def parse_relpath(self, g, media_path):
	film = get_movie_path(self, g)
	if os.path.exists(film):
		return str(os.path.relpath(film, media_path))
	return str()

#radarr_dictionary, movie, unparsed_title
def parse_movie_title(self):
	title=\
		str(self.radarr_dictionary[0].pop('title',
		                                  str(self.movie_title))).replace('((0)', '(')
	year = f"{str(self.radarr_dictionary[0].pop('year', str()))}".replace(" ()", str())
	return title + year
	#movie_title = str(self.movie_title).replace(":", "-")
	# try:
	# 	return str(self.radarr_dictionary[0].pop('title', str(self.movie_title))) + \
	# 	f"({str(self.radarr_dictionary[0].pop('year', str(0)))})".replace(" ()", str())
	#
	# 	#self.movie_title = f"{base} ({year})".replace(" ()", str()).replace(":", "-")
	# except IndexError:
	# 	pass
	# except KeyError:
	# 	pass
	# return str(self.movie_title), str(self.unparsed_title)
