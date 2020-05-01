import os
from os import chdir, environ


def parsed_collection():
	chdir(environ['PLEX_LINKER'])
	return "config_files/media_collection_parsed_last_run.yaml"


def get_media_collection_parsed_archives():
	chdir(environ['PLEX_LINKER'])
	return str(environ['CONFIG_ARCHIVES'])


def get_docker_media_path(g):
	return "/".join((str(os.environ['DOCKER_MEDIA_PATH']), g.MOVIES_PATH[0]))
