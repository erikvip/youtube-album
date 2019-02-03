#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Assemble and download mp3 albums from individual youtube videos

Usage:
	ytalbum.py [-id] COMMAND SEARCHKEYWORD

Depending on COMMAND, this will Search for albums by an artist, List the youtube URLS for each album track, or Download each track using youtube-dl

Arguments:
	COMMAND 		Search, List, or Download
	SEARCHKEYWORD 		The Artist+Album, or just Artist search string

Options:
  -i		Interactive mode
  -d 		Enable debug logging
  -h, --help 		Show help
"""

#Assemble and download mp3 albums from individual youtube videos

#Depending on COMMAND, this will Search for albums by an artist, List the youtube URLS for each album track, or Download each track using youtube-dl


__version__ = "0.2.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"


import os
import sys
import pprint
import logging
import urllib
import time

#from docopt import docopt
import argparse
#from urllib2 import build_opener
from urllib2 import build_opener, HTTPError, URLError
uni, byt, xinput = unicode, str, raw_input

import atexit

# from PyQt4 import QtGui

# Ensure lib added to path, before any other imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/'))

# Included libs
import shelve
import musicbrainzngs as mb
import musicbrainzngs.cache

cache = musicbrainzngs.cache.DictCache()
musicbrainzngs.set_cache(cache)


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


def mainold(action, searchKeyword):
	yta = YtAlbum()
	#yta.query = 'Anjali - Anjali'
	yta.query = searchKeyword
	#res = yta.findRelease()


def main(args):
	yta =YtAlbum()

	r = yta.listArtists('Guns and roses');
	pprint(r)
	sys.exit(1)

	artist = yta.listArtists(args.artist, 1)[0]
	if args.action=='list':
		res = mb.search_releases(query=args.album, artistname=args.artist, country='US', limit=20)
		yta.showReleaseList(res['release-list'])

	elif args.action=='search':
		# Artist search
		if args.album == None:
			res = yta.listArtists(args.artist)
		else:
			res = mb.search_releases(query=args.album, artistname=args.artist, limit=20)	
			yta.showReleaseList(res['release-list'])


#	yta.listReleasesByArtist(artist)	
	res = mb.search_releases(query=args.album, artistname=args.artist, limit=1)
	#res = yta.showReleaseList(res['release-list'])
#	pprint(res)
	#res = mb.get_release_by_id()
	disc = mb.get_release_by_id(res['release-list'][0]['id'], ["media","recordings"])
	#disc = mb.get_release_by_id(res['release-list'][0]['id'], ["media"])
#	pprint(disc)

class YtAlbum:
	def __init__(self):
		# Setup urllib2 opener
		opener = build_opener()
		ua = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; "
		ua += "Trident/5.0)"
		opener.addheaders = [("User-Agent", ua)]
		self.urlopen = opener.open

		mb.set_useragent("YtAlbum","0.0","https://youtube.com")

	def search_releases(self, query, limit=10):
		res = mb.search_releases(query=query, limit=limit)
		return res
	def search_release_groups(self, query, limit=10):
		res = mb.search_release_groups (query=query, limit=limit)
		return res


	def get_release_by_id(self, id):
		disc = mb.get_release_by_id(id, ["media","recordings"])
		return disc

	def get_release_group_by_id(self, id):
		disc = mb.get_release_group_by_id(id, ["media","recordings"])
		return disc


	def showReleaseList(self, releaseList):
		for b in releaseList:
			c=dict(b)
			if not c.has_key('country'): c['country']='N / A'
			if not c.has_key('date'): c['date']='Unknown'
			c['title'] = c['title'].encode('ascii', 'ignore')
		
			try:
				print ("%(artist-credit-phrase)s"
					+" - %(title)s [%(country)s]"
					+" [%(date)s] Discs:%(medium-count)s") % c
			except KeyError:
				pprint(c);
				sys.exit(1)


	def listArtists(self, artist, limit=10):
		logging.info("Getting artist list for keyword: %s" % artist)
		res=mb.search_artists(query=artist, limit=limit)
		for a in res['artist-list']:
			logging.debug("Found artist: %(name)s" % a)

		return res['artist-list']

	def listReleasesByArtist(self, artist, limit=20):
		logging.info("Getting release list for artist %(name)s, id:%(id)s " % artist)
		res = mb.search_releases(arid=artist['id'], limit=limit)
		for b in res['release-list']:
			logging.debug("Found release: %(title)s" % b)
		return res['release-list']

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
		pprint(res)
		sys.exit(1)

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

			#print "Artist: %(artist)s Album: %(title)s  Release Date: %(date)s" % (album)
			logging.info("Artist: %(artist)s Album: %(title)s  Release Date: %(date)s" % (album))

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

#					query = '"%s" "%s"' % ( album['artist'], t['recording']['title'].encode('ascii', 'ignore') )
					query = '%s %s' % ( album['artist'], t['recording']['title'].encode('ascii', 'ignore') )
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
					id = 0
					for v in data['items']:
						if v['id']['kind'] == 'youtube#video':
							id=v['id']['videoId']
							title=v['snippet']['title'].encode('ascii', 'ignore')
							break

					if id == 0:
						logging.error("No matching video found")
						pprint(data)
						sys.exit(1)

					#id=data["items"][0]['id']['videoId']
					#title=data["items"][0]['snippet']['title'].encode('ascii', 'ignore')
					print "%s %s" % (id, title)

					print "https://www.youtube.com/watch?v=%s" % (id)
				
				# Tracks loop
			# Disc loop
			results.append(album)

		return results
				

# main() when invoked from the shell
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('action', choices=['search', 'list', 'download'], 
		help="The action to take (e.g. search, list, download)")
	parser.add_argument('artist',  help='Artist Search Keyword')
	parser.add_argument('album',  help='Artist Search Keyword')


	parser.add_argument('-i', '--interactive', action='store_true')
	parser.add_argument('-d', '--debug', action='store_true')


	args = parser.parse_args()

	if args.debug == True:
		logging.getLogger().setLevel(logging.DEBUG);

	logging.debug(args)
	
	#main(args.action, args.keyword)
	main(args)
