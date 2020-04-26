from marshmallow import fields, post_load, Schema

from methods import Show

"""
TODO:
update all raw entries to be typed with defaults
"""
class ShowLookupSchema(Schema):
	added = fields.Raw(required = False)
	airTime = fields.Str(required = False, default = str())
	certification = fields.Str(required = False, default = str())
	cleanTitle = fields.Raw(required = False, default = str())
	firstAired = fields.Str(required = False, default = str())
	genres = fields.List(fields.Str(required = False, default = str()))
	id = fields.Int(required = True)
	images = fields.List(fields.Dict(required = False))
	imdbId = fields.Str(required = True)
	languageProfileId = fields.Int(required = False, default = 0)
	lastInfoSync = fields.Str(required = False, default = str())
	monitored = fields.Bool(required = False, default = False)
	network = fields.Str(required = False)
	overview = fields.Str(required = False)
	path = fields.Str(required = False, default = str())  # could make this an API call?
	profileId = fields.Int(required = False, default = 0)
	qualityProfileId = fields.Int(required = False, default = 0)
	ratings = fields.Raw(required = False)
	remotePoster = fields.Str(required = False, default = str())
	runtime = fields.Int(required = False, default = 20)
	seasonCount = fields.Int(required = False, default = 1)
	seasonFolder = fields.Bool(required = False, default = True)
	seasons = fields.Raw(required = False, default = list())
	seriesType = fields.Str(required = True, default = "anime")
	sortTitle = fields.Str(required = False)
	status = fields.Raw(required = False, status = "continuing")
	tags = fields.Raw(required = False, default = list())
	title = fields.Str(required = True, default = str())
	titleSlug = fields.Str(required = False)
	tvdbId = fields.Int(required = True)
	tvMazeId = fields.Int(required = False)
	tvRageId = fields.Int(required = False)
	useSceneNumbering = fields.Bool(required = False, default = False)
	year = fields.Int(required = False)
	
	@post_load
	def make_show(self, data, **kwargs):
		return Show(**data)
