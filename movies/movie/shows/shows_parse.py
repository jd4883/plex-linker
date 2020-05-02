import os
import methods
from jobs.set_path_permissions import (
	set_file_mask_with_chmod_on_files_and_links,
	set_ownership_on_files_and_links,
	)
from jobs.symlinking import (symlink_force)
from messaging import frontend as message

def parse_shows_dictionary_object(movie, g):
	message.method_launch(g)
	if not movie.shows_dictionary:
		return
	for series in movie.shows_dictionary.keys():
		if not isinstance(movie.shows_dictionary[series], dict):
			continue
		show = methods.Show(g,
		                    series,
		                    movie.shows_dictionary[series],
		                    movie.movie_dictionary)
		g.sonarr.lookup_series(show)
		show.initShow(movie, g)
		map(symlink_force(movie, show, g), show.shows_dictionary.items())
		message.method_launch(g)
		directory = str(os.environ['DOCKER_MEDIA_PATH'])
		os.chdir(directory)
		try:
			set_file_mask_with_chmod_on_files_and_links(movie.absolute_movie_file_path, g)
			set_ownership_on_files_and_links(movie.absolute_movie_file_path)
		except (FileNotFoundError, NotADirectoryError, OSError):
			pass
