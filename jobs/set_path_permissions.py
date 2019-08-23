#!/usr/bin/env python3
import os

from IO.YAML.yaml_to_object import get_variable_from_yaml


def set_file_mask_with_chmod_on_files_and_links(path):
	os.chmod(path,
	         0o775)


def set_permissions(movie_class_object):
	set_file_mask_with_chmod_on_files_and_links(movie_class_object.absolute_movie_path)
	set_ownership_on_files_and_links(movie_class_object.absolute_movie_path)
	if movie_class_object.absolute_movie_file_path:
		set_ownership_on_files_and_links(movie_class_object.absolute_movie_file_path)


def set_ownership_on_files_and_links(path):
	fd = os.open(f"{path}",
	             os.O_RDONLY)
	os.fchown(fd,
	          get_variable_from_yaml("PUID"),
	          get_variable_from_yaml("PGID"))
	os.close(fd)
