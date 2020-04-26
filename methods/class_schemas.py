from marshmallow import fields, post_load, Schema

from methods import Show


class ShowLookupSchema(Schema):
	added = fields.Str()
	airTime = fields.Str(required = False)
	certification = fields.Raw(required = False)
	cleanTitle = fields.Str(required = False)
	firstAired = fields.DateTime(required = False)
	genres = fields.List(fields.Str(required = False))
	id = fields.Raw(required = True)
	images = fields.List(fields.Dict(required = False))
	imdbId = fields.Str(required = True)
	languageProfileId = fields.Int(required = False)
	lastInfoSync = fields.Str(required = False)
	monitored = fields.Raw(required = False)
	network = fields.Raw(required = False)
	overview = fields.Raw(required = False)
	path = fields.Raw(required = True)
	profileId = fields.Int(required = False)
	qualityProfileId = fields.Raw(required = False)
	ratings = fields.Raw(required = False)
	remotePoster = fields.Url(required = False)
	runtime = fields.Raw(required = False)
	seasonCount = fields.Int(required = False)
	seasonFolder = fields.Bool(required = False)
	seasons = fields.Raw(required = False)
	seriesType = fields.Raw(required = True)
	sortTitle = fields.Str(required = False)
	status = fields.Raw(required = False)
	tags = fields.Raw(required = False)
	title = fields.Raw(required = True)
	titleSlug = fields.Str(required = False)
	tvdbId = fields.Raw(required = True)
	tvMazeId = fields.Int(required = False)
	tvRageId = fields.Int(required = False)
	useSceneNumbering = fields.Bool(required = False)
	year = fields.Raw(required = True)
	
	@post_load
	def make_show(self, data, **kwargs):
		return Show(**data)
