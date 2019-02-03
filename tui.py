import npyscreen
import pprint
#from io import StringIO
import io
import sys
from ytalbum import YtAlbum
import md5
import logging
logging.basicConfig(filename="tuidebug.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

#logging.basicConfig(logging.WARNING)


class ArtistSearchList(npyscreen.MultiLineAction):
    pass

class ArtistTitleText(npyscreen.TitleText):
    def edit(self):
        super(ArtistTitleText, self).edit()


class YoutubeAlbumTui(npyscreen.NPSApp):
    selectedArtist=""
    selectedAlbum=""
    artistList={}
    albumList={}

    searchMode=''

    def __init__(self, *args, **keywords):
        super(YoutubeAlbumTui, self).__init__()
        self.yta = YtAlbum()
       # logging.getLogger().setLevel(logging.INFO);

    def msg(self, msg):
        npyscreen.notify_confirm(msg, wide=True);

    def ArtistSearch(self):

        if self.txtArtist.value == "":
            return;

        self.searchMode='artist'

        #Reset the search button so we can search again
        self.btnArtist.value=False
        self.btnArtist.update()

        artists = self.yta.listArtists(self.txtArtist.value)
        self.mainList.values = []
        self.artistList = {}


        for a in artists:
            self.mainList.values.append(a['name'].encode('ascii', 'ignore'))
            key = md5.new(a['name'].encode('ascii','ignore')).digest()
            #self.artistList[a['name']] = a;
            self.artistList[key] = a;

        self.mainList.update()



    def LoadArtist(self, act_on_this):
        self.txtArtist.value=act_on_this
        self.selectedAlbum=act_on_this
        #self.txtArtist.set_editable(False)
        self.txtArtist.update()
        key = md5.new(act_on_this).digest()
        artist = self.artistList[key]

        #albums = self.yta.search_releases("artistname:"+act_on_this, 100)
        albums = self.yta.search_releases("arid:"+artist['id'], 100)
        self.mainList.values = []
        for a in albums['release-list']:
            try:
                atype = a['release-group']['type']
            except:
                atype = ""

            try:
                country = a['country']
            except:
                country = ""

            title =  a['title'].encode('ascii', 'ignore') + ' (' + atype + ') [' + country + ']'
            self.mainList.values.append(title)
            key = md5.new(title).digest()
            self.albumList[key] = a;


#            self.mainList.values.append(a['title'].encode('ascii', 'ignore'))
 #           key = md5.new(a['title'].encode('ascii','ignore')).digest()
  #          self.albumList[key] = a;

            #self.albumList[a['title']] = a;

        self.mainList.update()
        self.searchMode='album'


    def LoadAlbum(self, act_on_this):
        self.txtAlbum.value=act_on_this
        self.selectedAlbum=act_on_this
        self.txtAlbum.update()
        key = md5.new(act_on_this).digest()
        album = self.albumList[key]

        rel = self.yta.get_release_by_id(album['id'])
        tracks=[]
        disc_count=rel['release']['medium-count']
        for d in rel['release']['medium-list']:
            for t in d['track-list']:
                title = str(t['position']) + ': ' + t['recording']['title'].encode('ascii', 'ignore') 
                #tracks.append( t['recording']['title'].encode('ascii', 'ignore') )
                tracks.append(title)

        self.mainListBox.set_values(tracks)
        #title = act_on_this + ' ' + rel['release']['country']
        self.mainListBox.name=act_on_this
        self.mainListBox.name=title
        self.mainListBox.footer="Discs: %s Tracks: %s" % (disc_count, len(tracks))
        self.mainListBox.update()


        #disc = mb.get_release_by_id(res['release-list'][0]['id'], ["media","recordings"])


    def main(self):
        F  = npyscreen.Form(name = "Youtube Album Downloader",)

        #self.txtArtist  = F.add(npyscreen.TitleText, name = "Artist:", max_width=40, rely=2)
        self.txtArtist  = F.add(ArtistTitleText, name = "Artist:", max_width=40, rely=2)
        

        self.btnArtist = F.add(npyscreen.MiniButton, name="Artist Search", rely = 2, relx = 50)
        self.btnArtist.whenToggled = self.ArtistSearch

        self.txtAlbum  = F.add(npyscreen.TitleText, name = "Album:", max_width=40, rely=3, editable = False)

        self.mainList = F.add(ArtistSearchList, max_width=45, max_height=12, rely=6, select_exit=True, exit_right=True)
        self.mainListBox = F.add(npyscreen.BoxTitle, name = "", max_width=40, max_height=13, rely=6, relx=50, exit_left=True)      


        def mainListSelect(act_on_this, keypress):
            if self.searchMode == 'artist':
                self.LoadArtist(act_on_this)
            elif self.searchMode == 'album':
                self.LoadAlbum(act_on_this)
            return

        self.mainList.actionHighlighted = mainListSelect


        def on_ok():
            npyscreen.notify_confirm("OK Button Pressed!")
        F.on_ok = on_ok
        F.edit()


class bcolors:
    '''Console color termcap codes'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def dump(arg, stdout=False):
    import subprocess
    columns = int(subprocess.check_output(['stty', 'size']).split()[1])

    old_stdout = sys.stdout
    result = io.BytesIO()
    sys.stdout = result
    '''Output a variable in a user friendly way'''
    #print "="*80, "\n", bcolors.BOLD, arg, bcolors.ENDC, "\n" + "="*80, bcolors.WARNING
    print arg
    col_width = max(len(row) for row in dir(arg)) + 3

    maxr = columns - col_width - 13; 
    for d in dir(arg):
        try:
            chop = str(getattr(arg,d))
            if len(chop) > maxr:
                chop = chop[0:maxr] + ' ...'

            print d.ljust(col_width) + " : " + chop
        except AttributeError:
            print "AttributeError: {} -- {}".format(d, d  )

    try:
        pprint.pprint(vars(arg))
        #print "FUCK"
    except TypeError:
        pass
    
    ret = result.getvalue()
    sys.stdout = old_stdout
    return ret

        
if __name__ == "__main__":
    tui = YoutubeAlbumTui()
    tui.run()       