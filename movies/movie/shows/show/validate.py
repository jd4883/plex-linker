import os


def link_ready(quality):
	if quality:
		return True
	return False


def compare_symlink_to_relpath(show):
	comparison = f"{show.show_dictionary['Relative Show File Path']} -> {os.readlink(str(show.show_dictionary['Relative Show File Path']))}"
	if str(comparison) == str(show.show_dictionary["Symlinked"]):
		return True
	return False
