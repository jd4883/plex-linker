import os
import re
import subprocess

import messaging.backend as backend
import messaging.frontend as message


def symlink_force(show, g):
	message.method_launch(g)
	os.chdir(str(os.environ['HOST_MEDIA_PATH']))
	process = subprocess.Popen(get_symlink_command_string(show), stderr = subprocess.DEVNULL,
	                           stdout = subprocess.PIPE)
	process = re.sub("'", "", str(process.communicate()[0])[3:-4])
	
	g.LOG.info(backend.debug_message(654, g, process))
	g.LOG.info(backend.debug_message(642, g, show.has_link))
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
