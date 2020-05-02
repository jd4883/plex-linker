import os
import re
import subprocess

import messaging.backend as backend
import messaging.frontend as message


def symlink_force(movie, show, g):
	message.method_launch(g)
	if movie.hasFile:
		os.chdir(str(os.environ['HOST_MEDIA_PATH']))
		process = subprocess.Popen(["ln", "-fsvr", f"{cleanString(movie.absolute_movie_file_path, movie)}",
		                            f"{cleanString(show.relative_show_file_path, movie)}"],
		                           stderr = subprocess.DEVNULL,
		                           stdout = subprocess.PIPE)
		process = re.sub("'", "", str(iter(process.communicate()).__next__())[3:-4])
		
		g.LOG.info(backend.debug_message(654, g, process))
		message.method_exit(g)

def cleanString(string, movie):
	strings_to_replace = {
			'..': '.',
			':': '-',
			}
	for k, v in strings_to_replace.items():
		string = string.replace(k, v)
	if string.startswith("/"):
		string = string[1:]
	return string
