import os


def link_ready(quality):
	if quality:
		return True
	return False


def compare_symlink_to_relpath(show):
	show.show_dictionary["Symlinked"] = str()
	return False
	# testing so that the condition never succeeds was getting non-linked reported as still linked
	# may be a logic issue here
	comparison = f"{show.relative_show_path} -> {os.readlink(show.relative_show_path)}"
	if str(comparison) == str(show.show_dictionary["Symlinked"]):
		return True
	return False
