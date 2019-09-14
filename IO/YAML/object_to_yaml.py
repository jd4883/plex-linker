#!/usr/bin/env python3
import time
from pathlib import Path
from shutil import move

import yaml

from IO.gets import get_collection_absolute_path_parsed_this_run, get_collection_absolute_path_parsed_last_run
from jobs.set_path_permissions import (set_file_mask_with_chmod_on_files_and_links,
                                       set_ownership_on_files_and_links)
from messaging.frontend import method_launch, method_exit
from movies.movies_gets import (get_media_collection_parsed_archives)


def write_python_dictionary_object_to_yaml_file(g):
	method_launch(g)
	Path(get_collection_absolute_path_parsed_this_run()).touch()
	yaml.dump(g.movies_dictionary_object,
	          open(
		          get_collection_absolute_path_parsed_this_run(),
		          "w+"))
	move(get_collection_absolute_path_parsed_last_run(),
	     f"{get_media_collection_parsed_archives()}/collection_parsed_{time.strftime('%m-%d-%Y')}.yaml")
	move(get_collection_absolute_path_parsed_this_run(),
	     get_collection_absolute_path_parsed_last_run())
	set_ownership_on_files_and_links(
		get_collection_absolute_path_parsed_last_run())
	set_file_mask_with_chmod_on_files_and_links(
		get_collection_absolute_path_parsed_last_run(),
		g)
	set_ownership_on_files_and_links(get_media_collection_parsed_archives())
	set_file_mask_with_chmod_on_files_and_links(get_media_collection_parsed_archives(),
	                                            g)
	set_ownership_on_files_and_links(
		get_collection_absolute_path_parsed_this_run())
	set_file_mask_with_chmod_on_files_and_links(
		get_collection_absolute_path_parsed_this_run(),
		g)
	method_exit(g)
