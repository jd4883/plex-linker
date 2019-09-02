#!/usr/bin/env python3
import logging
import sys
from os.path import exists

def get_method_hierarchy_for_current_function(g):
	return f"({g.parent_method} -> {g.method}):".ljust(75)


def get_method_main():
	return "main"


def format_string(string):
	string = ' '.join([t.title() for t in string.split()])
	string = string.replace("_", " ")
	return string


def get_parent_method_string():
	return format_string(f"{sys._getframe(3).f_code.co_name}")


def get_parsed_message(g,
                       method_hierarchy):
	return " ".join((method_hierarchy,
	                 g.message1,
	                 g.message2,
	                 g.message3,
	                 g.message4)).rstrip().lstrip()


def get_child_method_string():
	return format_string(f"{sys._getframe(2).f_code.co_name}")


def get_logger(file):
	from movies.movies_puts import get_script_path
	filename = f'{get_script_path()}/logs/{file}.log'
	mode = 'a+' if exists(filename) else 'w+'
	logging.basicConfig(level=logging.DEBUG,
	                    format='%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s',
	                    datefmt='%m-%d %H:%M',
	                    filename=filename,
	                    filemode=mode)
	
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter(f'%(name)-12s:\t%(levelname)-8s\t%(message)s')
	console.setFormatter(formatter)
	logging.getLogger(str()).addHandler(console)
	return logging.getLogger(f'{file}')  # for now disabling method since it does not dynamically change nicely


def get_log_name():
	return f"plex_linker"
