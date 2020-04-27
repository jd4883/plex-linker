from marshmallow import fields, post_load, Schema

from methods import Show

"""
TODO:
update all raw entries to be typed with defaults
"""


class ShowLookupSchema(Schema):
	added = fields.Raw(default = str())
	airTime = fields.Str(default = str())
	certification = fields.Str(default = str())
	cleanTitle = fields.Raw()
	firstAired = fields.Str(default = str())
	genres = fields.List(fields.Str(default = str()))
	id = fields.Raw(required = True)
	images = fields.Raw(default = dict())
	imdbId = fields.Str(required = True)
	languageProfileId = fields.Int()
	lastInfoSync = fields.Str(default = str())
	monitored = fields.Bool(default = False)
	network = fields.Raw()
	overview = fields.Str(default = str())
	path = fields.Str(default = str())
	profileId = fields.Int(default = 0)
	qualityProfileId = fields.Int(default = 0)
	ratings = fields.Raw()
	remotePoster = fields.Str(default = str())
	runtime = fields.Int(default = 20)
	seasonCount = fields.Int(default = 1)
	seasonFolder = fields.Bool(default = True)
	seasons = fields.Raw(default = list())
	seriesType = fields.Str(required = True, default = "anime")
	sortTitle = fields.Str(default = str())
	status = fields.Raw()
	tags = fields.Raw(default = list())
	title = fields.Str(required = True)
	titleSlug = fields.Raw(default = str())
	tvdbId = fields.Int(required = True)
	tvMazeId = fields.Raw(default = str())
	tvRageId = fields.Raw(default = str())
	useSceneNumbering = fields.Raw(default = False)
	year = fields.Int()
	
	@post_load
	def make_show(self, data, **kwargs):
		return Show(**data)
