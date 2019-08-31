#!/usr/bin/env python3
import time
from pathlib import Path
from shutil import move

import yaml

from jobs.set_path_permissions import (set_file_mask_with_chmod_on_files_and_links,
                                       set_ownership_on_files_and_links)
from messaging.frontend import (method_launch,
                                method_exit)
from movies.movies_gets import (get_media_collection_parsed_last_time,
                                get_media_collection_parsed_archives)


def write_python_dictionary_object_to_yaml_file(g):
	method_launch(g)
	Path(
		f'/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_this_run.yaml').touch()
	yaml.dump(g.movies_dictionary_object,
	          open(
		          f'/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_this_run.yaml',
		          "w+"))
	move('/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_last_run.yaml',
	     f"{get_media_collection_parsed_archives()}/collection_parsed_{time.strftime('%m-%d-%Y')}.yaml")
	move(f'/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_this_run.yaml',
	     '/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_last_run.yaml')
	set_ownership_on_files_and_links(
		'/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_last_run.yaml')
	set_file_mask_with_chmod_on_files_and_links(
		'/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_last_run.yaml',
		g)
	set_ownership_on_files_and_links(get_media_collection_parsed_archives())
	set_file_mask_with_chmod_on_files_and_links(get_media_collection_parsed_archives(),
	                                            g)
	set_ownership_on_files_and_links(
		f'/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_this_run.yaml')
	set_file_mask_with_chmod_on_files_and_links(
		f'/var/data/scripts/symlink_scripts/movie_tv_pairing/config_files/media_collection_parsed_this_run.yaml',
		g)
	method_exit(g)
