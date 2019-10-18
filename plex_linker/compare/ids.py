def validate_tmdbId(id):
	return bool(str(id).isdigit() and id != 0)
	
