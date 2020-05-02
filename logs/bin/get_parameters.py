import sys
import re


def get_method_hierarchy_for_current_function(g):
	return f"({g.parent_method} -> {g.method}):".ljust(75)


def get_method_main():
	return "main"


def format_string(string):
	string = ' '.join([t.title() for t in string.split()])
	return re.sub("_", " ", string)


def get_parent_method_string(depth = 3):
	# noinspection PyProtectedMember
	return format_string(f"{sys._getframe(depth).f_code.co_name}")


def get_parsed_message(g, method_hierarchy):
	return " ".join((method_hierarchy, g.message1, g.message2, g.message3, g.message4)).rstrip().lstrip()


# noinspection PyProtectedMember
def get_child_method_string(depth = 2):
	return format_string(f"{sys._getframe(depth).f_code.co_name}")


