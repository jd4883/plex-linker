#!/usr/bin/env python3.7
import os
from pathlib import Path
from time import sleep

import methods as media
from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file as dict_to_yaml
from jobs.cleanup.cleanup import postExecutionCleanup
from plex_linker.gets.path import get_docker_media_path
from plex_linker.parser.movies import parse_all_movies_in_yaml_dictionary as parse_movies

if __name__ == "__main__":
	
	# TODO: improve how we look at items not in the library and make more efficient in calculations
	lock_path = f"{os.path.dirname(os.path.realpath(__file__))}/pid.lock"
	if not os.path.exists(lock_path):
		Path(lock_path).touch()
		g = media.Globals()
		master_dictionary = media.Movies(str(os.path.abspath(get_docker_media_path(g))))
		parse_movies(g)
		dict_to_yaml(g)
		
		"""
		RUNS CLEANUP METHODS
		** would like to remove all non-tracked links present in the media directories
		"""
		
		postExecutionCleanup()
		sleep(900)
		os.remove(lock_path)
