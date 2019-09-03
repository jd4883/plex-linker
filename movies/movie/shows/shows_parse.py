#!/usr/bin/env python3
from os import readlink

from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from messaging.frontend import (method_launch,
                                method_exit)
from movies.movie.movie_gets import (get_relative_movie_path,
                                     get_movie_path)
from movies.movie.shows.show.create_class_object import create_tv_show_class_object
from movies.movie.shows.show.show_validation import (validate_ready_to_link_movie_to_show)
from movies.movie.shows.shows_validation import check_if_valid_symlink_destination, check_if_valid_symlink_target


def parse_show_to_link(show,
                       g):
	method_launch(g)
	for _ in g.movies_dictionary_object[show.movie_title]['Shows'].items():
		if validate_ready_to_link_movie_to_show(show.quality,
		                                        g):
			print('should be linking here')
			symlink_force(show,
			              g)
			print('link should have worked')
			show.absolute_movie_path = g.movies_dictionary_object[show.movie_title]['Absolute Movie Path'] = \
				str(get_movie_path(show,
				                   g))
			show.relative_movie_path = g.movies_dictionary_object[show.movie_title]['Relative Movie Path'] = \
				str(get_relative_movie_path(show,
				                            g))
			set_permissions(show,
			                g)
			print('exiting linking')
	method_exit(g)


def parse_shows_dictionary_object(movie_class_object,
                                  g):
	method_launch(g)
	for show in g.movies_dictionary_object[movie_class_object.movie_title]['Shows'].keys():
		try:
			del g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Link Destination']
			del g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Absolute Show Path']
		except:
			pass
		g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Parsed Season Folder'] = str()
		g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Parsed Episode'] = str()
		g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Parsed Show Root Folder'] = str()
		g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Relative Show Path'] = str()
		g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Absolute Show Path'] = str()
		g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Parsed Relative Show Title'] = str()
		g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Show Dictionary Object'] = dict()
		g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Symlinked'] = str()
		# make try except more specific
		#try:
			# this component sort of worked 9-2 but never got fully going. Trying to come up with a reasonably intelligent
			# way to know what not to parse each time, ideally without storing variables
			# g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Symlinked'] = str()
			# link_status = str(g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Symlinked'])
		relative_show_path = str(
			g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Relative Show File Path'])
		absolute_movie_path = str(
			g.movies_dictionary_object[movie_class_object.movie_title]["Parsed Movie File"])
		if str(g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Symlinked']) is not "":
		#if get_live_link(relative_show_path) and \
		#		(check_if_valid_symlink_destination(relative_show_path) and \
		#			(check_if_valid_symlink_target(absolute_movie_path))):
				print('met inner if condition')
				print(
					f"No action required for {movie_class_object.movie_title}")  # make an official message handler here
				print('condition met for not parsing')
				g.list_of_linked_movies.append(movie_class_object.movie_title)
				continue
		else:
			print(f"Started parsing {movie_class_object.movie_title}")  # make an official message handler here
			tv_show = create_tv_show_class_object(movie_class_object,
			                                      show,
			                                      g)
			print('show object created')
			tv_show.show = show
			# show object not getting created correctly here
			print('about to parse show for linking')
			parse_show_to_link(tv_show,
			                   g)
		#except KeyError:
		#	print('hit except condition')
		#	g.movies_dictionary_object[movie_class_object.movie_title]['Shows'][show]['Symlinked'] = str()
	method_exit(g)


def get_live_link(relative_show_path):
	# probably can make the logic a bit more clever here and check if the path put together from the parsed elements
	# already has a valid link, if not parse else continue to next item
	try:
		readlink(relative_show_path)
	except FileNotFoundError:
		return False
	return True
