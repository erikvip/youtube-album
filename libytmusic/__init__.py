#!/usr/bin/env python
"""
Youtube tools for supporting ytmusic

This library provides youtube-specific functions for ytmusic. 
Currently provides the following functionality:

* Youtube video searching / paging
* Matching an album based on title and track length

https://github.com/erikvip

"""

__version__ = "0.0.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"


import pprint
import logging
import sys
from feedparser import *

if sys.version_info[:2] >= (3, 0):
	from urllib.parse import urlencode
else:
	from urllib import urlencode


class yttools:
	""""Youtube Tools - search and album matching"""

	def search(self, query, **kwa):
		"""
			Search youtube
			Provides an interface to the XML search api at:
			https://gdata.youtube.com/feeds/api/videos?q={query}

			Required arguments:
			query -- The search keyword

			Optional keyword arguments:

			orderby (string): Order by clause
			startIndex (int): Starting result (default: 1)
			maxResults (int): Maximum results to return (default: 25, maximum: 50)
			hd (bool): Set to true to return only HD videos, 720p or better. (Default: false)

			For more details, see:
			https://developers.google.com/youtube/2.0/developers_guide_protocol_api_query_parameters
		"""
		url = "https://gdata.youtube.com/feeds/api/videos"

		qargs = dict(
			v=2,
			q=query,
			hd=kwa.get("hd", False),
			orderby=kwa.get("orderby", "relevance")
		)
		
		# These argument keys must be quoted...
		qargs["start-index"] = kwa.get("startIndex", 1)
		qargs["max-results"] = kwa.get("maxResults", 25)

		# HD paramater must be absent for False, or "true" for True (lowercase)
		if qargs["hd"] == False: 
			del qargs["hd"]
		else:
			qargs["hd"] = "true"
 
		logging.info("Search arguments: %s" % qargs)

		queryString = [(k, qargs[k]) for k in sorted(qargs.keys())]
		url = "%s?%s" % (url, urlencode(queryString))

		logging.info("Search URL: %s" % url)

		# Fetch the youtube search results
		result = feedparser.parse(url)

		logging.info("Youtube search results: %s" % result)
		
		if result["status"] != 200:
			raise IOError("Youtube search failure")

		return result['entries']
		

if __name__ == '__main__':
	yt = yttools()
	res = yt.search("Aphex twin", hd=True)

	for v in res:
		pprint.pprint(v)
	print res


