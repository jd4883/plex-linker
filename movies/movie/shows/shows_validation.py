import os
from movies.movie.shows.show import validate as validate_show


def symlink_destination_exists(show):
	if os.path.exists(str(show.show_dictionary['Relative Show File Path'])):
		if os.path.islink(str(show.show_dictionary['Relative Show File Path'])):
			if os.readlink(str(show.show_dictionary['Relative Show File Path'])):
				return True
	return False


def symlink_destination_in_dictionary(movie):
	if os.path.exists(str(movie.movie_dictionary["Parsed Movie File"])) and \
			os.path.isfile(str(movie.movie_dictionary["Parsed Movie File"])):
		return True
	return False


def live_link_status(show):
	try:
		if os.readlink(str(show.show_dictionary['Relative Show File Path'])):
			return True
	except FileNotFoundError:
		pass
	return False


def link_status(movie, show):
	if live_link_status(show) and symlink_destination_exists(show):
		if symlink_destination_in_dictionary(movie):
			return True
	return False


def validate_if_linking_can_be_skipped(show, movie):
	if show.show_dictionary:
		if validate_show.compare_symlink_to_relpath(show) and link_status(movie, show):
			return True
	return False
