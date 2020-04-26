from marshmallow import fields, post_load, Schema

from methods import Show


class ShowLookupSchema(Schema):
	certification = fields.Raw(required = False)
	cleanTitle = fields.Raw(required = False)
	id = fields.Raw(required = True)
	imdbId = fields.Raw(required = True)
	languageProfileId = fields.Raw(required = False)
	lastInfoSync = fields.Raw(required = False)
	monitored = fields.Raw(required = False)
	network = fields.Raw(required = False)
	overview = fields.Raw(required = False)
	path = fields.Raw(required = True)
	profileId = fields.Raw(required = False)
	qualityProfileId = fields.Raw(required = False)
	ratings = fields.Raw(required = False)
	seasons = fields.Raw(required = False, default = list())
	tags = fields.Raw(required = False, default = list())
	title = fields.Raw(required = True, default = str())
	added = fields.Str(required = False)
	airTime = fields.Str(required = False)
	firstAired = fields.DateTime(required = False)
	genres = fields.List(fields.Str(required = False))
	images = fields.List(fields.Dict(required = False))
	remotePoster = fields.Url(required = False, default = str())
	runtime = fields.Int(required = False, default = 20)
	seasonCount = fields.Int(required = False, default = 1)
	seasonFolder = fields.Bool(required = False, default = True)
	seriesType = fields.Str(required = True, default = "anime")
	sortTitle = fields.Str(required = False)
	status = fields.Str(required = False, status = "continuing")
	titleSlug = fields.Str(required = False)
	tvdbId = fields.Int(required = True)
	tvMazeId = fields.Int(required = False)
	tvRageId = fields.Int(required = False)
	useSceneNumbering = fields.Bool(required = False, default = False)
	year = fields.Int(required = False)
	
	@post_load()
	def make_show(data, **kwargs):
		return Show(**data)
