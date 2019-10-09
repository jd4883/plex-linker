import os
import subprocess

import messaging.frontend as message
import messaging.backend as backend

def symlink_force(show, g):
	message.method_launch(g)
	if (show.absolute_movie_file_path or show.absolute_movie_file_path) == ("/'" or "" or None or "/"):
		# really primitive way to indicate if the movie value is blank we do not link
		pass
	elif validate_link_ready(show):
		os.chdir(str(os.environ['HOST_MEDIA_PATH']))
		# noinspection SpellCheckingInspection
		process = subprocess.Popen(get_symlink_command_string(show), stderr = subprocess.DEVNULL,
		                           stdout = subprocess.PIPE)
		show.link_status = strip_quotes_from_string(get_symlink_string(process)).replace('b"', str())[:-3].rstrip()
		# -3 covers the link not having the newline character at the end, if this is fixed this should be -1 instead
		if show.link_status:
			g.LOG.info(backend.debug_message(642, g, show.link_status))
	else:
		print(f'no link created for {show.absolute_movie_file_path}')
		show.link_status = str()
		show.relative_show_path = str()
		show.movie_file = str()
		g.list_of_movies_to_locate.append(show.movie_title)
	message.method_exit(g)


def get_symlink_command_string(show):
	return ["ln", "-fsvr", f"{show.absolute_movie_file_path}", f"{show.relative_show_path}"]


def get_symlink_string(process):
	return strip_quotes_from_string(str(process.communicate()[0])).strip()


# cleanup this method along with others and try to segment where they are stored
def validate_link_ready(show):
	if (show.absolute_movie_file_path and show.relative_show_path) is not (None or 'None/' or (
			show.absolute_movie_file_path.endswith('None') or show.relative_show_path.endswith('None'))):
		return True
	return False


def strip_quotes_from_string(string):
	string.replace('"', '')
	string.replace('\n', '')
	return string.replace("'", "")
