#!/usr/bin/env python3
def deprecated_set_season_value(g,
                                show_object):
	if not show_object.season:
		if g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Season']:
			show_object.season = \
				g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Season']
		else:
			show_object.season = \
				g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Season'] = str(0)
	#print('SET SEASON FIELD: this should go away when the class object is instantiated each run')


def deprecated_set_anime_status(g,
                                show_object):
	if not show_object.anime_status:
		show_object.anime_status = g.movies_dictionary_object[show_object.movie_title]['Shows'][show_object.show]['Anime']
# print('SET ANIME STATUS: this should go away when the class object is instantiated each run')
