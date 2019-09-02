#!/usr/bin/env python3.7

from logs.bin.get_parameters import *
from logs.bin.get_parameters import (
	get_parent_method_string,
	get_parsed_message,
)


def debug_message(status_code,
                  g,
                  var1=str(),
                  var2=str()):
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
	if status_code == 1001:
		g.message1 = format_string(f"bro, there ain't any absolute episodes to see here")
	elif status_code == 1000:
		g.message1 = format_string(f"funny story boss,")
		g.message2 = f"{var1}"
		g.message3 = format_string(f" absolute episode found and will be parsed")
	elif status_code == 999:
		g.message1 = format_string(f"uh boss, we've got a winner; an anime winner that is")
	elif status_code == 997:
		g.message1 = format_string(f"boss, we are returning")
		g.message2 = f"{var1}"
	elif status_code == 996:
		g.message1 = format_string("looking up")
		g.message2 = f"{var1}"
		g.message3 = format_string("and returning a string or dictionary object")
	elif status_code == 995:
		g.message1 = format_string(f"returning the dictionary")
		g.message2 = format_string(f"{var1}")
		g.message3 = f"to the callback function"
	elif status_code == 993:
		g.message1 = format_string("about to link:\t\t\ttarget =")
		g.message2 = f"{var1}"
		g.message3 = format_string("-> link")
		g.message4 = f"{var2}"
	elif status_code == 992:
		g.message1 = format_string(f"removing original:")
		g.message2 = format_string(f"{var1}")
		g.message3 = format_string(" to avoid conflicting files")
	elif status_code == 991:
		g.message1 = format_string(f"entering method:")
		g.message2 = format_string(f"{g.method}")
	elif status_code == 990:
		g.message1 = format_string(f"exiting method:")
		g.message2 = format_string(f"{g.method}")
	elif status_code == 989:
		g.message1 = format_string(f"returning validated path:")
		g.message2 = f"{var1}"
	elif status_code == 988:
		g.message1 = format_string(f"ready to link: ")
		g.message2 = f"{var1}"
		g.message3 = format_string(f"was found and will be linked as")
		g.message4 = f"{var2}"
	elif status_code == 987:
		g.message1 = f"{var1}"
	elif status_code == 986:
		g.message1 = f"{var1}"
		g.message2 = format_string(f"is:\t")
		g.message3 = f"{var2}"
	elif status_code == 985:
		g.message1 = format_string(f"absolute")
		g.message2 = format_string(f"path:")
		g.message3 = format_string(f"{var2}")
	elif status_code == 984:
		g.message1 = f"{var1}:"
		g.message2 = f"{var2}"
	elif status_code == 982:
		g.message1 = format_string(f"success:")
		g.message2 = f"{var1}"
	elif status_code == 981:  # useful for handling edge cases
		g.message1 = format_string(f"we hit an unexpected edge case in this method")
	elif status_code == 876:
		g.message1 = format_string(f"method")
		g.message2 = f"`{g.parent_method}`"
		g.message3 = format_string(f"finished")
	elif status_code == 875:
		g.message1 = f"{var1}"
		g.message2 = f"`({var2})`"
		g.message3 = format_string(f"has been successfully parsed")
	elif status_code == 874:
		g.message1 = f"edge case hit here boss, we need a better way to " \
		             f"identify if self have associated shows"
		g.message2 = f"`({var2})`"
		g.message3 = format_string(f"has been successfully parsed")
	
	# new defined methods are all here
	elif status_code == 825:
		g.message1 = format_string("season parsed as:")
		g.message2 = f"{var1}"
	elif status_code == 824:
		g.message1 = format_string("permissions configured for:")
		g.message2 = f"{var1}"
	elif status_code == 823:
		g.message1 = format_string("base show name:")
		g.message2 = f"{var1}"
	elif status_code == 822:
		g.message1 = format_string("absolute show path:")
		g.message2 = f"{var1}"
	elif status_code == 821:
		g.message1 = format_string(f"possible root paths:")
		g.message2 = f"{var1}"
	elif status_code == 820:
		g.message1 = format_string(f"show title:")
		g.message2 = f"{var1}"
	elif status_code == 819:
		g.message1 = format_string(f"show path:")
		g.message2 = f"{var1}"
	elif status_code == 818:
		g.message1 = format_string(f"media path:")
		g.message2 = f"{var1}"
	elif status_code == 817:
		g.message1 = format_string(f"absolute self file path:")
		g.message2 = f"{var1}"
	elif status_code == 816:
		g.message1 = format_string(f"absolute self folder path:")
		g.message2 = f"{var1}"
	elif status_code == 815:
		g.message1 = format_string(f"checking if this is a video:")
		g.message2 = f"{var1}"
	elif status_code == 814:
		g.message1 = format_string(f"video extension found:")
		g.message2 = f"{var1}"
	elif status_code == 813:
		g.message1 = format_string(f"checking directory for files with extension:")
		g.message2 = f"{var1}"
	elif status_code == 812:
		g.message1 = format_string(f"video file found:")
		g.message2 = f"{var1}"
	elif status_code == 811:
		g.message1 = format_string(f"nothing interesting to parse here:")
		g.message2 = f"{var1}"
	elif status_code == 810:
		g.message1 = format_string(f"parsed absolute path:")
		g.message2 = f"{var1}"
	elif status_code == 809:
		g.message1 = format_string(f"self dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 808:
		g.message1 = format_string(f"show(s) dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 807:
		g.message1 = format_string(f"show dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 806:
		g.message1 = format_string(f"self media path:")
		g.message2 = f"{var1}"
	elif status_code == 805:
		g.message1 = format_string(f"self file extension:")
		g.message2 = f"{var1}"
	elif status_code == 804:
		g.message1 = format_string(f"self file quality:")
		g.message2 = f"{var1}"
	elif status_code == 803:
		g.message1 = format_string(f"shows associated with `{var1}`:")
		g.message2 = f"{var2}"
	elif status_code == 802:
		g.message1 = format_string(f"absolute self path:")
		g.message2 = f"{var1}"
	elif status_code == 801:
		g.message1 = format_string(f"relative self path:")
		g.message2 = f"{var1}"
	elif status_code == 800:
		g.message1 = format_string(f"self dictionary:")
		g.message2 = f"{var1}"
	elif status_code == 799:
		g.message1 = format_string(f"self name:")
		g.message2 = f"{var1}"
	elif status_code == -1:
		g.message1 = format_string(
			f"boss, you've indicated this {status_code} is an error that warrants exiting. check yo code!!")
		exit(-1)
	elif status_code == -2:
		g.message1 = format_string(f"bro,")
		g.message2 = f"{var1}"
		g.message3 = format_string(f"was not found, check your yaml file")
	elif status_code == -3:
		g.message1 = format_string(f"bro,")
		g.message2 = f"{var1}"
		g.message3 = format_string(f"appears to have a type error, check your yaml file")
	else:
		g.message1 = format_string(f"Uh boss, you may want to refactor your code for a better message \
						  for code {status_code}. If done this message will go away")
	g.message1 = g.message1.ljust(35)
	g.message2 = g.message2.ljust(25)
	g.message3 = g.message3.ljust(25)
	g.message4 = g.message4.ljust(25)
	return get_parsed_message(g,
	                          method_hierarchy)
