#!/usr/bin/env python3
from os import (symlink,
                remove)

from messaging.frontend import (print_removing_duplicate_file,
                                method_exit,
                                method_launch, print_linking_show_to_movie)
from movies.movies_puts import (set_working_directory_to_media_path)


def symlink_force(show_class_object):
	method_launch(show_class_object)
	if (show_class_object.absolute_movie_file_path or
	    show_class_object.relative_show_path) is not \
			(None or 'None/'
			 or show_class_object.absolute_movie_file_path.endswith('None') or
			 show_class_object.relative_show_path.endswith('None')):
		while True:
			set_working_directory_to_media_path(show_class_object.MEDIA_PATH)
			try:
				
				symlink(f"{show_class_object.absolute_movie_file_path}",
				        f"{show_class_object.relative_show_path}")
				print_linking_show_to_movie(show_class_object)
				break
			except FileExistsError:
				print_removing_duplicate_file(show_class_object)
				remove(show_class_object.relative_show_path)
		method_exit(show_class_object)
