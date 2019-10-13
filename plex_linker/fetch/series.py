#!/usr/bin/env python3
import os

from messaging import backend as backend


def symlink_status(self, g):
	result = str(self.series_dict['Symlinked']) \
		if ('Symlinked' in self.series_dict) and self.series_dict['Symlinked'] \
		else str()
	g.LOG.debug(backend.debug_message(651, g, result))
	return result
	
def show_path_string(self, string):
	return str((str(string).replace('//','/')).replace(":", "")).replace(str(os.environ['SONARR_ROOT_PATH_PREFIX']),
	                                                                     str())
