#!/usr/bin/env python3
import os
from os import (chdir)
from subprocess import (Popen,
                        PIPE,
                        DEVNULL)

from messaging.frontend import (method_exit,
                                method_launch)


def symlink_force(self,
                  g):
	method_launch(g)
	try:
		self.show_dictionary['Relative Show File Path'] = self.relative_show_path
	except AttributeError:
		self.show_dictionary['Relative Show File Path'] = str()
	self.movie_dictionary["Parsed Movie File"] = self.absolute_movie_file_path
	if (self.absolute_movie_file_path or self.relative_show_path) is not \
			(None or 'None/' or (self.absolute_movie_file_path.endswith('None') or self.relative_show_path.endswith('None'))):
		chdir(str(os.environ['HOST_MEDIA_PATH']))
		process = Popen(["ln", "-fsvr", f"{self.absolute_movie_file_path}", f"{self.relative_show_path}"], stderr=DEVNULL, stdout=PIPE)
		self.show_dictionary['Symlinked'] = strip_quotes_from_string(f"{process.communicate()[0].strip()}").replace('b"', str())[:-1].rstrip()
		self.show_dictionary['Relative Show File Path'] = self.relative_show_path
		g.list_of_linked_movies.append(self.movie_title)
		print(self.show_dictionary['Symlinked'])
	else:
		print(f'no link created for {self.absolute_movie_file_path}')
		self.show_dictionary['Symlinked'] = str()
		self.show_dictionary['Relative Show File Path'] = str()
		self.movie_dictionary["Parsed Movie File"] = str()
		g.list_of_movies_to_locate.append(self.movie_title)
	method_exit(g)

def strip_quotes_from_string(string):
	string.replace('"', '')
	return string.replace("'", "")
