#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "0.2.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"


import os
import sys
#import traceback
import pprint
import logging
import urllib
import time
import StringIO

#from urllib2 import build_opener
from urllib2 import build_opener, HTTPError, URLError

import atexit

# from PyQt4 import QtGui

# Ensure lib added to path, before any other imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/'))

# Included libs
import musicbrainzngs as mb
import pafy
#import ytalbumgui as gui
from feedparser import *

from pprint import pprint

from xml.etree import ElementTree as ET

import json

uni, byt, xinput = unicode, str, raw_input

def utf8_encode(x):
    """ Encode Unicode. """
    return x.encode("utf8") if type(x) == uni else x


def utf8_decode(x):
    """ Decode Unicode. """
    return x.decode("utf8") if type(x) == byt else x


#logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(message)s')


def main():

	yta = YtAlbum()
	#yta.query = 'Anjali - Anjali'
	yta.query = "tracy bonham - the burdens of being upright"
	res = yta.findRelease()

#	time.sleep(5)

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
		

		#statusUpdate("Search keywords:  " + name)

		print "Search string: %s" % ( name )

		results = []

		#name = 'Aphex Twin classics'
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

#			win.addstr(2, 1, "Artist: " + album['artist'])
#			win.addstr(3, 1, "Title: %(title)s [%(id)s]" % album )
#			win.addstr(4, 1, "Release Date: %(date)s Country: %(country)s Status: %(status)s" % album)
#			win.refresh()
#			disc = mb.get_release_by_id(a['id'], ["media","recordings"])
#			statusUpdate("Processing album %(title)s" % album)

			disc = mb.get_release_by_id(a['id'], ["media","recordings"])

			for d in disc['release']['medium-list']:
				
				for t in d['track-list']:

					# Convert recording time to Minutes:Seconds
					time = int(t['length']) / 1000
					minutes = time/60
					seconds = str(time%60)[:2].zfill(2)
					#pprint(d)

					# Cover art
					#coverartarchive.org/release/95069c41-9f93-4473-a4a7-8722f14fb2c4/back

					print "  Disc #%s Track #%s %s" % ( d['position'], t['position'], t['recording']['title'].encode('ascii', 'ignore') )

					query = '"%s" "%s"' % ( album['artist'], t['recording']['title'].encode('ascii', 'ignore') )

					# Youtube Search API URL
#					url = 'https://gdata.youtube.com/feeds/api/videos?q=%s&v=2&hd=true' % urllib.quote_plus(query)
#					AIzaSyCCY9n5yMzLOEbkIldSTvpJ4Wb5hvoqcsk
#					url = 'https://www.googleapis.com/youtube/v3/search?q=%s&v=2&hd=true' % urllib.quote_plus(query)
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


					#print url
					
#					opener = urllib.request.build_opener()
#					pprint(opener)
					try:
						resp = self.urlopen(url).read()
					except HTTPError as err:
						print(err.code)
						print err.msg
						sys.exit(1)					
#						resp = os.popen("./ytscrape.sh \"%s\"" % query).read()
						#print(resp)

#					for l in resp.split("\n"):
#						id=l[1:12]
#						title=l[12:]
#						print title




					#sys.exit(1)
					#data = ET.fromstring(utf8_encode(resp))

					data = json.loads(resp)

					id=data["items"][0]['id']['videoId']
					title=data["items"][0]['snippet']['title'].encode('ascii', 'ignore')
					print "%s %s" % (id, title)

					print "https://www.youtube.com/watch?v=%s" % (id)
					#pprint(data)
#					for v in data['items']:
#						if v['id']['kind'] == 'youtube#video':
#							print "    %s - %s" % (v['id']['videoId'], v['snippet']['title'])





#					track = {
#						'position': str(t['position']), 
#						'title' : t['recording']['title'].encode('ascii', 'ignore'),
#						'duration' : "%i:%s" % (minutes, seconds), 
#						'seconds' : time, 
#						'api_url' : url, 
#						'query' : query
#					}

					# Fetch the youtube search results
#					ytres = feedparser.parse(url)

					#pprint(ytres)

					# Possible Youtube Sources
					sources = []

#					track['sources'] = sources
#					album['tracks'].append(track);
					
				# Tracks loop
			# Disc loop
			results.append(album)

		return results
				

# main() when invoked from the shell
if __name__ == '__main__':

	# Catch exceptions here and output them in curses
	main()
	#try:
		

	#except Exception, err:
		 		
 	#	sys.exit(1)
 
#	time.sleep(5000)
