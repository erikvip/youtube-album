#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "0.0.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"


import os
import sys
import pprint
import logging
import traceback
import atexit
# Requires
import urwid
import urwid.raw_display
import urwid.web_display
import nobsmusicbrainzapi as mbapi
from libytmusic import yttools


class YtMusicCurses:

	palette = [
		('body','white','black', 'standout'),
		('listbox', 'white', 'black'),
		('infobox', 'white', 'black'),
		('reverse','light gray','black'),
		('header','black','light green', 'bold'),
		('important','dark blue','light gray',('standout','underline')),
		('editfc','white', 'dark blue', 'bold'),
		('editbx','light gray', 'dark blue'),
		('editcp','black','light gray', 'standout'),
		('bright','dark gray','light gray', ('bold','standout')),
		('buttn','black','dark cyan'),
		('buttnf','white','dark blue','bold'),
	]

	def __init__(self):
		self.initLogging()

		# Music Brainz startup
		self.mb = mbapi.nobsmusicbrainzapi()

		# Youtube tools
		self.yt = yttools()

		# Default is youtube search
		self.mode = self._youtubeSearch

	def initLogging(self):
		'''Start up logging module'''
		logging.getLogger('').handlers = []
		logging.basicConfig(
			level=logging.INFO, 
			#format='%(asctime)s %(message)s',
			filename="/tmp/ytmusic.log", 
			filemode="a"
		)
		self.log = logging.getLogger("ytmusic-curses")
		self.log.info("Started logging")

	def main(self):
		'''Main widget init and startup the urwid curses loop'''

		self.text_header = (u"Youtube Music v%s | "
			#u"UP / DOWN / PAGE UP / PAGE DOWN scroll.  F8 exits." 
			u"F5: Youtube Search | F6: Artist/Album Search"
			% __version__)	

		self.walker = urwid.SimpleListWalker([])

		urwid.connect_signal( self.walker, 'modified', self.listSelect )
		
		self.search = urwid.Edit("Youtube Search: ", "", align='left')
		self.info = urwid.Text("")

		self.infobox = urwid.BoxAdapter(urwid.AttrWrap(urwid.LineBox(urwid.ListBox( [self.info]  )), 'infobox'),10)
		self.listbox = urwid.BoxAdapter(urwid.AttrWrap(urwid.ListBox(self.walker), 'listbox'),10)

		self.columns = urwid.Columns([self.listbox])

		self.listbox_content = [
			self.columns,
			urwid.AttrWrap(self.search, 'editbx', 'editfc' ),
		]
		
		self.header = urwid.Text(self.text_header)
		self.header_wrapper = urwid.AttrWrap(self.header, 'header')
		
		self.container = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))

		self.frame = urwid.Frame(urwid.AttrWrap(self.container, 'body'), header=self.header_wrapper)	

		if urwid.web_display.is_web_request():
			self.screen = urwid.web_display.Screen()
		else:
			self.screen = urwid.raw_display.Screen()

		# Main loop
		urwid.MainLoop(self.frame, self.palette, self.screen,
			unhandled_input=self._frameInput, pop_ups=True).run()

	def listSelect(self):
		item = self.walker.get_focus()[0].base_widget.youtube

		#from pudb import set_trace; set_trace()
		#self.log.info("listSelect: %s" % item.title) 
		# Update the info box
		self.info.set_text("%s\r\n\r\n%s" % (item['title'], item['media_group']) )

	def _frameInput(self, key):
		'''Unhandled input for the main frame'''
		self.log.info("Frame Input: %s" % key)

		if key == "f5":
			self.mode=self._youtubeSearch
			self.search.set_caption("Youtube search: ")

		if key == "f6":
			self.mode = self._artistSearch
			self.search.set_caption("Artist search: ")

		if key == "f7":
			self.log.info("Current mode: %s" % self.mode)
			# Toggle info window
			w = self.columns._get_widget_list()

			if ( len(w) == 1 ):
				self.columns._set_widget_list([ self.listbox, self.infobox ])
			else:
				self.columns._set_widget_list([ self.listbox ])


		# Perform search
		if key == "enter":
			queryString = self.search.edit_text
			self.log.info("Search queryString: %s" % queryString)

			if len(queryString) > 0:
				self.mode(queryString)


	def _artistSearch(self, queryString):
		self.log.info("Album search: %s " % queryString)
		self.header.set_text("Artist search for: %s" % queryString)
		artists = self.mb.search_artist(queryString)
		self.log.info("Search results: %s" % artists)

		items = []
		for a in artists:
			button = urwid.Button(a['name'])
			button.arid = a['arid']
			button.name = a['name']
			urwid.connect_signal(button, 'click', self._artistSelected)
			items.append(urwid.AttrMap(button, 'buttn', 'buttnf'))

		self.walker[:] = items


	def _youtubeSearch(self, queryString):
		self.log.info("Youtube search: %s " % queryString)
		self.header.set_text("Youtube search results for: %s" % queryString)
		results = self.yt.search(queryString)

		items = []
		for r in results:
			button = urwid.Button(r['title'])
			button.youtube = r
			urwid.connect_signal(button, 'click', self._youtubeResultSelected)
			items.append(urwid.AttrMap(button, 'buttn', 'buttnf'))
		self.walker[:] = items


	def _youtubeResultSelected(self, button):
		vid = button.youtube
		self.log.info("Youtube Result Selected: %s" % vid)


	def _artistSelected(self, button):
		'''An artist has been selected. Do an album search'''
		arid = button.arid
		name = button.name
		self.log.info("Item selected = %s, arid = %s, name = %s" % (button, arid, name))

		# Now do an album search 
		albums = self.mb.search_album(arid=arid)
		self.log.info("Album search results: %s" % albums)

		self.header.set_text("Showing albums by %s" % name)

		items = []
		for a in albums:
			button = urwid.Button(a['title'])
			button.album = a
			urwid.connect_signal(button, 'click', self._albumSelected)
			items.append(urwid.AttrMap(button, 'buttn', 'buttnf'))
		self.walker[:] = items

	def _albumSelected(self, button):
		'''An artist / album has been selected.  List tracks'''
		album = button.album
		self.log.info("Album selected: %s" % album)
		self.header.set_text("Album: %s" % album['title'])

		tracks = self.mb.get_album(album['aid'])
		self.log.info("Track search results: %s" % tracks)




def main():
	# Main handler

	logging.getLogger('').handlers = []
	logging.basicConfig(
		level=logging.INFO, 
		#format='%(asctime)s %(message)s',
		filename="/tmp/ytmusic.log", 
		filemode="a"
	)
	log = logging.getLogger("ytmusic-curses")
	log.info("Started logging")


	# Music Brainz search api
	mb = mbapi.nobsmusicbrainzapi()

	palette = [
        ('body','white','black', 'standout'),

#		('listbox', 'white', 'dark blue'),
#        ('infobox', 'white', 'dark green'),

		('listbox', 'white', 'black'),
        ('infobox', 'white', 'black'),

        ('reverse','light gray','black'),
        ('header','black','light green', 'bold'),
        ('important','dark blue','light gray',('standout','underline')),
        ('editfc','white', 'dark blue', 'bold'),
        ('editbx','light gray', 'dark blue'),
        ('editcp','black','light gray', 'standout'),
        ('bright','dark gray','light gray', ('bold','standout')),
        ('buttn','black','dark cyan'),
        ('buttnf','white','dark blue','bold'),
        ]

	

	text_header = (u"Youtube Music %s " 
		u"UP / DOWN / PAGE UP / PAGE DOWN scroll.  F8 exits." % __version__)	

	text_cb_list = [u"Abc", u"def", "asdf"]
	text_cb_list_two = [u"Abaaa", u"bbb", "zzz"]
#	pile = urwid.Pile([urwid.AttrWrap(urwid.CheckBox(txt),'buttn','buttnf') for txt in text_cb_list])
#	fil = urwid.Filler(pile)

	#walker = urwid.SimpleListWalker([urwid.AttrMap(urwid.Button(w), 'buttn', 'buttnf') for w in text_cb_list])
	walker = urwid.SimpleListWalker([])
	

	search = urwid.Edit("Artist Search: ", "", align='left')
	#urwid.connect_signal(search, 'change', handleSearch)
	
	#infobox = urwid.LineBox(urwid.Text("asdf"))
	infobox = urwid.BoxAdapter(urwid.AttrWrap(urwid.LineBox(urwid.ListBox( [urwid.Text("Asdf")]  )), 'infobox'),10)
	listbox = urwid.BoxAdapter(urwid.AttrWrap(urwid.ListBox(walker), 'listbox'),10)

	#columns = urwid.Columns([listbox, (0,infobox) ])
	columns = urwid.Columns([listbox])

	listbox_content = [
		#urwid.BoxAdapter(urwid.Filler(urwid.Pile([urwid.AttrWrap(urwid.CheckBox(txt),'buttn','buttnf') for txt in text_cb_list])), 10),
		#urwid.BoxAdapter(urwid.ListBox(walker), 10),
		#urwid.Columns([
			#urwid.BoxAdapter(urwid.ListBox(walker), 10), 
			
	#		urwid.AttrWrap(infobox, 'infobox'),
		#]),
		#listbox,
		columns,
		urwid.AttrWrap(search, 'editbx', 'editfc' ),
	]
	
	head = urwid.Text(text_header)
	header = urwid.AttrWrap(head, 'header')
	
	container = urwid.ListBox(urwid.SimpleListWalker(listbox_content))


	frame = urwid.Frame(urwid.AttrWrap(container, 'body'), header=header)	


	if urwid.web_display.is_web_request():
		screen = urwid.web_display.Screen()
	else:
		screen = urwid.raw_display.Screen()

	def album_selected(button):
		album = button.album
		logging.info("Album selected: %s" % album)
		head.set_text("Album: %s" % album['title'])

		tracks = mb.get_album(album['aid'])
		logging.info("Track search results: %s" % tracks)




	def artist_selected(button):
		arid = button.arid
		name = button.name
		logging.info("Item selected = %s, arid = %s, name = %s" % (button, arid, name))
		# Now do an album search 
		albums = mb.search_album(arid=arid)
		logging.info("Album search results: %s" % albums)

		head.set_text("Showing albums by %s" % name)

		items = []
		for a in albums:
			button = urwid.Button(a['title'])
			button.album = a
			urwid.connect_signal(button, 'click', album_selected)
			items.append(urwid.AttrMap(button, 'buttn', 'buttnf'))

			#items.append(a['title'])
		#walker[:] = [urwid.AttrMap(urwid.Button(w), 'buttn', 'buttnf') for w in items] 
		walker[:] = items



	def unhandled(key):
		logging.info("Key press: %s" % key)
		if key == 'f8':
			raise urwid.ExitMainLoop()
		if key == "f7":
			walker[:] = [urwid.AttrMap(urwid.Button(w), 'buttn', 'buttnf') for w in text_cb_list_two] 
		if key == "f6":

			w = columns._get_widget_list()

			#log.info("Columns widget list: %s" % w)
			if ( len(w) == 1 ):
				columns._set_widget_list([ listbox, infobox ])
			else:
				columns._set_widget_list([ listbox ])

		if key == "enter":
#			from pudb import set_trace; set_trace()

			queryString = search.edit_text
			log.info("Search queryString: %s" % queryString)

			if len(queryString) > 0:
				head.set_text("Artist search for: %s" % queryString)
				artists = mb.search_artist(queryString)
				log.info("Search results: %s" % artists)

				items = []
				for a in artists:
					button = urwid.Button(a['name'])
					button.arid = a['arid']
					button.name = a['name']
					urwid.connect_signal(button, 'click', artist_selected)
					items.append(urwid.AttrMap(button, 'buttn', 'buttnf'))


				#walker[:] = [urwid.AttrMap(urwid.Button(w), 'buttn', 'buttnf') for w in items] 
				walker[:] = items
		

	

	urwid.MainLoop(frame, palette, screen,
		unhandled_input=unhandled, pop_ups=True).run()






# main() when invoked from the shell
if __name__ == '__main__':
	#main()
	app = YtMusicCurses()
	app.main()

