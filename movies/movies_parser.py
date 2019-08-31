#!/usr/bin/env python3
import jobs.cleanup.remove_duplicates

from messaging.frontend import (method_launch,
                                method_exit)

def parse_movies_in_library_and_remove_duplicates(var1,
                                                  var2,
                                                  path_array,
                                                  g):
	method_launch(g)
	if var1 or var2 is 'staging':
		jobs.cleanup.remove_duplicates.removing_duplicate_movies_from_staging(path_array,
		                                                                      var1,
		                                                                      var2,
		                                                                      g)
	else:
		jobs.cleanup.remove_duplicates.remove_duplicate_movies_that_are_not_from_staging(path_array,
		                                                                                 var1,
		                                                                                 var2,
		                                                                                 g)
	method_exit(g)
