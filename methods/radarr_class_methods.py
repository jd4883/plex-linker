#!/usr/bin/env python3
import os
import re

import messaging.backend
from plex_linker.gets.path import get_movie_path


def parse_relpath(self, g, media_path):
	film = get_movie_path(self, g)
	if os.path.exists(film):
		return str(os.path.relpath(film, media_path))
	return str()
