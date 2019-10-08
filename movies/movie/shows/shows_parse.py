import messaging.frontend as message
import movies.movie.shows.show.validate as validate
from jobs.set_path_permissions import (set_permissions)
from jobs.symlinking import (symlink_force)
from movies.movie.movie_gets import (get_movie_path, get_relative_movie_path)
from movies.movie.shows.show.init import init_show_object
from movies.movie.shows.shows_validation import linking_can_be_skipped


def parse_show_to_link(show, g):
	message.method_launch(g)
	
	for _ in show.shows_dictionary.items():
		if validate.link_ready(show.quality):
			symlink_force(show, g)
			#show.absolute_movie_path = show.movie_dict['Absolute Movie Path'] = str(get_movie_path(show, g))
			#show.relative_movie_path = show.movie_dict['Relative Movie Path'] = str(get_relative_movie_path(show))
			set_permissions(show, g)
	message.method_exit(g)


def parse_shows_dictionary_object(movie, g):
	message.method_launch(g)
	if not movie.shows_dictionary:
		return
	for series in movie.shows_dictionary.keys():
		if series not in movie.shows_dictionary:
			print(f'conditional triggered for no series found to link to {movie.movie_title}')
			continue
		if str(type(movie.shows_dictionary[series])) != "<class 'dict'>":
			# no shows to associate with the movie
			print(f'conditional triggered for no series not set as a dictionary {movie.movie_title}')
			break
		show = init_show_object(movie, str(series), g)
		if linking_can_be_skipped(show, movie):
			print(f'conditional triggered for linking already completed {movie.movie_title}')
			continue
		else:
			print(f'proceeding to link {movie.movie_title}')
			parse_show_to_link(show, g)
