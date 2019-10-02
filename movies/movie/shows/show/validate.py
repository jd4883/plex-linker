def link_ready(quality):
	if quality:
		return True
	return False


def compare_symlink_to_relpath(show):
	if f'{str(show.show_dictionary["Relative Show File Path"]).lower()}' == \
			show.show_dictionary["Symlinked"].lower():
		return True
	return False
