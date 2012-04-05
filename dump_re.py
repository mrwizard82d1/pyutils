"""A debugging utility for regular expressions."""


from __future__ import print_function


import re


def dump_results(match_obj, text):
	"""Print the match object results."""
	if match_obj:
		print('{}<{}>{}'.format(text[:match_obj.start()],
								text[match_obj.start(): match_obj.end()],
								text[match_obj.end():]))
	else:
		print('No match.')

	
def search(pattern, text, flags=0):
	"""Print the results of searching text for pattern with flags."""
	match_obj = re.search(pattern, text, flags)
	dump_results(match_obj, text)


def match(pattern, text, flags=0):
	"Print the results of matching text for pattern with flags."""
	match_obj = re.match(pattern, text, flags)
	dump_results(match_obj, text)
