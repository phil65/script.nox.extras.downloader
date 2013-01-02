#
# BackgroundPackInstaller Script by Phil65  (inspired by ThemeInstaller script by Dan Dar3)
# Installs background packs from local or remote zip files

import os
import re
#import glob
import fnmatch
import zipfile
import urllib
import xbmc, xbmcgui, xbmcaddon
import shutil

__addon__        = xbmcaddon.Addon()
__addonid__      = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')
__cwd__          = __addon__.getAddonInfo('path').decode("utf-8")
__language__     = __addon__.getLocalizedString

SKIN_PATH = os.path.join( xbmc.translatePath("special://home/addons"), xbmc.getSkinDir() )

def main() :
  #  BACKGROUNDPACKS_REPO = None
    global ZIP_PATH
    global BACKGROUNDPACKS_REPO
    global SKIN_BG_PATH
    modeselect= []
    modeselect.append( __language__(32008) )
    modeselect.append( __language__(32009) )
    dialogSelection = xbmcgui.Dialog()
    index        = dialogSelection.select( __language__(32010), modeselect ) 
    if index == -1 :
        return
    # Download more themes...
    elif index == 0 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/"
        ZIP_PATH = SKIN_PATH
        SKIN_BG_PATH  = os.path.join( SKIN_PATH, "backgrounds" )
        themes = get_local_backgroundpacks()
        themes.append( __language__(32001) )
        # Install local theme...
    else :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/themes/"
        SKIN_BG_PATH  = os.path.join( SKIN_PATH, "media" )
        ZIP_PATH = os.path.join( SKIN_PATH, "media" )
        themes = get_local_backgroundpacks()
        themes.append( __language__(32011) )
 #   if len(sys.argv) == 2 and sys.argv[ 1 ].startswith("http://") :
 #       BACKGROUNDPACKS_REPO = sys.argv[ 1 ]
    # Get a list of local themes...
    # Add entry to download more themes...
    # Dialog to select local theme or download more...
    dialogThemes = xbmcgui.Dialog()
    index        = dialogThemes.select( __language__(32002), themes ) 
    # Cancel / Back...
    if index == -1 :
        return
    # Download more themes...
    elif index == len( themes ) - 1 :
        show_remote_themes( BACKGROUNDPACKS_REPO )
    # Install local theme...
    else :
        theme   = themes[ index ]
        install_local_backgroundpack( theme )

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)
    
def get_local_backgroundpacks( ) :
    # Get a list of extra themes (local)      
    themes = []
    if os.path.isdir( ZIP_PATH ) :
        for entry in os.listdir( ZIP_PATH ) :
            if fnmatch.fnmatch(entry, "*.zip") :
                ( name, ext ) = os.path.splitext( entry )
                themes.append( name )
    return themes

def show_remote_themes( BACKGROUNDPACKS_REPO ) :
    file = urllib.urlopen( BACKGROUNDPACKS_REPO )
    html = file.read()
    # Parse HTML...
    regexp = re.compile( "<li><a href=\"(.*?)\">(.*?)</a></li>", re.DOTALL )
    items  = regexp.findall( html )
    # Build a list of remote themes...
    themes = []
    for item in items :
       if item[1] != ".." :
           ( name, ext ) = os.path.splitext( item[1] )
           themes.append( name )
    # No remote themes found...
    if len( themes ) == 0 :
        xbmcgui.Dialog().ok( __addonid__, __language__(32007) )
    # User to choose a remote theme...
    else :
        dialogThemes = xbmcgui.Dialog()
        index = dialogThemes.select( __language__(32006), themes )
        # Cancel...
        if index == -1 :
            return
        #  User chose remote theme...
        theme = themes[ index ]
        # Show progress dialog...
        dp = xbmcgui.DialogProgress()
        # Download theme...
        remote_theme = os.path.join( BACKGROUNDPACKS_REPO, "%s.zip" % theme )
        local_theme  = os.path.join( ZIP_PATH, "%s.zip" % theme )
        urllib.urlretrieve( remote_theme, local_theme, lambda nb, bs, fs, url=remote_theme : download_progress_hook( nb, bs, fs, local_theme, dp ) )
        # Close progress dialog...
        dp.close()
        # Install local theme...
        install_local_backgroundpack( theme )

def download_progress_hook( numblocks, blocksize, filesize, url=None, dp=None, ratio=1.0 ):
    downloadedsize  = numblocks * blocksize
    percent         = int( downloadedsize * 100 / filesize )
    dp.update( percent )

def install_local_backgroundpack( theme ) :
    try :
        # Init
     #   shutil.rmtree(SKIN_BG_PATH)
        if SKIN_BG_PATH  != os.path.join( SKIN_PATH, "media" ) :
            contents = [os.path.join(SKIN_BG_PATH, i) for i in os.listdir(SKIN_BG_PATH)]
            [shutil.rmtree(i) if os.path.isdir(i) else os.unlink(i) for i in contents]
        backgroundpackZip = os.path.join( ZIP_PATH, "%s.zip" % theme )
        # Extract theme zip...
        zip = zipfile.ZipFile (backgroundpackZip, "r")
        zip.extractall(SKIN_BG_PATH, filter(lambda f: not f.endswith('/'), zip.namelist()))
        zip.close()   
        xbmcgui.Dialog().ok( __addonid__, __language__(32003))        
    except :
        # Message...
        xbmcgui.Dialog().ok( __addonid__, __language__(32004))
                            
main()