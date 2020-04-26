import subprocess


# any other cleanup scripts that are needed can be added here
def postExecutionCleanup():
	return subprocess.Popen(["/bin/bash",
	                         "scripts/clearcache.sh"],
	                        stderr = subprocess.DEVNULL,
	                        stdout = subprocess.PIPE)
