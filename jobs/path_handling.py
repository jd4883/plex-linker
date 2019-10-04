def create_directory(folder):
	import subprocess
	subprocess.Popen("mkdir", "-p", str(folder), stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
