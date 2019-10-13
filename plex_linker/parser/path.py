#!/usr/bin/env python3
def parse_relative_episode_file_path(self, episode_dict):
	#print(f"EPISODE DICT {self.show_path_string(episode_dict)}")
	if ('hasFile' in episode_dict) and (bool(episode_dict['hasFile'])):
		#print(f"EPISODE PATH FOUND: {self.show_path_string(episode_dict['episodeFile']['path'])}")
		return self.show_path_string(episode_dict['episodeFile']['path'])
	#print(f"CHECK EPISODE PATH HERE WE HAVE A ISSUE: {self.show_path_string(episode_dict)}")
	raise KeyError
