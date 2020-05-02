#!/usr/bin/env python3.7
import os
import subprocess
from pathlib import Path
from time import sleep
from methods.plex_api import PlexAPI
import methods as media
from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file as dict_to_yaml
from jobs.cleanup.cleanup import postExecutionCleanup
from plex_linker.gets.path import get_docker_media_path
from plex_linker.parser.movies import parse_all_movies_in_yaml_dictionary as parse_movies

if __name__ == "__main__":
	
	# TODO: improve how we look at items not in the library and make more efficient in calculations
	lock_path = f"{os.path.dirname(os.path.realpath(__file__))}/pid.lock"
	if not os.path.exists(lock_path):
		os.chdir(str(os.environ['DOCKER_MEDIA_PATH']))
		# used to clean dead links each run
		subprocess.Popen(["find", ".", "-xtype", "l",  "-delete"], stderr = subprocess.DEVNULL, stdout = subprocess.PIPE)
		Path(lock_path).touch()
		g = media.Globals()
		master_dictionary = media.Movies(str(os.path.abspath(get_docker_media_path(g))))
		parse_movies(g)
		dict_to_yaml(g)
		
		"""
		RUNS CLEANUP METHODS
		** would like to remove all non-tracked links present in the media directories
		"""
		
		plex = PlexAPI()
		postExecutionCleanup()
		print("PLEX: MOVIES")
		[print(video.title) for video in plex.movieLibrary]
		print("PLEX: TV")
		[print(video.title) for video in plex.tv]
		print("PLEX: ANIME")
		[print(video.title) for video in plex.anime]
		sleep(900)  # 15 minutes
		os.remove(lock_path)
