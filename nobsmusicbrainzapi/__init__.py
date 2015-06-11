#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "0.2.1"
__author__ = "Erik Phillips <erikvip@gmail.com>"
__license__ = "GPLv3"


import pprint
import logging
import sys

from xml.etree import ElementTree as ET
import unicodedata
#from urllib.request import build_opener
#from urllib2 import * #build_opener, HTTPError, URLError
#import urllib2 as u
if sys.version_info[:2] >= (3, 0):
    # pylint: disable=E0611,F0401
    import pickle
    from urllib.request import build_opener
    from urllib.error import HTTPError, URLError
    from urllib.parse import urlencode
    uni, byt, xinput = str, bytes, input

else:
    from urllib2 import build_opener, HTTPError, URLError
    import cPickle as pickle
    from urllib import urlencode
    uni, byt, xinput = unicode, str, raw_input
    uni = unicode

#logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

def utf8_encode(x):
    """ Encode Unicode. """
    return x.encode("utf8") if type(x) == uni else x


def utf8_decode(x):
    """ Decode Unicode. """
    return x.decode("utf8") if type(x) == byt else x


class nobsmusicbrainzapi:

	def __init__(self):
		self._init_opener()

	def _init_opener(self):
	    """ Set up url opener. """
	    opener = build_opener()
	    ua = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; "
	    ua += "Trident/5.0)"
	    opener.addheaders = [("User-Agent", ua)]
	    self.urlopen = opener.open

	def search_artist(self, artistname, **kwa):
	    """ Return a list of artists / ids from MusicBrainz. 

	    """
	    url = "http://musicbrainz.org/ws/2/artist/"
	    qargs = dict(
	        query='"%s"' % artistname,
	    )
	    logging.info("Artist search for '%s'" % (artistname))
	    wdata = self._do_query(url, qargs)
	    
	    if not wdata:
	        return None

	    ns = {'mb': 'http://musicbrainz.org/ns/mmd-2.0#'}
	    root = ET.fromstring(utf8_encode(wdata))
	    alist = root.find("mb:artist-list", namespaces=ns)
	    artistcount = int(alist.get('count'))

	    if artistcount == 0:
	        return None

	    res = []
	    for a in alist:
	        arid = a.get("id")
	        aname =  a.find("mb:name", namespaces=ns).text
	        res.append({'arid': arid, 'name': aname})

	    return res

	def search_album(self, **kwa):
	    """ Return artist, album title and track count from MusicBrainz. """
	    url = "http://musicbrainz.org/ws/2/release/"
	    #	        release='"%s"' % albumname,
	    qargs = dict(
	        primarytype=kwa.get("primarytype", "album"),
	        status=kwa.get("status", "official"))

	    qargs.update({k: '"%s"' % v for k, v in kwa.items()})
	    qargs = ["%s:%s" % item for item in qargs.items()]
	    qargs = {"query": " AND ".join(qargs)}   
	    print qargs
	    wdata = self._do_query(url, qargs)

	    if not wdata:
	        return None

	    ns = {'mb': 'http://musicbrainz.org/ns/mmd-2.0#'}
	    root = ET.fromstring(utf8_encode(wdata))
	    rlist = root.find("mb:release-list", namespaces=ns)
	    albumcount = int(rlist.get('count'))

	    logging.info("Search album %i results for '%s'" % (albumcount, qargs))

	    if albumcount == 0:
	        return None

	    res = []
	    for a in rlist:
	        item = {'aid': a.get("id"), 'score': a.get("score")}
	        for v in a:
	        	tag = v.tag.split("}")[1]
	        	item[tag] = utf8_encode(v.text)
	        res.append(item)

	    return res

	def get_album(self, aid):
		url = "http://musicbrainz.org/ws/2/release/%s" % aid

		qargs = {"inc": "recordings"}
		wdata = self._do_query(url, qargs)

		if not wdata:
			return None

		ns = {'mb': 'http://musicbrainz.org/ns/mmd-2.0#'}
		root = ET.fromstring(utf8_encode(wdata))
		release = root.find("mb:release", namespaces=ns)
		medium = release.find("mb:medium-list", namespaces=ns)

		mcount = medium.get('count')

		res = []
		for m in medium:
			mpos = m.find("mb:position", namespaces=ns).text
			tracklist = m.find("mb:track-list", namespaces=ns)

			for t in tracklist:
				item = {'medium_position': mpos, 'medium_count': mcount}
				for v in t:
					tag = v.tag.split("}")[1]
					if tag != 'recording': 
						item[tag] = utf8_encode(v.text)
				recording = t.find("mb:recording", namespaces=ns)

				for r in recording:
					tag = r.tag.split("}")[1]
					item[tag] = utf8_encode(r.text)

				res.append(item)

		return res


	    
	    


	def _do_query(self, url, query, err='query failed', cache=True, report=False):

		query = [(k, query[k]) for k in sorted(query.keys())]
		url = "%s?%s" % (url, urlencode(query))

		logging.info("MB URL: %s" % url)

		wdata = utf8_decode(self.urlopen(url).read())

		return wdata if not report else (wdata, False)


if __name__ == '__main__':
	mb = nobsmusicbrainzapi()

	#a = mb.search_artist("orbit")
	#print a
	#albums = mb.search_album(arid="f22942a1-6f70-4f48-866e-238cb2308fbd")

	#album = mb.get_album("a91b9efb-efe5-4eb1-afaf-bca53de18967")
	album = mb.get_album("ead065b1-b582-4ac1-9041-f0c09b0ac67a")

	#print album


#	for a in albums:
		#print(a['title'])
		#pprint.pprint(a)
	
	
