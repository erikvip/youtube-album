#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "0.1.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"


import os
import sys
import pprint
import logging
import urllib

from PyQt4 import QtGui

# Ensure lib added to path, before any other imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/'))

# Included libs
import musicbrainzngs as mb
import pafy
import ytalbumgui as gui
from feedparser import *

logging.basicConfig(level=logging.INFO)


def main():
	yta = YtAlbum()
	yta.query = 'Aphex twin On'
	res = yta.findRelease()

	#print res['title']

	for r in res:
		print r['title']
	#	pprint.pprint(r)
	#pprint.pprint(res)

class YtAlbum:

	def findRelease(self):

		#artistlist = []
		#artistResults = None

		name = self.query
		
		results = []

		#name = 'Aphex Twin classics'
		limit = 1

		chars = set('!?*')
		if any((c in chars) for c in name):
		    name = '"'+name+'"'
		    
		mb.set_useragent("YtAlbum","0.0","https://youtube.com")
		res = mb.search_releases(query='artist:'+name,limit=limit)

		for a in res['release-list']:
			#print a['id'], a['title'], a['artist-credit-phrase'], a['date'], a['country'], a['status']
			album = {
				'id': a['id'], 
				'artist': a['artist-credit-phrase'], 
				'date': a['date'], 
				'country': a['country'], 
				'status': a['status'], 
				'title' : a['title'],
				'tracks' : []
			}
			
			logging.info('Found release: \n\
				Artist: %(artist)s \n\
				Title: %(title)s \n\
				Album_id: %(id)s \n\
				date: %(date)s country: %(country)s status: %(status)s' % album )

			disc = mb.get_release_by_id(a['id'], ["media","recordings"])

			for d in disc['release']['medium-list']:
				#pprint.pprint(d)
				for t in d['track-list']:
					# Convert recording time to Minutes:Seconds
					time = int(t['length']) / 1000
					minutes = time/60
					seconds = str(time%60)[:2].zfill(2)
					
					# Cover art
					#coverartarchive.org/release/95069c41-9f93-4473-a4a7-8722f14fb2c4/back

					query = '"%s" "%s"' % ( album['artist'], t['recording']['title'].encode('ascii', 'ignore') )

					# Youtube Search API URL
					url = 'https://gdata.youtube.com/feeds/api/videos?q=%s&v=2&hd=true' % urllib.quote_plus(query)
					#print url

					track = {
						'position': str(t['position']), 
						'title' : t['recording']['title'].encode('ascii', 'ignore'),
						'duration' : "%i:%s" % (minutes, seconds), 
						'seconds' : time, 
						'api_url' : url
					}

					logging.info('Track #%(position)s \tDuration: %(duration)s [%(seconds)ss] \t%(title)s \tAPI URL: %(api_url)s' % track)

					# Fetch the youtube search results
					ytres = feedparser.parse(url)

					# Possible Youtube Sources
					sources = []

					for y in ytres['entries']:

						s = y['yt_duration']['seconds']; 
						title = y['title'].encode('ascii', 'ignore')
						vidurl = "https://www.youtube.com/watch?v=%s" % y['yt_videoid']

						if ( abs(int(time) - int(s)) >  10 ):
							logging.debug('Skipping source. Duration mismatched. Wanted: %s Got: %s\t %s \t %s' % (time, s, title, vidurl) )
							continue
						else:

							# Example fetch audio only:
							#vid = pafy.new(vidurl)
							#audio = vid.getbestaudio()
							#audiofile = audio.download(filepath='/home/ephillips/tmp/')

							src = {
								'title': title, 
								'duration': s, 
								'seconds': time, 
								'hd': y['yt_hd'], 
								'videoid': y['yt_videoid'], 
								'url' : vidurl
							}

							logging.info('Possible source found: %(duration)ss %(url)s\t %(title)s' % src )

							sources.append( src )

						# Valid source 
					# Sources loop	
					track['sources'] = sources
					album['tracks'].append(track);
					
				# Tracks loop
			# Disc loop
			results.append(album)
		# Album loop

		return results
				
# Query for Album / Artists by name
#def findReleaseByName(name):



# main() when invoked from the shell
if __name__ == '__main__':

	main()
'''
	app = QtGui.QApplication(sys.argv)

	main_window = gui.YtAlbumGuiMain()
	main_window.show()
	# Enter the main loop
	app.exec_()
'''


	