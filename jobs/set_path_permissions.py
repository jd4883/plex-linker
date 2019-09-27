#!/usr/bin/env python3
import os
from os import environ, chdir
from os.path import exists
from pathlib import Path
import messaging.frontend as message


def set_file_mask_with_chmod_on_files_and_links(path, g):
	message.method_launch(g)
	try:
		path = str(path)
		Path(str(path)).touch()
		os.chmod(path, 0o775)
	except FileNotFoundError:
		pass
	message.method_exit(g)


def set_permissions(movie_class_object, g):
	message.method_launch(g)
	directory = str(environ['DOCKER_MEDIA_PATH'])
	chdir(directory)
	set_file_mask_with_chmod_on_files_and_links(movie_class_object.absolute_movie_file_path, g)
	set_ownership_on_files_and_links(movie_class_object.absolute_movie_file_path)
	message.method_exit(g)

def set_ownership_on_files_and_links(path):
	message.method_launch(g)
	try:
		path = str(path)
		if not exists(path):
			Path(path).touch()
		fd = os.open(f"{path}", os.O_RDONLY)
		os.fchown(fd, int(environ['PUID']), int(environ['PGID']))
		os.close(fd)
	except FileNotFoundError:
		pass
	message.method_exit(g)
