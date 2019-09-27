import os
def get_collection_absolute_path_parsed_this_run():
	return str(os.environ['YAML_FILE_CURRENT'])


def get_collection_absolute_path_parsed_last_run():
	return str(os.environ['YAML_FILE_PREVIOUS'])


