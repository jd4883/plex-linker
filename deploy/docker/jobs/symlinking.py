"""Create symlink from movie file to show path."""
import os
import subprocess

from messaging.backend import log_debug
from messaging.frontend import method_exit, method_launch


def _clean_path(s: str) -> str:
	for old, new in (("..", "."), (":", "-")):
		s = s.replace(old, new)
	return s.lstrip("/")


def symlink_force(movie, show, g):
	method_launch(g)
	os.chdir(g.MEDIA_PATH)
	src = _clean_path(movie.absolute_movie_file_path)
	dst = _clean_path(show.relative_show_file_path)
	if not os.path.isfile(src):
		method_exit(g)
		return
	out, _ = subprocess.Popen(
		["ln", "-fsvr", src, dst],
		stderr=subprocess.DEVNULL,
		stdout=subprocess.PIPE,
	).communicate()
	g.LOG.info(log_debug(g, "link created", (out or b"").decode().strip()))
	method_exit(g)
