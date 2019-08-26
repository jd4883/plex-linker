#!/usr/bin/env python3
from IO.YAML.yaml_to_object import get_variable_from_yaml


def set_working_directory_to_media_path(media_directory):
	from os import chdir
	chdir(media_directory)


def set_working_directory_to_script_path():
	from os import chdir
	chdir(get_script_path())


def create_directory_if_not_present(path):
	from os import makedirs
	try:
		makedirs(path)
	except FileExistsError:
		pass


def get_script_path():
	return get_variable_from_yaml("Script Path")


def set_symlink_status_attributes_for_dictionary(class_object):
	#class_object.movies_dictionary_object.update({class_object.movie_title['Shows'][class_object.show] : {'Symlink Target': class_object.absolute_movie_file_path}})
	#print(class_object.movies_dictionary_object[class_object.movie_title])
	# class_object.movies_dictionary_object.update(
	#	{class_object.movie_title: {'Symlink Target': class_object.absolute_movie_file_path}})
	# class_object.movies_dictionary_object.update(
	#		{class_object.movie_title['Shows']: {
	#			class_object.show: {'Symlink Destination': class_object.relative_show_path,
	#			                    'Symlink Status': True}}})
	return class_object

