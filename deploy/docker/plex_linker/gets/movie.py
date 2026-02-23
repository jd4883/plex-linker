"""Movie path helpers."""
from os.path import relpath

from config import docker_media_path


def get_relative_movies_path(self):
    return relpath(self.absolute_movies_path, docker_media_path())
