#!/usr/bin/env python3
import logging
import os
import sys


def get_method_hierarchy_for_current_function(g):
	return f"({g.parent_method} -> {g.method}):".ljust(75)


def get_method_main():
	return "main"


def format_string(string):
	string = ' '.join([t.title() for t in string.split()])
	string = string.replace("_", " ")
	return string


def get_parent_method_string(depth = 3):
	# noinspection PyProtectedMember
	return format_string(f"{sys._getframe(depth).f_code.co_name}")


def get_parsed_message(g, method_hierarchy):
	return " ".join((method_hierarchy, g.message1, g.message2, g.message3, g.message4)).rstrip().lstrip()


# noinspection PyProtectedMember
def get_child_method_string(depth = 2):
	return format_string(f"{sys._getframe(depth).f_code.co_name}")


def get_logger(file):
	filename = f"{os.environ['LOGS']}/{file}.log"
	mode = 'a+' if os.path.exists(filename) else 'w+'
	logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s',
	                    datefmt = '%m-%d %H:%M', filename = filename, filemode = mode)
	
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter(f'%(name)-12s:\t%(levelname)-8s\t%(message)s')
	console.setFormatter(formatter)
	logging.getLogger(str()).addHandler(console)
	return logging.getLogger(str(file))  # for now disabling method since it does not dynamically change nicely


def get_log_name():
	return str(os.environ['LOG_NAME'])
