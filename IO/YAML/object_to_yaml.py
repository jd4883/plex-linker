#!/usr/bin/env python3
from os import chdir

import yaml

from movies.movies_gets import get_media_collection_parsed_this_time
from movies.movies_puts import set_working_directory_to_script_path, get_script_path


def write_python_dictionary_object_to_yaml_file(self):
	set_working_directory_to_script_path()
	chdir(get_script_path())
	yaml.dump(self.movies_dictionary_object,
	          open(get_media_collection_parsed_this_time(),
	               "w+"))
