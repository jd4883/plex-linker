"""Set chmod and optional ownership on paths (PUID/PGID env for ownership)."""
import os
from pathlib import Path

from messaging.frontend import method_exit, method_launch


def set_file_mask_with_chmod_on_files_and_links(path, g):
	method_launch(g)
	try:
		os.chmod(str(path), 0o775)
	except (NotADirectoryError, OSError):
		pass
	method_exit(g)


def set_ownership_on_files_and_links(path):
	try:
		path = Path(path)
		if not path.exists():
			path.touch()
		fd = os.open(str(path), os.O_RDONLY)
		os.fchown(fd, int(os.environ.get("PUID", -1)), int(os.environ.get("PGID", -1)))
		os.close(fd)
	except (NotADirectoryError, OSError, ValueError, KeyError):
		pass
