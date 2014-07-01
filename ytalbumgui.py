#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "0.1.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"

import sys
import pprint
from PyQt4 import QtGui
from PyQt4 import QtCore

import ytalbum

class YtAlbumGuiMain(QtGui.QMainWindow):

	ytAlbum = {}

	def __init__(self, win_parent = None):
		#Init the base class
		QtGui.QMainWindow.__init__(self, win_parent)

		self.create_widgets()

	def create_widgets(self):

		#Widgets
		self.artist_label = QtGui.QLabel("Artist:")
		self.artist_edit = QtGui.QLineEdit()
		self.artist_button = QtGui.QPushButton("Find")

		#Horizontal layout
		h_box = QtGui.QHBoxLayout()
		h_box.addWidget(self.artist_label)
		h_box.addWidget(self.artist_edit)
		h_box.addWidget(self.artist_button)

		#Create central widget, add layout, and set
		central_widget = QtGui.QWidget()
		central_widget.setLayout(h_box)
		self.setCentralWidget(central_widget)

		# Click handlers
		QtCore.QObject.connect(self.artist_button, 
			QtCore.SIGNAL('clicked()'), 
			self.findArtistHandler)

# Search for artist and display albums
	def findArtistHandler(self):
		artist = self.artist_edit.displayText()

		self.ytAlbum['artist'] = artist






if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	main_window = YtAlbumGuiMain()
	main_window.show()
	# Enter the main loop
	app.exec_()
