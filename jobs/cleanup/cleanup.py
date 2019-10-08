#!/usr/bin/env python3
def cleanup_sonarr_api_query(result):
	# need to make this a dynamic alternative to the ugly code here
	i = 0
	while i < len(result):
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
		i += 1
	return result


