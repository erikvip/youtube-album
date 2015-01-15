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

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

def main():
	# Main handler

	choices = u'One Two Three'.split()

	palette = [
        ('body','white','black', 'standout'),
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
	walker = urwid.SimpleListWalker([urwid.AttrMap(urwid.Button(w), 'buttn', 'buttnf') for w in text_cb_list])
	listbox_content = [
		#urwid.BoxAdapter(urwid.Filler(urwid.Pile([urwid.AttrWrap(urwid.CheckBox(txt),'buttn','buttnf') for txt in text_cb_list])), 10),
		urwid.BoxAdapter(
				urwid.ListBox(
					walker
		), 3),
		urwid.AttrWrap(urwid.Edit("", "wtf", align='left'), 'editbx', 'editfc' ),
	]
	
	head = urwid.Text(text_header)
	header = urwid.AttrWrap(head, 'header')
	listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
	frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)	


	if urwid.web_display.is_web_request():
		screen = urwid.web_display.Screen()
	else:
		screen = urwid.raw_display.Screen()

	def unhandled(key):
		if key == 'f8':
			raise urwid.ExitMainLoop()
		if key == "f7":
			walker[:] = [urwid.AttrMap(urwid.Button(w), 'buttn', 'buttnf') for w in text_cb_list_two] 
		if key == "f6":
			walker[:] = []

		#head.set_text("Key pressed: %s" % key)
		




	urwid.MainLoop(frame, palette, screen,
		unhandled_input=unhandled, pop_ups=True).run()






# main() when invoked from the shell
if __name__ == '__main__':
	main()

