#!/usr/bin/env python3

from messaging import backend as backend


def parent_dict(g, movie_dict):
	result = movie_dict
	g.LOG.debug(backend.debug_message(627, g, result))
	return result
