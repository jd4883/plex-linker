def parse_relative_episode_file_path(self, episode_dict):
	print(f"EPISODE DICT {self.path_str(episode_dict)}")
	if ('hasFile' in episode_dict) and (bool(episode_dict['hasFile'])):
		print(f"EPISODE PATH FOUND: {self.path_str(episode_dict['episodeFile']['path'])}")
		return self.path_str(episode_dict['episodeFile']['path'])
	print(f"CHECK EPISODE PATH HERE WE HAVE A ISSUE: {self.path_str(episode_dict)}")
	raise

