#!/usr/bin/env python3
from os import (chdir)
from subprocess import (Popen,
                        PIPE,
                        DEVNULL)

from messaging.frontend import (method_exit,
                                method_launch)


def symlink_force(show_class_object,
                  g):
	method_launch(g)
	# move these to a better location when the values initialize
	chdir('/media/video')
	try:
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show][
			'Relative Show File Path'] = show_class_object.relative_show_path
	except AttributeError as err:
		print(f"{g.method} had a AttributeError: {err}")  # testing
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show][
			'Relative Show File Path'] = str()
	g.movies_dictionary_object[show_class_object.movie_title][
		"Parsed Movie File"] = show_class_object.absolute_movie_file_path
	if show_class_object.absolute_movie_file_path or \
			show_class_object.relative_show_path is not \
			(None or 'None/' or \
			 show_class_object.absolute_movie_file_path.endswith('None') or \
			 show_class_object.relative_show_path.endswith('None')):
		chdir('/media/video')
		process = Popen(["ln",
		                 "-fsvr",
		                 f"{show_class_object.absolute_movie_file_path}",
		                 f"{show_class_object.relative_show_path}"],
		                stderr=DEVNULL,
		                stdout=PIPE)
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show]['Symlinked'] = \
			strip_quotes_from_string(f"{process.communicate()[0].strip()}").replace('b"', str())[:-1].rstrip()
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show][
			'Relative Show File Path'] = \
			show_class_object.relative_show_path
		g.list_of_linked_movies.append(show_class_object.movie_title)
	else:
		print(f'no link created for {show_class_object.absolute_movie_file_path}')
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show]['Symlinked'] = str()
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show][
			'Relative Show File Path'] = str()
		g.movies_dictionary_object[show_class_object.movie_title][
			"Parsed Movie File"] = str()
		g.list_of_movies_to_locate.append(show_class_object.movie_title)
	method_exit(g)


# noinspection PySameParameterValue
def strip_quotes_from_string(string):
	string.replace('"', '')
	return string.replace("'", "")
