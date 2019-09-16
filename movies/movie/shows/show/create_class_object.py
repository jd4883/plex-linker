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
	print(f"episode to compare: {tv_show_class_object.episode}")
	print(f'season to compare: {tv_show_class_object.season}')
	for episode in tv_show_class_object.raw_episodes:
		# print(f"Season number to potentially parse: {episode['seasonNumber']}")
		if (int(episode['seasonNumber']) == int(tv_show_class_object.season)) and (int(episode['episodeNumber']) == int(
				tv_show_class_object.episode)):
			print('we should parse an episode')
		# if str(episode['episodeNumber']) == str(tv_show_class_object.episode):
		# 	print(f"Episode found: {episode['episodeNumber']}")
		# else:
		# 	print(f"episode is not a match: {episode['episodeNumber']}")
	exit(-1)
	# tv_show_class_object.raw_episodes[show]['seasonNumber']
	# tv_show_class_object.raw_episodes[show]['episodeNumber']
	# tv_show_class_object.raw_episodes[show]['title']
	# tv_show_class_object.raw_episodes[show]['episodeFile']['relativePath']
	# tv_show_class_object.raw_episodes[show]['path']
	# tv_show_class_object.raw_episode_files[show]['quality']['quality']['name']
	# tv_show_class_object.raw_episode_files[show]['monitored'] = False
	# tv_show_class_object.raw_episode_files[show]['hasfile']
	# tv_show_class_object.raw_episode_files[show]['episodeid']
	# tv_show_class_object.raw_episode_files[show]['absoluteEpisodeNumber']
	# tv_show_class_object.raw_episode_files[show]['mediaInfo']['videoCodec']
	# tv_show_class_object.raw_episode_files[show]['mediaInfo']['audioCodec']
	# tv_show_class_object.raw_episode_files[show]['mediaInfo']['audioChannels']
	#
	
	
	for genre in sorted(g.sonarr_genres):
		output = g.sonarr.set_new_tag_for_sonarr({"label": genre})
		try:
			g.sonarr.set_new_tag_for_sonarr(str(genre).lower())
		except:
			pass
	method_exit(g)
	return tv_show_class_object
