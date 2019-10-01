import os
from pathlib import Path
import messaging.frontend as message


def set_file_mask_with_chmod_on_files_and_links(path, g):
	message.method_launch(g)
	try:
		
		path = str(path)
		Path(str(path)).touch()
		os.chmod(path, 0o775)
	except NotADirectoryError:
		pass
	message.method_exit(g)


def set_permissions(movie_class_object, g):
	message.method_launch(g)
	directory = str(os.environ['DOCKER_MEDIA_PATH'])
	os.chdir(directory)
	try:
		set_file_mask_with_chmod_on_files_and_links(movie_class_object.absolute_movie_file_path, g)
		set_ownership_on_files_and_links(movie_class_object.absolute_movie_file_path)
	except FileNotFoundError or NotADirectoryError:
		pass
	message.method_exit(g)
	

def set_ownership_on_files_and_links(path):
	try:
		path = str(path)
		if not os.path.exists(path):
			Path(path).touch()
		fd = os.open(f"{path}", os.O_RDONLY)
		os.fchown(fd, int(os.environ['PUID']), int(os.environ['PGID']))
		os.close(fd)
	except NotADirectoryError:
		pass
