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

		self.setGeometry(300,300,600,600)
		self.setWindowTitle('Youtube Album Downloader')

		self.create_widgets()

	def create_widgets(self):

		#Search Widgets
		self.artist_label = QtGui.QLabel("Artist / Album:")
		self.artist_edit = QtGui.QLineEdit()
		self.artist_button = QtGui.QPushButton("Find")


		
		self.table = QtGui.QTableWidget(3, 3, self)

		# Disable editing
		self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

		#self.table.setRowCount(1)
		#self.table.setColumnCount(1)

		# Build the table headers
		self.table.setHorizontalHeaderLabels(['Artist', 'Album', 'Country'])

		self.table.setItem(0,0, QtGui.QTableWidgetItem('Aphex'))
		self.table.setItem(0,1, QtGui.QTableWidgetItem('Alasdfasdf'))
		self.table.setItem(0,2, QtGui.QTableWidgetItem('US OF A'))
		#layout = QtGui.QGridLayout(self.table)

#		self.setLayout( layout )

#		self.gridWidget = QtGui.QWidget()
#		self.gridLayout = QtGui.QGridLayout(self.gridWidget)
#		self.gridLayout.addWidget( QtGui.QLabel('Album'), 0, 1 )
#		self.gridLayout.addWidget( QtGui.QLabel('Album ID'), 0, 2 )

		#Horizontal layout for Search Items
		h_box = QtGui.QHBoxLayout()
		h_box.addWidget(self.artist_label)
		h_box.addWidget(self.artist_edit)
		h_box.addWidget(self.artist_button)

		# Main window V_box layout
		v_box = QtGui.QVBoxLayout()
		v_box.addLayout(h_box)		
		v_box.addWidget(self.table)


		#Create central widget, add layout, and set
		central_widget = QtGui.QWidget()
		central_widget.setLayout(v_box)
		self.setCentralWidget(central_widget)
		self.table.show()

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
