#!/usr/bin/env python3
def parse_relative_episode_file_path(self, episode_dict):
	if ('hasFile' in episode_dict) and (bool(episode_dict['hasFile'])):
		return self.show_path_string(episode_dict['episodeFile']['path'])
	raise KeyError
