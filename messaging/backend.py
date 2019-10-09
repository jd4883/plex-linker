#!/usr/bin/env python3.7

from logs.bin.get_parameters import *
from logs.bin.get_parameters import (
	get_parent_method_string,
	get_parsed_message,
	)


def debug_message(status_code, g, var1 = str(), var2 = str()):
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
		g.message1 = format_string(f"checking if this is a video file:")
		g.message2 = f"{var1}"
	elif status_code == 608:
		g.message1 = format_string(f"movie extension found:")
		g.message2 = f"{var1}"
	elif status_code == 609:
		g.message1 = format_string(f"checking directory for files with extension:")
		g.message2 = f"{var1}"
	elif status_code == 610:
		g.message1 = format_string(f"movie file found:")
		g.message2 = f"{var1}"
	elif status_code == 611:
		g.message1 = format_string(f"show(s) dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 612:
		g.message1 = format_string(f"movie quality:")
		g.message2 = f"{var1}"
	elif status_code == 613:
		g.message1 = format_string(f"movie title:")
		g.message2 = f"{var1}"
	elif status_code == 614:
		g.message1 = format_string(f"parsed absolute movie path:")
		g.message2 = f"{var1}"
	elif status_code == 615:
		g.message1 = format_string(f"parsed absolute movie file path:")
		g.message2 = f"{var1}"
	elif status_code == 616:
		g.message1 = format_string(f"parsed relative movie file path:")
		g.message2 = f"{var1}"
	elif status_code == 617:
		g.message1 = format_string(f"parsed relative movie path:")
		g.message2 = f"{var1}"
	elif status_code == 618:
		g.message1 = format_string(f"parsed show id:")
		g.message2 = f"{var1}"
	elif status_code == 619:
		g.message1 = format_string(f"parsed episode id:")
		g.message2 = f"{var1}"
	elif status_code == 620:
		g.message1 = format_string(f"failed to parse episode ID from show (SHOW | ID):")
		g.message2 = f"{var1}"
		g.message3 = f"{var2}"
	elif status_code == 621:
		g.message1 = format_string(f"parsed anime status:")
		g.message2 = f"{var1}"
	elif status_code == 621:
		g.message1 = format_string(f"parsed padding:")
		g.message2 = f"{var1}"
	elif status_code == 622:
		g.message1 = format_string(f"raw episode:")
		g.message2 = f"{var1}"
	elif status_code == 623:
		g.message1 = format_string(f"episode dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 624:
		g.message1 = format_string(f"show dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 625:
		g.message1 = format_string(f"sonarr show dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 626:
		g.message1 = format_string(f"sonarr api query dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 627:
		g.message1 = format_string(f"movie dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 628:
		g.message1 = format_string(f"absolute episode:")
		g.message2 = f"{var1}"
	elif status_code == 629:
		g.message1 = format_string(f"parsed relative show title:")
		g.message2 = f"{var1}"
	elif status_code == 630:
		g.message1 = format_string(f"show season number:")
		g.message2 = f"{var1}"
	elif status_code == 631:
		g.message1 = format_string(f"show season folder:")
		g.message2 = f"{var1}"
	elif status_code == 632:
		g.message1 = format_string(f"show root path:")
		g.message2 = f"{var1}"
	elif status_code == 633:
		g.message1 = format_string(f"relative show path:")
		g.message2 = f"{var1}"
	elif status_code == 634:
		g.message1 = format_string(f"show parsed episode:")
		g.message2 = f"{var1}"
	elif status_code == 635:
		g.message1 = format_string(f"parsed absolute episode:")
		g.message2 = f"{var1}"
	elif status_code == 636:
		g.message1 = format_string(f"show episode title:")
		g.message2 = f"{var1}"
	elif status_code == 637:
		g.message1 = format_string(f"parsed show title:")
		g.message2 = f"{var1}"
	elif status_code == 638:
		g.message1 = format_string(f"conditional met - no series found to link:")
		g.message2 = f"{var1}"
	elif status_code == 639:
		g.message1 = format_string(f"conditional met - no series found in dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 640:
		g.message1 = format_string(f"conditional met - linking already completed:")
		g.message2 = f"{var1}"
	elif status_code == 641:
		g.message1 = format_string(f"generating new link:")
		g.message2 = f"{var1}"
		g.message3 = f"--> {var2}"
	elif status_code == 642:
		g.message1 = format_string(f"Checking Link status for:")
		g.message2 = f"{var1}"
	elif status_code == -1:
		g.message1 = format_string(
				f"boss, you've indicated this {status_code} is an error that warrants exiting. check yo code!!")
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
