import time
from pathlib import Path
from shutil import move

import yaml

from IO.gets import get_collection_absolute_path_parsed_this_run, get_collection_absolute_path_parsed_last_run
from jobs.set_path_permissions import (
	set_file_mask_with_chmod_on_files_and_links,
	set_ownership_on_files_and_links,
	)
from messaging.frontend import method_launch, method_exit
from plex_linker.gets.path import get_media_collection_parsed_archives


def write_python_dictionary_object_to_yaml_file(g):
	method_launch(g)
	new = Path(get_collection_absolute_path_parsed_this_run())
	new.touch()
	yaml.dump(g.movies_dict, open(new, "w+"))
	previous = get_collection_absolute_path_parsed_last_run()
	archive_dir = get_media_collection_parsed_archives()
	move(previous, f"{archive_dir}/collection_parsed_{time.strftime('%m-%d-%Y')}.yaml")
	move(new, previous)
	set_ownership_on_files_and_links(previous)
	set_file_mask_with_chmod_on_files_and_links(previous, g)
	set_ownership_on_files_and_links(archive_dir)
	set_file_mask_with_chmod_on_files_and_links(archive_dir, g)
	set_ownership_on_files_and_links(new)
	set_file_mask_with_chmod_on_files_and_links(new, g)
	method_exit(g)
