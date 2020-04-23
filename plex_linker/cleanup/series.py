def cleanup_dict(dictObj):
	dictkeys = [
			'Has Link',
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
			'imdbId'
			]
	[removeKeys(dictObj, k) for k in dictkeys]


def removeKeys(dictObj, k):
	try:
		del dictObj[k]
	except KeyError or AttributeError:
		pass
