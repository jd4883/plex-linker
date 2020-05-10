import os

# TODO: this segment needs a little TLC as it isn't great now but could be way better without a lot of work
def get_collection_absolute_path_parsed_this_run():
	try:
		path = os.environ['YAML_FILE_CURRENT']
	except KeyError:
		path = get_collection_absolute_path_parsed_last_run()
	return str(path)


def get_collection_absolute_path_parsed_last_run():
	return str(os.environ['YAML_FILE_PREVIOUS'])
