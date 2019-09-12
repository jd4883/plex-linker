#!/usr/bin/env python3

from subprocess import (Popen,
                        DEVNULL,
                        PIPE)
from messaging.frontend import (method_exit,
                                method_launch)


def symlink_force(show_class_object,
                  g):
	method_launch(g)
	# move these to a better location when the values initialize
	g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show][
		'Relative Show File Path'] = show_class_object.relative_show_path
	g.movies_dictionary_object[show_class_object.movie_title][
		"Parsed Movie File"] = show_class_object.absolute_movie_file_path
	print(g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show][
		      'Relative Show File Path'])
	print(g.movies_dictionary_object[show_class_object.movie_title]["Parsed Movie File"].replace('/var/data/media/video',
	                                                                                             '/media'))
	if ((str(show_class_object.absolute_movie_file_path).replace('/var/data/media/video',
	                                                             '/media') or show_class_object.absolute_movie_file_path) or
	    show_class_object.relative_show_path) \
			is not (None or 'None/'
			        or show_class_object.absolute_movie_file_path.endswith('None')
			        or show_class_object.relative_show_path.endswith('None')):
		method_launch(g)
		# added the popen for relative symlinking because this was not working in the os symlink built in.
		# have not done any testing in Windows only on Ubuntu 18
		if str(show_class_object.absolute_movie_file_path).startswith('/media'):
			show_class_object.absolute_movie_file_path = \
				str(show_class_object.absolute_movie_file_path).replace('/media',
				                                                        '/var/data/media/video')
		process = Popen(["ln",
		                 "-fsvr",
		                 f"{show_class_object.absolute_movie_file_path}",
		                 f"{show_class_object.relative_show_path}"],
		                stderr=DEVNULL,
		                stdout=PIPE)
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show]['Symlinked'] = \
			strip_quotes_from_string(f"{process.communicate()[0].strip()}").replace('b"', str())[:-1].rstrip()
		print(g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show]['Symlinked'])
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
