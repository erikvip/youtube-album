#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "0.1.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"

import sys
import pprint
from PyQt4 import QtGui
from PyQt4 import QtCore

from PyQt4.QtCore import QUrl
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

import ytalbum

class YtAlbumGuiMain(QtGui.QMainWindow):

	#ytAlbum = {}

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

		# Data Table		
		self.table = QtGui.QTableWidget(0, 0, self)

		# Disable editing 
		self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)


		#self.table.setRowCount(1)
		self.table.setColumnCount(6)

		# Build the table headers
		self.table.setHorizontalHeaderLabels(['Artist', 'Album', 'Country', '#', 'Title', 'Source'])

#		self.table.setItem(0,0, QtGui.QTableWidgetItem('Aphex'))
#		self.table.setItem(0,1, QtGui.QTableWidgetItem('Alasdfasdf'))
#		widget = QtGui.QTableWidgetItem('Test')
		#widget.setBackgroundColor(QtCore.Qt.red)
#		widget.setIcon(QtGui.QIcon(QtCore.QString('https://google.com/favicon.ico')))
		#widget.setStyleSheet("""
		#	""")

#		self.table.setItem(0,2, widget)

		url = "http://www.google.com/favicon.ico"; 
		#Queue = QNetworkAccessManager()
#		def finishImageLoad(v):
#			print "asdfadsf"

		#Queue.finished.connect(finishImageLoad)
		#Queue.get(QNetworkRequest(QUrl(url)))
		#self.table.setItem(0,2, QtGui.QTableWidgetItem(QtGui.QIcon(url)) )



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

		#self.ytAlbum['artist'] = artist

#		self.table.setItem(0,0, QtGui.QTableWidgetItem('Aphex'))
#		self.table.setItem(0,1, QtGui.QTableWidgetItem('Alasdfasdf'))
#		self.table.setItem(0,1, QtGui.QTableWidgetItem('Two'))

		yta = ytalbum.YtAlbum()

		yta.query = artist
		res = yta.findRelease()

		for r in res:
			#print r.artist
			self.table.insertRow( self.table.rowCount() )
			self.table.setItem( self.table.rowCount()-1, 0, QtGui.QTableWidgetItem( r['artist'] ))
			self.table.setItem( self.table.rowCount()-1, 1, QtGui.QTableWidgetItem( r['title']  ))
			self.table.setItem( self.table.rowCount()-1, 2, QtGui.QTableWidgetItem( r['country'] ))

			for t in r['tracks']:
				self.table.insertRow( self.table.rowCount() )
				self.table.setItem( self.table.rowCount()-1, 0, QtGui.QTableWidgetItem( r['artist'] ))
				self.table.setItem( self.table.rowCount()-1, 1, QtGui.QTableWidgetItem( r['title']  ))
				self.table.setItem( self.table.rowCount()-1, 2, QtGui.QTableWidgetItem( r['country'] ))
				self.table.setItem( self.table.rowCount()-1, 3, QtGui.QTableWidgetItem( t['position'] ))
				self.table.setItem( self.table.rowCount()-1, 4, QtGui.QTableWidgetItem( t['title'] ))

				#pprint.pprint(t['sources'])

				source = "Not Found!"
				if t['sources'] != False:
					if len(t['sources']) > 0:
						src = QtGui.QTableWidgetItem( t['sources'][0]['url'] )
					else:
						src = QtGui.QTableWidgetItem( "Not Found!" )
						src.setBackgroundColor(QtCore.Qt.red)
				else:
					src = QtGui.QTableWidgetItem( "Not Found!" )
					src.setBackgroundColor(QtCore.Qt.red)

				self.table.setItem( self.table.rowCount()-1, 5, src )









if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	main_window = YtAlbumGuiMain()
	main_window.show()
	# Enter the main loop
	app.exec_()
