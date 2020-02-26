#!/usr/bin/env python3
def cleanup_dict(dictObj):
	for k in ['Has Link',
	          'Parsed Episode Title',
	          'Parsed Season Folder',
	          'Relative Show File Path',
	          'Relative Show File Path',
	          'Relative Show Path',
	          'Season',
	          'Show Genres',
	          'Show Root Path',
	          'Title',
	          'episodeFileId',
	          'imdbId']:
		try:
			del dictObj[k]
		except KeyError:
			continue
		except AttributeError:
			continue
