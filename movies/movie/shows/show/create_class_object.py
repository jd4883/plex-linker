#!/usr/bin/env python3

from movies.movie.shows.show.show_gets import *


def create_tv_show_class_object(self,
                                show,
                                g):
	from class_objects import Show
	method_launch(g)
	tv_show_class_object = Show(show,
	                            self.movie_title,
	                            g)
	tv_show_class_object.show = show
	get_show(tv_show_class_object,
	         g)
	tv_show_class_object.raw_episodes = g.sonarr.get_episodes_by_series_id(g.movies_dictionary_object[self.movie_title]['Shows'][tv_show_class_object.show]['Show ID'])
	tv_show_class_object.raw_episode_files = g.sonarr.get_episode_files_by_series_id(g.movies_dictionary_object[self.movie_title]['Shows'][tv_show_class_object.show]['Show ID'])
	# fields from here are all valid from the API call to parse out
	
	# need to play with radarr as well as plex API calls for more functionality and cleaning up functions
	print(tv_show_class_object.raw_episodes[show])
	# tv_show_class_object.raw_episodes[index]['episodeNumber']
	# tv_show_class_object.raw_episodes[index]['seasonNumber']
	# tv_show_class_object.raw_episodes[index]['episodeNumber']
	# tv_show_class_object.raw_episodes[index]['title']
	# tv_show_class_object.raw_episodes[index]['episodeFile']['relativePath']
	# tv_show_class_object.raw_episodes[index]['path']
	# tv_show_class_object.raw_episode_files[index]['quality']['quality']['name']
	# tv_show_class_object.raw_episode_files[index]['monitored'] = False
	# tv_show_class_object.raw_episode_files[index]['hasfile']
	# tv_show_class_object.raw_episode_files[index]['episodeid']
	# tv_show_class_object.raw_episode_files[index]['absoluteEpisodeNumber']
	# tv_show_class_object.raw_episode_files[index]['mediaInfo']['videoCodec']
	# tv_show_class_object.raw_episode_files[index]['mediaInfo']['audioCodec']
	# tv_show_class_object.raw_episode_files[index]['mediaInfo']['audioChannels']
	
	
	
	for genre in sorted(g.sonarr_genres):
		output = g.sonarr.set_new_tag_for_sonarr({"label": genre})
		try:
			g.sonarr.set_new_tag_for_sonarr(str(genre).lower())
		except:
			pass
	method_exit(g)
	return tv_show_class_object
