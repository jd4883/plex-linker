#!/usr/bin/env python3

from subprocess import (Popen,
                        DEVNULL,
                        PIPE)
from messaging.frontend import (method_exit,
                                method_launch)


def symlink_force(show_class_object,
                  g):
	method_launch(g)
	print(f'determining links to create for {show_class_object.absolute_movie_file_path}')
	if (show_class_object.absolute_movie_file_path or show_class_object.relative_show_path) is not (
			None or 'None/' or show_class_object.absolute_movie_file_path.endswith(
		'None') or show_class_object.relative_show_path.endswith('None')):
		method_launch(g)
		# added the popen for relative symlinking because this was not working in the os symlink built in.
		# have not done any testing in Windows only on Ubuntu 18
		process = Popen(["ln",
		                 "-fsvr",
		                 f"{show_class_object.absolute_movie_file_path}",
		                 f"{show_class_object.relative_show_path}"],
		                stderr=DEVNULL,
		                stdout=PIPE)
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show]['Symlink'] = f"{process.communicate()[0].strip()}".replace('b"',
		                                                                                                                                                      str())[:-1]
		g.list_of_linked_movies.append(show_class_object.movie_title)
	else:
		print(f'no link created for {show_class_object.absolute_movie_file_path}')
		g.movies_dictionary_object[show_class_object.movie_title]['Shows'][show_class_object.show][
			'Symlink'] = str()
		g.list_of_movies_to_locate.append(show_class_object.movie_title)
	method_exit(g)
