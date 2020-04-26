from marshmallow import fields, post_load, Schema

from methods import Show


class ShowLookupSchema(Schema):
	added = fields.Str()
	airTime = fields.Str(required = False)
	certification = fields.Raw(required = False)
	cleanTitle = fields.Str(required = False)
	firstAired = fields.DateTime()
	genres = fields.List(fields.Str())
	id = fields.Int(required = True)
	images = fields.List(fields.Dict(required = False))
	imdbId = fields.Str(required = True)
	languageProfileId = fields.Int()
	lastInfoSync = fields.Str(required = False)
	monitored = fields.Bool(required = True)
	network = fields.Raw(required = False)
	overview = fields.Str(required = False)
	path = fields.Raw(required = True)
	profileId = fields.Int()
	qualityProfileId = fields.Int()
	ratings = fields.Raw(required = False)
	remotePoster = fields.Url(required = False)
	runtime = fields.Int()
	seasonCount = fields.Int()
	seasonFolder = fields.Bool()
	seasons = fields.Raw(required = False)
	seriesType = fields.Str(required = True)
	sortTitle = fields.Str()
	status = fields.Str(required = False)
	tags = fields.Raw(required = False)
	title = fields.Str(required = True)
	titleSlug = fields.Str()
	tvdbId = fields.Int(required = True)
	tvMazeId = fields.Int()
	tvRageId = fields.Int()
	useSceneNumbering = fields.Bool(required = False)
	year = fields.Raw(required = True)
	
	@post_load
	def make_show(self, data, **kwargs):
		return Show(**data)
