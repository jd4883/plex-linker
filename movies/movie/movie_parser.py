import messaging.frontend as message


def extension_from_movie_file(movie,
                              g):
	message.method_launch(g)
	movie.quality = parse_quality(movie)
	message.print_movie_file_found_to_parse(movie, g)
	message.print_movie_extension_found_to_parse(movie, g)
	message.print_movie_file_quality(movie, g)
	message.method_exit(g)


# def parse_movie_file_quality(movie_file):
# 	return movie_file.split().pop()
#
#
# def parse_quality(movie):
# 	if str(movie.quality).lower() == "Remux-1080p.mkv".lower():
# 		quality.replace("Remux-1080p.mkv", "Bluray-1080p Remux.mkv")
# 	if quality.endswith(f"Proper.{movie.extension}"):
# 		quality = f"{movie.movie_file.split().pop(-2)} {movie.quality}"
# 	else:
# 		quality = movie_file.split().pop()
# 	return quality
