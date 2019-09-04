#!/usr/bin/env python3
import os
from pathlib import Path

from IO.YAML.yaml_to_object import get_variable_from_yaml
from messaging.frontend import (method_launch,
                                method_exit)
from movies.movies_puts import set_working_directory_to_media_path


def set_file_mask_with_chmod_on_files_and_links(path,
                                                g):
	Path(str(path)).touch()
	method_launch(g)
	os.chmod(path,
	         0o775)
	method_exit(g)


def set_permissions(movie_class_object,
                    g):
	set_working_directory_to_media_path(g.MEDIA_PATH)
	set_file_mask_with_chmod_on_files_and_links(movie_class_object.absolute_movie_path,
	                                            g)
	set_ownership_on_files_and_links(movie_class_object.absolute_movie_path)
	if movie_class_object.absolute_movie_file_path:
		set_working_directory_to_media_path(g.MEDIA_PATH)
		set_ownership_on_files_and_links(movie_class_object.absolute_movie_file_path)


def set_ownership_on_files_and_links(path):
	Path(str(path)).touch()
	fd = os.open(f"{path}",
	             os.O_RDONLY)
	os.fchown(fd,
	          get_variable_from_yaml("PUID"),
	          get_variable_from_yaml("PGID"))
	os.close(fd)
