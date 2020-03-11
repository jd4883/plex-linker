#!/usr/bin/env python3
from os import environ
from os.path import relpath


def get_relative_movies_path(self):
	return relpath(self.absolute_movies_path, str(environ['DOCKER_MEDIA_PATH']))
