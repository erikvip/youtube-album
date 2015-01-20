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

	

	text_header = (u"Welcome to the urwid tour!  "
		u"UP / DOWN / PAGE UP / PAGE DOWN scroll.  F8 exits.")	

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
	main()

