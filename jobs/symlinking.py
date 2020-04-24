import os
import re
import subprocess

import messaging.backend as backend
import messaging.frontend as message


def symlink_force(show, g):
	message.method_launch(g)
	# TODO: add method to handle deleting dead links and files instead of links
	if (show.absolute_movie_path or show.absolute_movie_file_path) in ["/'", str(), None, "/"] \
			or str(show.absolute_movie_path or show.absolute_movie_file_path).endswith("/'" or "" or None or "/") or \
			not show.episode:
		# really primitive way to indicate if the movie value is blank we do not link
		# also checks if the episode is unset
		show.absolute_movie_file_path = str()
		show.has_link = bool()
	if not show.has_link:
		os.chdir(str(os.environ['HOST_MEDIA_PATH']))
		# noinspection SpellCheckingInspection
		process = subprocess.Popen(get_symlink_command_string(show), stderr = subprocess.DEVNULL,
		                           stdout = subprocess.PIPE)
		process = re.sub("'", "", str(process.communicate()[0])[3:-4])
		
		# may be an error may be because relative pathing but the output is pretty useless here for 654
		g.LOG.info(backend.debug_message(654, g, process))
		g.LOG.info(backend.debug_message(642, g, show.has_link))
	else:
		print(f'Link not created for {show.absolute_movie_file_path}')
		show.link_status = str()
		show.relative_show_path = str()
		show.movie_file = str()
	message.method_exit(g)


def get_symlink_command_string(show):
	return ["ln", "-fsvr", f"{show.absolute_movie_file_path}", f"{show.relative_show_file_path}"]


# # cleanup this method along with others and try to segment where they are stored
# def validate_link_ready(show):
# 	if (show.absolute_movie_file_path and show.relative_show_path) is not (None or 'None/' or (
# 			show.absolute_movie_file_path.endswith('None') or show.relative_show_path.endswith('None'))):
# 		return True
# 	return False


# def strip_quotes_from_string(string):
# 	return re.sub("['\"\n]", str(), string)
