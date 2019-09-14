#!/usr/bin/env python3.7

from logs.bin.get_parameters import *
from logs.bin.get_parameters import (
	get_parent_method_string,
	get_parsed_message,
)


def debug_message(status_code,
                  g,
                  var1=str()):
	if not status_code:
		status_code = -1
	if not g.method:
		g.method = get_child_method_string()
		g.parent_method = get_parent_method_string()
	g.message1 = str()
	g.message2 = str()
	g.message3 = str()
	g.message4 = str()
	from logs.bin.get_parameters import get_method_hierarchy_for_current_function
	method_hierarchy = get_method_hierarchy_for_current_function(g)
	if status_code == 600:
		g.message1 = format_string(f"entering method:")
		g.message2 = format_string(f"{g.method}")
	elif status_code == 601:
		g.message1 = format_string(f"exiting method:")
		g.message2 = format_string(f"{g.method}")
	elif status_code == 602:  # useful for handling edge cases
		g.message1 = format_string(f"we hit an unexpected edge case in this method")
	elif status_code == 603:
		g.message1 = format_string("season parsed as:")
		g.message2 = f"{var1}"
	elif status_code == 604:
		g.message1 = format_string(f"show title:")
		g.message2 = f"{var1}"
	elif status_code == 605:
		g.message1 = format_string(f"show path:")
		g.message2 = f"{var1}"
	elif status_code == 606:
		g.message1 = format_string(f"media path:")
		g.message2 = f"{var1}"
	elif status_code == 607:
		g.message1 = format_string(f"checking if this is a video:")
		g.message2 = f"{var1}"
	elif status_code == 608:
		g.message1 = format_string(f"video extension found:")
		g.message2 = f"{var1}"
	elif status_code == 609:
		g.message1 = format_string(f"checking directory for files with extension:")
		g.message2 = f"{var1}"
	elif status_code == 610:
		g.message1 = format_string(f"video file found:")
		g.message2 = f"{var1}"
	elif status_code == 611:
		g.message1 = format_string(f"show(s) dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 612:
		g.message1 = format_string(f"self file quality:")
		g.message2 = f"{var1}"
	elif status_code == -1:
		g.message1 = format_string(f"boss, you've indicated this {status_code} is an error that warrants exiting. check yo code!!")
		exit(-1)
	else:
		g.message1 = format_string(f"Uh boss, you may want to refactor your code for a better message \
						  for code {status_code}. If done this message will go away")
	g.message1 = g.message1.ljust(35)
	g.message2 = g.message2.ljust(25)
	g.message3 = g.message3.ljust(25)
	g.message4 = g.message4.ljust(25)
	return get_parsed_message(g,
	                          method_hierarchy)
