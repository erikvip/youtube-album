#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = '0.1.1'

__authors__ = (
	'Erik Phillips'
)

__license__ = 'GPL'


import os
import sys
import pprint
import requests

# Ensure lib added to path, before any other imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/'))

# Included libs
import musicbrainzngs as mb
import pafy
from feedparser import *

def main():

	artistlist = []
	artistResults = None

	name = 'Aphex Twin classics'
	limit = 5

	chars = set('!?*')
	if any((c in chars) for c in name):
	    name = '"'+name+'"'
	    
	mb.set_useragent("headphones","0.0","https://github.com/rembo10/headphones")
	res = mb.search_releases(query='artist:'+name,limit=limit)

	for a in res['release-list']:
		print a['id'], a['title'], a['artist-credit-phrase'], a['date'], a['country'], a['status']

		disc = mb.get_release_by_id(a['id'], ["media","recordings"])

		for d in disc['release']['medium-list']:
			for t in d['track-list']:
				# Convert recording time to Minutes:Seconds
				time = int(t['length']) / 1000
				minutes = time/60
				seconds = str(time%60)[:2].zfill(2)
				
				# Cover art
				#coverartarchive.org/release/95069c41-9f93-4473-a4a7-8722f14fb2c4/back

				trackPosition = t['position']
				trackTitle = t['recording']['title']

				print t['position'], t['recording']['title'].encode('ascii', 'ignore'), "%i:%s" % (minutes, seconds)

				# Youtube Search API URL
				url = 'https://gdata.youtube.com/feeds/api/videos?q=%s&v=2&hd=true' % trackTitle.encode('ascii', 'ignore')

				# Fetch the youtube search results
				ytres = feedparser.parse(url)

				for y in ytres['entries']:
					ytTitle = y['title'].encode('ascii', 'ignore')
					ytDuration = y['yt_duration']['seconds']
					ytHd = y['yt_hd']
					ytVideoid = y['yt_videoid']
					print "Title:%s Duration:%s Total:%s Hd:%s vid:%s" % (ytTitle, ytDuration, time, ytHd, ytVideoid)

					vidurl = "https://www.youtube.com/watch?v=%s" % ytVideoid

					vid = pafy.new(vidurl)
					audio = vid.getbestaudio()

					audiofile = audio.download(filepath='/home/ephillips/tmp/')

					print audiofile

					exit(1)
				exit(1)

# main() when invoked from the shell
if __name__ == '__main__':
	main()
