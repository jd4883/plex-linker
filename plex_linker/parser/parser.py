#!/usr/bin/env python3
def parse_relative_episode_file_path(self, episode_dict):
	if ('hasFile' in episode_dict) and (bool(episode_dict['hasFile'])):
		return self.path_str(episode_dict['episodeFile']['path'])

