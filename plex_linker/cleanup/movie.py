#!/usr/bin/env python3
def cleanup_dict(dictObj):
	fields = ['Absolute Movie File Path', 'Absolute Movie Path', 'Has File', 'Parsed Extension',
	         'Parsed Movie Quality', 'Parsed Movie Extension', 'Relative Movie File Path', 'Relative Movie Path',
	         'Title', 'Unparsed Title', 'Year']
	for k in fields:
		try:
			del dictObj[k]
		except KeyError or AttributeError:
			continue
