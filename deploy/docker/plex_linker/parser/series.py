from messaging.backend import log_debug


def season_folder_from_api(self, g):
	result = self.inherited_series_dict["Parsed Season Folder"] = f"Season {self.season}"
	g.LOG.debug(log_debug(g, "season folder", result))
	return result


def relative_show_path(self, g):
	result = self.inherited_series_dict["Relative Show Path"] = f"{self.path}/{self.seasonFolder}"
	g.LOG.debug(log_debug(g, "relative show path", result))
	return str(result)


def padded_absolute_episode(self, g):
	result = ""
	if isinstance(self.absoluteEpisodeNumber, list):
		result = "-".join([str(i).zfill(self.padding) for i in self.absoluteEpisodeNumber])
	elif isinstance(self.absoluteEpisodeNumber, int):
		result = str(self.absoluteEpisodeNumber).zfill(self.padding)
	elif "Parsed Absolute Episode" in self.inherited_series_dict:
		del self.inherited_series_dict["Parsed Absolute Episode"]
	if result in (0, "00", "000", None):
		return ""
	g.LOG.debug(log_debug(g, "parsed absolute episode", result))
	return result
