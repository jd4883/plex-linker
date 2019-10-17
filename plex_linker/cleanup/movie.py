#!/usr/bin/env python3
def cleanup_dict(dict):
	for k in ['Absolute Movie File Path',
	          'Absolute Movie Path',
	          'Has File',
	          'Parsed Extension',
	          'Parsed Movie Quality',
	          'Parsed Movie Extension',
	          'Relative Movie File Path',
	          'Relative Movie Path',
	          'Title',
	          'Unparsed Title',
	          'Year']:
		try:
			del dict[k]
		except KeyError:
			continue
		except AttributeError:
			continue
