import messaging.frontend as message


# def parse_show(self, g, season = str(os.environ['SEASON_INT'])):
# 	message.method_launch(g)
# 	init.anime_status(self)
# 	if not self.show_dictionary['Season']:
# 		self.show_dictionary['Season'] = season
# 	self.show_dictionary['Parsed Season Folder'] = season_folder_key(self, g)
# 	self.episode = set_nested_dictionary_key_value_pair(self.show_dictionary['Episode'], str())
# 	self.absolute_episode = set_nested_dictionary_key_value_pair(self.show_dictionary['Absolute Episode'], str())
# 	message.method_launch(g)
# 	if self.show_dictionary['Anime']:
# 		self.episode = "-".join([get_padded_episode_number(e, 3) for e in self.episode])
# 		self.absolute_episode = "-".join([get_padded_episode_number(e, 3) for e in self.absolute_episode])
# 	else:
# 		self.episode = "-".join([get_padded_episode_number(e, 2) for e in self.episode])
# 		self.absolute_episode = "-".join([get_padded_episode_number(e, 2) for e in self.absolute_episode])
# 	message.method_exit(g)
# 	self.parsed_relative_title = set_nested_dictionary_key_value_pair(self.show_dictionary['Parsed Relative Show '
# 	                                                                                       'Title'],
# 	                                                                  parse_show_title_from_show_dictionary(self, g))
# 	message.method_exit(g)
# 	return self.parsed_relative_title


# def get_parsed_show_title(show):
# 	return " ".join((show.parsed_title, show.quality))


# def parse_root_path_string(api_query):
# 	if 'path' in api_query:
# 		return str(api_query['path']).replace(str(environ['SONARR_ROOT_PATH_PREFIX']), '')
# 	return str()


def parse_show_id(show, g):
	message.method_launch(g)
	show_id = str()
	for index in g.shows_dictionary:
		if index['title'] == show:
			show_id = int(index['id'])
			break
	message.method_exit(g)
	return show_id
