def validate_tmdbId(ID):
	return bool(str(ID).isdigit() and ID != 0)
