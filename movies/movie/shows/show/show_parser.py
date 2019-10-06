import messaging.frontend as message


def parse_show_id(show, g):
	message.method_launch(g)
	show_id = str()
	for index in g.shows_dictionary:
		if index['title'] == show:
			show_id = int(index['id'])
			break
	message.method_exit(g)
	return show_id
