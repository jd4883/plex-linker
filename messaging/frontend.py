#!/usr/bin/env python3.7
import os

import logs.bin.get_parameters as parameters
from messaging.backend import debug_message


def message_exiting_function(g):
	os.chdir(g.MEDIA_DIRECTORY)
	g.LOG.debug(debug_message(601, g))


def method_launch(g):
	os.chdir(str(os.environ['DOCKER_MEDIA_PATH']))
	g.parent_method = parameters.get_parent_method_string()
	g.method = parameters.get_child_method_string()


def method_exit(g):
	os.chdir(g.MEDIA_DIRECTORY)
	message_exiting_function(g)
