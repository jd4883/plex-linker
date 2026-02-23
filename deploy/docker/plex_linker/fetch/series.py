"""Return movie dict for series context (no transformation)."""
from messaging.backend import log_debug


def parent_dict(g, movie_dict):
	g.LOG.debug(log_debug(g, "movie dict", movie_dict))
	return movie_dict
