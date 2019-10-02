import os
from movies.movie.shows.show import validate as validate_show

# confirmed working
def symlink_destination_exists(show):
	if os.path.exists(str(show.show_dictionary['Relative Show File Path'])):
		if os.path.islink(str(show.show_dictionary['Relative Show File Path'])):
			if os.readlink(str(show.show_dictionary['Relative Show File Path'])):
				return True
	return False


def symlink_destination_in_dictionary(movie):
	# problems in here because we are looking at the exact file but need the full path
	print(f'SYMLINK DESTINATION IN DICT METHOD: {str(movie.movie_dictionary["Parsed Movie File"])}')
	if os.path.exists(str(movie.movie_dictionary["Parsed Movie File"])):
		print('FIRST IF TRIGGERED')
		if os.path.isfile(str(movie.movie_dictionary["Parsed Movie File"])):
			print("LINK DEST IN DICT TRIGGERED")
			return True
	return False

# confirmed working
def live_link_status(show):
	try:
		if os.readlink(str(show.show_dictionary['Relative Show File Path'])):
			return True
	except FileNotFoundError:
		pass
	return False


def link_status(movie, show):
	if live_link_status(show):
		if symlink_destination_exists(show):
			if symlink_destination_in_dictionary(movie):
				print("LINK IN DICT")
				return True
	return False


def linking_can_be_skipped(show, movie):
	if show.show_dictionary:
		if link_status(movie, show):
			print('SECOND IF TRIGGERED')
			if validate_show.compare_symlink_to_relpath(show):
				print(f'INNER IF TRIGGERED')
				return True
	return False
