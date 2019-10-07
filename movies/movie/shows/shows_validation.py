import os
from movies.movie.shows.show import validate as validate_show

def symlink_destination_exists(show):
	if os.path.exists(str(show.relative_show_path)):
		if os.path.islink(str(show.relative_show_path)):
			return True
	return False

def symlink_destination_in_dictionary(movie):
	# this calculation should be much further up but i'll move it later
	movie.relative_movie_file_path = "/".join((movie.relative_movie_file_path, movie.movie_file))
	if os.path.exists(movie.relative_movie_file_path) and os.path.isfile(movie.relative_movie_file_path):
		return True
	return False

def live_link_status(show, g):
	os.chdir(str(os.environ['DOCKER_MEDIA_PATH']))
	try:
		if not os.path.isdir(str(show.relative_show_path)) and os.readlink(str(show.relative_show_path)):
			return True
	except FileNotFoundError:
		pass
	except OSError:
		pass
	return False

def link_status(movie, show, g):
	if live_link_status(show, g):
		if symlink_destination_exists(show):
			if symlink_destination_in_dictionary(movie):
				return True
	return False

def linking_can_be_skipped(show, movie, g):
	if show.show_dictionary:
		if link_status(movie, show, g):
			if validate_show.compare_symlink_to_relpath(show):
				return True
	return False
