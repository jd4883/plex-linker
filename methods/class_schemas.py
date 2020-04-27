from marshmallow import fields, post_load, Schema

from methods import Show

"""
TODO:
update all raw entries to be typed with defaults
"""


class ShowLookupSchema(Schema):
	cleanTitle = fields.Raw()
	genres = fields.Raw(default = list())
	id = fields.Raw(required = True)
	imdbId = fields.Str(required = True)
	languageProfileId = fields.Int()
	path = fields.Str(default = str())
	profileId = fields.Int()
	qualityProfileId = fields.Raw()
	ratings = fields.Raw(default = str())
	runtime = fields.Int(default = 20)
	seasonCount = fields.Int(default = 1)
	seasonFolder = fields.Raw(default = True)
	seasons = fields.Raw()
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
