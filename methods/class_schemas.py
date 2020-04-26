from marshmallow import fields, post_load, Schema

from methods import Show

"""
TODO:
update all raw entries to be typed with defaults
"""
class ShowLookupSchema(Schema):
	added = fields.Raw()
	airTime = fields.Str()
	certification = fields.Str()
	cleanTitle = fields.Raw()
	firstAired = fields.Str()
	genres = fields.List(fields.Str())
	id = fields.Int(required = True)
	images = fields.List(fields.Dict())
	imdbId = fields.Str(required = True)
	languageProfileId = fields.Int()
	lastInfoSync = fields.Str()
	monitored = fields.Bool(required = False, default = False)
	network = fields.Str()
	overview = fields.Str()
	path = fields.Str()  # could make this an API call?
	profileId = fields.Int()
	qualityProfileId = fields.Int()
	ratings = fields.Raw()
	remotePoster = fields.Str()
	runtime = fields.Int(required = False, default = 20)
	seasonCount = fields.Int(required = False, default = 1)
	seasonFolder = fields.Bool(default = True)
	seasons = fields.Raw(default = list())
	seriesType = fields.Str(required = True, default = "anime")
	sortTitle = fields.Str()
	status = fields.Raw(default = "continuing")
	tags = fields.Raw()
	title = fields.Str(required = True)
	titleSlug = fields.Str()
	tvdbId = fields.Int(required = True)
	tvMazeId = fields.Int()
	tvRageId = fields.Int()
	useSceneNumbering = fields.Bool(default = False)
	year = fields.Int()
	
	@post_load
	def make_show(self, data, **kwargs):
		return Show(**data)
