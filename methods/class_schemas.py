from marshmallow import fields, post_load, Schema

from methods import Show


class ShowLookupSchema(Schema):
	added = fields.Str()
	airTime = fields.Str()
	certification = fields.Raw()
	cleanTitle = fields.Str()
	firstAired = fields.DateTime()
	genres = fields.List(fields.Str())
	id = fields.Int(required = True)
	images = fields.Raw()
	imdbId = fields.Str(required = True)
	languageProfileId = fields.Int()
	lastInfoSync = fields.Str()
	monitored = fields.Bool(required = True)
	network = fields.Raw()
	overview = fields.Str()
	path = fields.Str(required = True)
	profileId = fields.Raw()
	qualityProfileId = fields.Int()
	ratings = fields.List(fields.Raw())
	remotePoster = fields.Url()
	runtime = fields.Int()
	seasonCount = fields.Int()
	seasonFolder = fields.Bool()
	seasons = fields.Raw()
	seriesType = fields.Str(required = True)
	sortTitle = fields.Str()
	status = fields.Str()
	tags = fields.List(fields.Int())
	title = fields.Str(required = True)
	titleSlug = fields.Str()
	tvdbId = fields.Int(required = True)
	tvMazeId = fields.Int()
	tvRageId = fields.Int()
	useSceneNumbering = fields.Bool()
	year = fields.Raw(required = True)
	
	@post_load
	def make_show(self, data, **kwargs):
		return Show(**data)
