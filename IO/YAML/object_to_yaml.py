#!/usr/bin/env python3
from pathlib import Path
from shutil import move
import yaml
import time
from jobs.set_path_permissions import (set_permissions,
                                       set_file_mask_with_chmod_on_files_and_links,
                                       set_ownership_on_files_and_links)
from movies.movies_gets import (get_media_collection_parsed_this_time,
                                get_media_collection_parsed_last_time,
                                get_media_collection_parsed_archives)
from movies.movies_puts import (set_working_directory_to_script_path)


def write_python_dictionary_object_to_yaml_file(self):
	set_working_directory_to_script_path()
	yaml.dump(self.movies_dictionary_object,
	          open(get_media_collection_parsed_this_time(),
	               "w+"))
	Path(get_media_collection_parsed_archives()).mkdir(parents=True,
	                                                   exist_ok=True)
	move(get_media_collection_parsed_last_time(),
	     f"{get_media_collection_parsed_archives()}/collection_parsed_{time.strftime('%m-%d-%Y')}.yaml")
	move(get_media_collection_parsed_this_time(),
	     get_media_collection_parsed_last_time())
	set_ownership_on_files_and_links(get_media_collection_parsed_last_time())
	set_file_mask_with_chmod_on_files_and_links(get_media_collection_parsed_last_time())
	set_ownership_on_files_and_links(get_media_collection_parsed_archives())
	set_file_mask_with_chmod_on_files_and_links(get_media_collection_parsed_archives())
# set_ownership_on_files_and_links(get_media_collection_parsed_this_time())
# set_file_mask_with_chmod_on_files_and_links(get_media_collection_parsed_this_time())
