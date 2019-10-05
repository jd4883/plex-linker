#!/usr/bin/env python3
def cleanup_sonarr_api_query(result):
	cleanup_list = ['overview',
	                'status',
	                'network',
	                'cleanTitle',
	                'useSceneNumbering',
	                'runtime',
	                'images',
	                'seasonCount',
	                'remotePoster',
	                'added',
	                'sortTitle',
	                'lastInfoSync',
	                'titleSlug',
	                'certification',
	                'profileId',
	                'tags',
	                'ratings',
	                'qualityProfileId',
	                'tvRageId',
	                'tvMazeId',
	                'firstAired',
	                'languageProfileId',
	                'seasonFolder']
	# need to make this a dynamic alternative to the ugly code here
	i = 0
	while i < len(result):
		# j = 0
		# while j < len(cleanup_list):
		# 	if result[i][j] in cleanup_list:
		# 		result[i].pop(j)
		# 	j += 1
		# print('completed i j loop')
		result[i].pop('overview', str())
		result[i].pop('status', str())
		result[i].pop('network', str())
		result[i].pop('cleanTitle', str())
		result[i].pop('useSceneNumbering', str())
		result[i].pop('runtime', str())
		result[i].pop('images', str())
		result[i].pop('seasonCount', str())
		result[i].pop('added', str())
		result[i].pop('sortTitle', str())
		result[i].pop('titleSlug', str())
		result[i].pop('profileId', str())
		result[i].pop('tags', str())
		result[i].pop('ratings', str())
		result[i].pop('qualityProfileId', str())
		result[i].pop('tvRageId', str())
		result[i].pop('tvMazeId', str())
		result[i].pop('firstAired', str())
		result[i].pop('languageProfileId', str())
		result[i].pop('seasonFolder', str())
		# try:
		# 	result[i].pop('overview', str())
		# 	result[i].pop('status', str())
		# 	result[i].pop('network', str())
		# 	result[i].pop('cleanTitle', str())
		# 	result[i].pop('useSceneNumbering', str())
		# 	result[i].pop('runtime', str())
		# 	result[i].pop('images', str())
		# 	result[i].pop('seasonCount', str())
		# 	result[i].pop('added', str())
		# 	result[i].pop('sortTitle', str())
		# 	result[i].pop('titleSlug', str())
		# 	result[i].pop('profileId', str())
		# 	result[i].pop('tags', str())
		# 	result[i].pop('ratings', str())
		# 	result[i].pop('qualityProfileId', str())
		# 	result[i].pop('tvRageId', str())
		# 	result[i].pop('tvMazeId', str())
		# 	result[i].pop('firstAired', str())
		# 	result[i].pop('languageProfileId', str())
		# 	result[i].pop('seasonFolder', str())
		# except KeyError:
		# 	pass
		i += 1
	return result


def link_properties(movie, show):
	show.show_dictionary['Symlinked'] = str()
	show.show_dictionary['Relative Show File Path'] = str()
	movie.movie_dictionary["Parsed Movie File"] = str()
