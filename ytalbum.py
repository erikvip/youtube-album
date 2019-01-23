#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "0.2.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"


import os
import sys
import pprint
import logging
import urllib
import time


#from urllib2 import build_opener
from urllib2 import build_opener, HTTPError, URLError
uni, byt, xinput = unicode, str, raw_input

import atexit

# from PyQt4 import QtGui

# Ensure lib added to path, before any other imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/'))

# Included libs
import musicbrainzngs as mb
#import pafy
#import ytalbumgui as gui
#from feedparser import *

from pprint import pprint
import json


def utf8_encode(x):
    """ Encode Unicode. """
    return x.encode("utf8") if type(x) == uni else x


def utf8_decode(x):
    """ Decode Unicode. """
    return x.decode("utf8") if type(x) == byt else x


logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(message)s')


def main(searchKeyword):
	yta = YtAlbum()
	#yta.query = 'Anjali - Anjali'
	yta.query = searchKeyword
	res = yta.findRelease()

class YtAlbum:
	def __init__(self):
		# Setup urllib2 opener
		opener = build_opener()
		ua = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; "
		ua += "Trident/5.0)"
		opener.addheaders = [("User-Agent", ua)]
		self.urlopen = opener.open

	def findRelease(self):
		name = self.query
		logging.info("Search query: %s" % name)
		
		results = []

		limit = 1

		chars = set('!?*')
		if any((c in chars) for c in name):
		    name = '"'+name+'"'
		    
		mb.set_useragent("YtAlbum","0.0","https://youtube.com")
		res = mb.search_releases(query='artist:'+name,limit=limit)

		for a in res['release-list']:
			album = {
				'id': a['id'], 
				'artist': a['artist-credit-phrase'], 
				'date': a['date'], 
				'country': a['country'], 
				'status': a['status'], 
				'title' : a['title'],
				'tracks' : []
			}

			print "Artist: %(artist)s Album: %(title)s  Release Date: %(date)s" % (album)

			disc = mb.get_release_by_id(a['id'], ["media","recordings"])

			for d in disc['release']['medium-list']:
				
				for t in d['track-list']:

					# Convert recording time to Minutes:Seconds
					time = int(t['length']) / 1000
					minutes = time/60
					seconds = str(time%60)[:2].zfill(2)

					# Cover art
					#coverartarchive.org/release/95069c41-9f93-4473-a4a7-8722f14fb2c4/back

					logging.info("  Disc #%s Track #%s %s" % ( d['position'], t['position'], t['recording']['title'].encode('ascii', 'ignore') ))

					query = '"%s" "%s"' % ( album['artist'], t['recording']['title'].encode('ascii', 'ignore') )
					logging.info("Youtube search query: %s" % query)

					# Youtube Search API URL
					apikey1 = 'AIzaSyCCY9n5yMzLOEbkIldSTvpJ4Wb5hvoqcsk'
					apikey2 = 'AIzaSyCWZeDpW5W2llplhc6RaS77kUM_xvx5hTY'
					apikey3 = 'AIzaSyBJVgNp6W_Jh_S4QwhwZvBVKx-hM8g7kd8'
					apikey4 = 'AIzaSyAQgN0Q1zhBckI8CxR3lgogMBRT1eCmNms'

					url = 'https://www.googleapis.com/youtube/v3/search?q=%(query)s&key=%(key)s&part=%(part)s' % (
						{
							'query': urllib.quote_plus(query), 
							'key': apikey1, 
							'part' : 'snippet'
						} )


					try:
						resp = self.urlopen(url).read()
					except HTTPError as err:
						logging.error("Download failed. HTTP Error %s %s" % (err.code, err.msg))
						print(err.code)
						print err.msg
						sys.exit(1)					

					data = json.loads(resp)

					id=data["items"][0]['id']['videoId']
					title=data["items"][0]['snippet']['title'].encode('ascii', 'ignore')
					print "%s %s" % (id, title)

					print "https://www.youtube.com/watch?v=%s" % (id)
				
				# Tracks loop
			# Disc loop
			results.append(album)

		return results
				

# main() when invoked from the shell
if __name__ == '__main__':
	
	if len(sys.argv) <= 1 or sys.argv[1] is None: 
		logging.error("Must specify Artist / Album search keyword");
		sys.exit(1)

	main(sys.argv[1])
