#!/usr/bin/env python3
import shutil
from shutil import (rmtree)

import movies.movies_parser
from messaging.frontend import (
	method_launch,
	method_exit,
	message_no_duplicates_to_remove,
	)


# noinspection PyUnusedFunction
def remove_duplicates(list_of_possible_paths,
                      g):
	method_launch(g)
	genres = {
			'staging':        'staging',
			'standup_comedy': 'horror',
			'horror':         'thrillers',
			'thrillers':      'foreign',
			'foreign':        'horror'
			}
	while True:
		for key, value in genres.items():
			movies.movies_parser.parse_movies_in_library_and_remove_duplicates(key,
			                                                                   value,
			                                                                   list_of_possible_paths,
			                                                                   g)
		break
	method_exit(g)


def remove_duplicate_movies_that_are_not_from_staging(possible_duplicate_movie,
                                                      var1,
                                                      var2,
                                                      g):
	method_launch(g)
	if f"/{var1}/" in possible_duplicate_movie[0] and f"/{var2}/" in possible_duplicate_movie[1]:
		rmtree(possible_duplicate_movie[0])
	elif f"/{var1}/" in possible_duplicate_movie[1] and f"/{var2}/" in possible_duplicate_movie[2]:
		rmtree(possible_duplicate_movie[1])
	else:
		message_no_duplicates_to_remove()
	method_exit(g)


def removing_duplicate_movies_from_staging(possible_duplicate_movie,
                                           var1,
                                           var2,
                                           g):
	method_launch(g)
	if f"/{var1}/" in possible_duplicate_movie[0] and f"/{var2}/" not in possible_duplicate_movie[1]:
		shutil.rmtree(possible_duplicate_movie[0])
	elif f"/{var1}/" in possible_duplicate_movie[1] and f"/{var2}/" not in possible_duplicate_movie[2]:
		shutil.rmtree(possible_duplicate_movie[1])
	else:
		# No duplicates to parse here
		pass
	method_exit(g)
