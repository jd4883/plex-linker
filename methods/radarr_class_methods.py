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


# radarr_dictionary, movie, unparsed_title
def get_parsed_movie_title(self, g):
	result = re.sub("/", "+", re.sub(":", "-", f"{self.unparsed_title} ({self.year})"))
	g.LOG.debug(messaging.backend.debug_message(613, g, result))
	return result
