#!/usr/bin/env python3
from shutil import rmtree

from messaging.frontend import (method_launch,
                                method_exit)


# noinspection PyUnusedFunction
def remove_directory_and_contents(path,
                                  g):
	method_launch(g)
	rmtree(path)
	method_exit(g)
