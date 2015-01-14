#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "0.0.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"


import os
import sys
import pprint
import logging
import curses
import traceback
import atexit
# Requires
import urwid
import urwid.raw_display
import urwid.web_display

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(message)s')

def main():
	# Main handler

	choices = u'One Two Three'.split()

	main = urwid.Padding(menu(u'Pythons', choices), left=2, right=2)
	inp =  urwid.Text(('bold', u"stuff"), 'right', 'any')

	top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
	    align='center', width=('relative', 60),
	    valign='middle', height=('relative', 60),
	    min_width=20, min_height=9)

	#urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

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
	pile = urwid.Pile([urwid.AttrWrap(urwid.CheckBox(txt),'buttn','buttnf') for txt in text_cb_list])
	fil = urwid.Filler(pile)
	walker = urwid.SimpleListWalker([urwid.AttrMap(urwid.Button(w), 'buttn', 'buttnf') for w in text_cb_list])

	listbox_content = [
		#urwid.Padding(menu(u'Pythons', choices), left=2, right=2),
		#urwid.Padding(urwid.Text(text_listbox), left=0, right=0, min_width=20),
		#urwid.Padding(urwid.GridFlow([urwid.AttrWrap(urwid.CheckBox(txt),'buttn','buttnf') for txt in text_cb_list],10, 0, 1, 'left') ,left=4, right=3, min_width=10),
		#urwid.Filler(urwid.Pile([urwid.AttrWrap(urwid.CheckBox(txt),'buttn','buttnf') for txt in text_cb_list])),
		#urwid.BoxAdapter(urwid.Filler(urwid.Pile([urwid.AttrWrap(urwid.CheckBox(txt),'buttn','buttnf') for txt in text_cb_list])), 10),
		#urwid.BoxAdapter(fil, 10),
		urwid.BoxAdapter(
				urwid.ListBox(
					walker
		), 3),

		#urwid.BoxAdapter(urwid.Filler(urwid.Padding(PopUpDialog(), 'center', 15)), 5),
		urwid.AttrWrap(urwid.Edit("", "wtf", align='left'), 'editbx', 'editfc' ),
	]

	head = urwid.Text(text_header)
	header = urwid.AttrWrap(head, 'header')
	#header = urwid.Columns([head])
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
			#p = PopUpDialog()
			#p.create_pop_up()
			#p = ThingWithAPopUp()
			#p.create_pop_up()
			#header[:] = [urwid.AttrMap(urwid.Text('asdfasdf'), 'buttn', 'buttnf')] 
		head.set_text("Key pressed: %s" % key)




	urwid.MainLoop(frame, palette, screen,
		unhandled_input=unhandled, pop_ups=True).run()


class PopUpDialog(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']
    def __init__(self):
        close_button = urwid.Button("that's pretty cool")
        urwid.connect_signal(close_button, 'click',
            lambda button:self._emit("close"))
        pile = urwid.Pile([urwid.Text(
            "^^  I'm attached to the widget that opened me. "
            "Try resizing the window!\n"), close_button])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))


class ThingWithAPopUp(urwid.PopUpLauncher):
    def __init__(self):
        self.__super.__init__(urwid.Button("click-me"))
        urwid.connect_signal(self.original_widget, 'click',
            lambda button: self.open_pop_up())

    def create_pop_up(self):
        pop_up = PopUpDialog()
        urwid.connect_signal(pop_up, 'close',
            lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':0, 'top':1, 'overlay_width':32, 'overlay_height':7}



def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
	print(choice)	
    #response = urwid.Text([u'You chose ', choice, u'\n'])
    #done = urwid.Button(u'Ok')
    #urwid.connect_signal(done, 'click', wtf)
    #main.original_widget = urwid.Filler(urwid.Pile([response,
     #   urwid.AttrMap(done, None, focus_map='reversed')]))


def wtf():
	print("wtf")


# NCurses compatible logger
class CursesHandler(logging.Handler):
	def emit(self, record):
		win.addstr(1,1,"CURSES HANDLER")
		pass

# Exit hook function. Clean up curses bindings here
def terminateCurses():
	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	curses.endwin()

atexit.register(terminateCurses)


ch = CursesHandler()
logging.getLogger('root').addHandler(ch)



# main() when invoked from the shell
if __name__ == '__main__':

	# Init curses
	stdscr = curses.initscr()
	curses.start_color()
	curses.use_default_colors()
	for i in range(0, curses.COLORS):
		curses.init_pair(i + 1, i, -1)

	curses.cbreak()
	curses.noecho()
	stdscr.keypad(1)

	# Main window
	win = curses.newwin(0,0)

	# Status window
	y, x = win.getmaxyx()

	# Resize the main window so we have room for status
	win.resize(y-3 ,x)
	win.box()
	win.refresh()

	winstat = curses.newwin(3,x,y-3,0)
	winstat.box()

	winstat.refresh()

	# Catch exceptions here and output them in curses
	try:
		main()
		time.sleep(5000)
	except Exception, err:
		terminateCurses()
 		traceback.print_exc()
 		 		
 		sys.exit(1)
 
	time.sleep(5000)
