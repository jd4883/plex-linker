import datetime

from marshmallow import fields, post_load, Schema

from methods import Show


class ShowLookupSchema(Schema):
	def __init__(self):
		self.added = fields.Str()
		self.airTime = fields.Str(required = False)
		self.certification = fields.Raw(required = False)
		self.cleanTitle = fields.Raw(required = False)
		self.firstAired = fields.DateTime(required = False)
		self.genres = fields.List(fields.Str(required = False))
		self.id = fields.Raw(required = True)
		self.images = fields.List(fields.Dict(required = False))
		self.imdbId = fields.Raw(required = True)
		self.languageProfileId = fields.Raw(required = False)
		self.lastInfoSync = fields.Raw(required = False)
		self.monitored = fields.Raw(required = False)
		self.network = fields.Raw(required = False)
		self.overview = fields.Raw(required = False)
		self.path = fields.Raw(required = True)
		self.profileId = fields.Raw(required = False)
		self.qualityProfileId = fields.Raw(required = False)
		self.ratings = fields.Raw(required = False)
		self.remotePoster = fields.Url(required = False, default = str())
		self.runtime = fields.Int(required = False, default = 20)
		self.seasonCount = fields.Int(required = False, default = 1)
		self.seasonFolder = fields.Bool(required = False, default = True)
		self.seasons = fields.Raw(required = False, default = list())
		self.seriesType = fields.Str(required = True, default = "anime")
		self.sortTitle = fields.Str(required = False)
		self.status = fields.Str(required = False, status = "continuing")
		self.tags = fields.Raw(required = False, default = list())
		self.title = fields.Raw(required = True)
		self.titleSlug = fields.Str(required = False)
		self.tvdbId = fields.Int(required = True)
		self.tvMazeId = fields.Int(required = False)
		self.tvRageId = fields.Int(required = False)
		self.useSceneNumbering = fields.Bool(required = False, default = False)
		self.year = fields.Int(required = True, default = int(datetime.datetime.year))
	
	@post_load
	def make_show(self, data, **kwargs):
		return Show(**data)
