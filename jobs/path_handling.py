def create_directory(folder):
	import subprocess
	subprocess.Popen("mkdir", "-p", folder, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
