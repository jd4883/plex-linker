#!/usr/bin/env python3
import os
from os import environ
from pathlib import Path

from messaging.frontend import (method_launch,
                                method_exit)
from movies.movies_puts import set_working_directory_to_media_path


def set_file_mask_with_chmod_on_files_and_links(path,
                                                g):
	method_launch(g)
	try:
		path = str(path)
		Path(str(path)).touch()
		os.chmod(path,
		         0o775)
	except FileNotFoundError:
		pass
	method_exit(g)
	


def set_permissions(movie_class_object,
                    g):
	set_working_directory_to_media_path(str(environ['DOCKER_MEDIA_PATH']))
	set_file_mask_with_chmod_on_files_and_links(movie_class_object.absolute_movie_file_path,
	                                            g)
	set_ownership_on_files_and_links(movie_class_object.absolute_movie_file_path)


def set_ownership_on_files_and_links(path):
	try:
		Path(str(path)).touch()
		fd = os.open(f"{path}",
		             os.O_RDONLY)
		os.fchown(fd,
		          int(environ['PUID']),
		          int(environ['PGID']))
		os.close(fd)
	except FileNotFoundError:
		pass
