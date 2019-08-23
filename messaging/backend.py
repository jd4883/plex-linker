#!/usr/bin/env python3.7
from logs.bin.get_parameters import *
from logs.bin.get_parameters import (
	get_parent_method_string,
	get_parsed_message,
)


def debug_message(status_code=-1,
                  method="",
                  parent_method="main",
                  var1="",
                  var2=""):
	if not method:
		method = get_child_method_string()
		parent_method = get_parent_method_string()
	message2 = ""
	message3 = ""
	message4 = ""
	from logs.bin.get_parameters import get_method_hierarchy_for_current_function
	method_hierarchy = get_method_hierarchy_for_current_function(method,
	                                                             parent_method)
	if status_code == 1001:
		message1 = format_string(f"bro, there ain't any absolute episodes to see here")
	elif status_code == 1000:
		message1 = format_string(f"funny story boss,")
		message2 = f"{var1}"
		message3 = format_string(f" absolute episode found and will be parsed")
	elif status_code == 999:
		message1 = format_string(f"uh boss, we've got a winner; an anime winner that is")
	elif status_code == 997:
		message1 = format_string(f"boss, we are returning")
		message2 = f"{var1}"
	elif status_code == 996:
		message1 = format_string("looking up")
		message2 = f"{var1}"
		message3 = format_string("and returning a string or dictionary object")
	elif status_code == 995:
		message1 = format_string(f"returning the dictionary")
		message2 = format_string(f"{var1}")
		message3 = f"to the callback function"
	elif status_code == 993:
		message1 = format_string("about to link:\t\t\ttarget =")
		message2 = f"{var1}"
		message3 = format_string("-> link")
		message4 = f"{var2}"
	elif status_code == 992:
		message1 = format_string(f"removing original:")
		message2 = format_string(f"{var1}")
		message3 = format_string(" to avoid conflicting files")
	elif status_code == 991:
		message1 = format_string(f"entering method:")
		message2 = format_string(f"{method}")
	elif status_code == 990:
		message1 = format_string(f"exiting method:")
		message2 = format_string(f"{method}")
	elif status_code == 989:
		message1 = format_string(f"returning validated path:")
		message2 = f"{var1}"
	elif status_code == 988:
		message1 = format_string(f"ready to link: ")
		message2 = f"{var1}"
		message3 = format_string(f"was found and will be linked as")
		message4 = f"{var2}"
	elif status_code == 987:
		message1 = f"{var1}"
	elif status_code == 986:
		message1 = f"{var1}"
		message2 = format_string(f"is:\t")
		message3 = f"{var2}"
	elif status_code == 985:
		message1 = format_string(f"absolute")
		message2 = format_string(f"path:")
		message3 = format_string(f"{var2}")
	elif status_code == 984:
		message1 = f"{var1}:"
		message2 = f"{var2}"
	elif status_code == 982:
		message1 = format_string(f"success:")
		message2 = f"{var1}"
	elif status_code == 981:  # useful for handling edge cases
		message1 = format_string(f"we hit an unexpected edge case in this method")
	elif status_code == 876:
		message1 = format_string(f"method")
		message2 = f"`{parent_method}`"
		message3 = format_string(f"finished")
	elif status_code == 875:
		message1 = f"{var1}"
		message2 = f"`({var2})`"
		message3 = format_string(f"has been successfully parsed")
	elif status_code == 874:
		message1 = f"edge case hit here boss, we need a better way to " \
		           f"identify if movies have associated shows"
		message2 = f"`({var2})`"
		message3 = format_string(f"has been successfully parsed")
	
	# new defined methods are all here
	elif status_code == 826:
		message1 = format_string("Linked:")
		message2 = f"{var1}"
		message3 = format_string(" -->")
		message4 = f"{var2}"
	elif status_code == 825:
		message1 = format_string("season parsed as:")
		message2 = f"{var1}"
	elif status_code == 824:
		message1 = format_string("permissions configured for:")
		message2 = f"{var1}"
	elif status_code == 823:
		message1 = format_string("base show name:")
		message2 = f"{var1}"
	elif status_code == 822:
		message1 = format_string("absolute show path:")
		message2 = f"{var1}"
	elif status_code == 821:
		message1 = format_string(f"possible root paths:")
		message2 = f"{var1}"
	elif status_code == 820:
		message1 = format_string(f"show title:")
		message2 = f"{var1}"
	elif status_code == 819:
		message1 = format_string(f"show path:")
		message2 = f"{var1}"
	elif status_code == 818:
		message1 = format_string(f"media path:")
		message2 = f"{var1}"
	elif status_code == 817:
		message1 = format_string(f"absolute movie file path:")
		message2 = f"{var1}"
	elif status_code == 816:
		message1 = format_string(f"absolute movie folder path:")
		message2 = f"{var1}"
	elif status_code == 815:
		message1 = format_string(f"checking if this is a video:")
		message2 = f"{var1}"
	elif status_code == 814:
		message1 = format_string(f"video extension found:")
		message2 = f"{var1}"
	elif status_code == 813:
		message1 = format_string(f"checking directory for files with extension:")
		message2 = f"{var1}"
	elif status_code == 812:
		message1 = format_string(f"video file found:")
		message2 = f"{var1}"
	elif status_code == 811:
		message1 = format_string(f"nothing interesting to parse here:")
		message2 = f"{var1}"
	elif status_code == 810:
		message1 = format_string(f"parsed absolute path:")
		message2 = f"{var1}"
	elif status_code == 809:
		message1 = format_string(f"movie dictionary:")
		message2 = f"{var1}"
	elif status_code == 808:
		message1 = format_string(f"show(s) dictionary:")
		message2 = f"{var1}"
	elif status_code == 807:
		message1 = format_string(f"show dictionary:")
		message2 = f"{var1}"
	elif status_code == 806:
		message1 = format_string(f"movie media path:")
		message2 = f"{var1}"
	elif status_code == 805:
		message1 = format_string(f"movie file extension:")
		message2 = f"{var1}"
	elif status_code == 804:
		message1 = format_string(f"movie file quality:")
		message2 = f"{var1}"
	elif status_code == 803:
		message1 = format_string(f"shows associated with `{var1}`:")
		message2 = f"{var2}"
	elif status_code == 802:
		message1 = format_string(f"absolute movie path:")
		message2 = f"{var1}"
	elif status_code == 801:
		message1 = format_string(f"relative movies path:")
		message2 = f"{var1}"
	elif status_code == 800:
		message1 = format_string(f"movie dictionary:")
		message2 = f"{var1}"
	elif status_code == 799:
		message1 = format_string(f"movie name:")
		message2 = f"{var1}"
	elif status_code == -1:
		message1 = format_string(
			f"boss, you've indicated this {status_code} is an error that warrants exiting. check yo code!!")
		exit(-1)
	elif status_code == -2:
		message1 = format_string(f"bro,")
		message2 = f"{var1}"
		message3 = format_string(f"was not found, check your yaml file")
	elif status_code == -3:
		message1 = format_string(f"bro,")
		message2 = f"{var1}"
		message3 = format_string(f"appears to have a type error, check your yaml file")
	else:
		message1 = format_string(f"Uh boss, you may want to refactor your code for a better message \
                    for code {status_code}. If done this message will go away")
	message1 = message1.ljust(35)
	message2 = message2.ljust(25)
	message3 = message3.ljust(25)
	message4 = message4.ljust(25)
	return get_parsed_message(message1,
	                          message2,
	                          message3,
	                          message4,
	                          method_hierarchy)
