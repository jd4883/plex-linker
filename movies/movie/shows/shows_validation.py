#!/usr/bin/env python3
from os.path import (exists,
                     islink,
                     isfile)
from os import readlink

def check_if_valid_symlink_destination(show):
	if exists(show) and islink(show):
		readlink(show)
		return True
	return False


def check_if_valid_symlink_target(movie):
	if exists(movie) and isfile(movie):
		return True
	return False
