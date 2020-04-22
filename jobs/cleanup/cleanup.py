import subprocess


def cleanup_sonarr_api_query(result):
	cleanupList = ["added", "cleanTitle", "firstAired", "images", "languageProfileId", "network", "overview",
	               "profileId", "qualityProfileId", "ratings", "runtime", "seasonCount", "seasonFolder", "sortTitle",
	               "status", "tags", "titleSlug", "tvMazeId", "tvRageId", "useSceneNumbering"]
	[result[index].get(x, str()) for index, (x) in enumerate(cleanupList) if x in result]
	return result


# any other cleanup scripts that are needed can be added here
def postExecutionCleanup():
	return subprocess.Popen(["/bin/bash",
	                         "scripts/clearcache.sh"],
	                        stderr = subprocess.DEVNULL,
	                        stdout = subprocess.PIPE)
