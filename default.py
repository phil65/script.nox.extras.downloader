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
    global INSTALL_PATH
    global download_mode
    modeselect= []
    if xbmc.getSkinDir() != "skin.aeon.nox" :
        xbmcgui.Dialog().ok( __addonid__, "Skin not supported")        
        return
    modeselect.append( __language__(32008) )
    modeselect.append( __language__(32009) )
    modeselect.append( __language__(32013) )
    modeselect.append( __language__(32015) )
    modeselect.append( __language__(32016) )
    modeselect.append( __language__(32019) )
    modeselect.append( __language__(32018) )
    modeselect.append( __language__(32024) )
    modeselect.append( __language__(32027) )
    dialogSelection = xbmcgui.Dialog()
    download_mode        = dialogSelection.select( __language__(32010), modeselect ) 
    if download_mode == -1 :
        return
    # Download more themes...
    elif download_mode == 0 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/backgrounds/"
        ZIP_PATH = os.path.join( SKIN_PATH, "backgroundpacks" )
        if not os.path.exists(ZIP_PATH):
            os.makedirs(ZIP_PATH)
        INSTALL_PATH  = os.path.join( SKIN_PATH, "backgrounds" )
        themes = get_local_backgroundpacks()
        themes.append( __language__(32001) )
        # Install local theme...
    elif download_mode == 1 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/themes/"
        INSTALL_PATH  = os.path.join( SKIN_PATH, "media" )
        ZIP_PATH = INSTALL_PATH
        themes = get_local_backgroundpacks()
        themes.append( __language__(32011) )
    elif download_mode == 2 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/genreart/icons/"
        INSTALL_PATH  = os.path.join( SKIN_PATH, "extras", "genre", "video", "icons" )
        ZIP_PATH = INSTALL_PATH
        if not os.path.exists(ZIP_PATH):
            os.makedirs(ZIP_PATH)
        themes = get_local_backgroundpacks()
        themes.append( __language__(32012) )
    elif download_mode == 3 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/genreart/fanart/"
        INSTALL_PATH  = os.path.join( SKIN_PATH, "extras", "genre", "video", "fanart" )
        ZIP_PATH = INSTALL_PATH
        if not os.path.exists(ZIP_PATH):
            os.makedirs(ZIP_PATH)
        themes = get_local_backgroundpacks()
        themes.append( __language__(32014) )
    elif download_mode == 4 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/weather-fanart/"
        INSTALL_PATH  = os.path.join( SKIN_PATH, "extras" )
        ZIP_PATH = os.path.join( SKIN_PATH, "extras", "Weatherpacks" )
        if not os.path.exists(ZIP_PATH):
            os.makedirs(ZIP_PATH)
        if not os.path.exists(os.path.join( SKIN_PATH, "extras", "Weather-Fanart" )):
            os.makedirs(os.path.join( SKIN_PATH, "extras", "Weather-Fanart" ))
        themes = get_local_backgroundpacks()
        themes.append( __language__(32017) )
    elif download_mode == 5 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/Music/icons/"
        INSTALL_PATH  = os.path.join( SKIN_PATH, "extras", "genre", "music", "icons" )
        ZIP_PATH = INSTALL_PATH
        if not os.path.exists(ZIP_PATH):
            os.makedirs(ZIP_PATH)
        themes = get_local_backgroundpacks()
        themes.append( __language__(32020) )
    elif download_mode == 6 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/Music/fanart/"
        INSTALL_PATH  = os.path.join( SKIN_PATH, "extras", "genre", "music", "fanart" )
        ZIP_PATH = INSTALL_PATH
        if not os.path.exists(ZIP_PATH):
            os.makedirs(ZIP_PATH)
        themes = get_local_backgroundpacks()
        themes.append( __language__(32021) )
    elif download_mode == 7 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/Mods/"
        INSTALL_PATH  = SKIN_PATH
        if not os.path.exists(os.path.join( SKIN_PATH, "Mods" )):
            os.makedirs(os.path.join( SKIN_PATH, "Mods" ))
        ZIP_PATH = os.path.join( SKIN_PATH, "Mods" )
        themes = get_local_backgroundpacks()
        themes.append( __language__(32025) )
    elif download_mode == 8 :
        BACKGROUNDPACKS_REPO = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/Scripts/"
        INSTALL_PATH  = xbmc.translatePath("special://home/addons")
        if not os.path.exists(os.path.join( SKIN_PATH, "Scripts" )):
            os.makedirs(os.path.join( SKIN_PATH, "Scripts" ))
        ZIP_PATH = os.path.join( SKIN_PATH, "Scripts" )
        themes = get_local_backgroundpacks()
        themes.append( __language__(32026) )
		
 #   if len(sys.argv) == 2 and sys.argv[ 1 ].startswith("http://") :
 #       BACKGROUNDPACKS_REPO = sys.argv[ 1 ]
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
        install_local_zip( theme )

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
        dp.create( __addonid__, __language__(32005), theme )
        # Download theme...
        remote_theme = os.path.join( BACKGROUNDPACKS_REPO, "%s.zip" % theme )
        local_theme  = os.path.join( ZIP_PATH, "%s.zip" % theme )
        urllib.urlretrieve( remote_theme, local_theme, lambda nb, bs, fs, url=remote_theme : download_progress_hook( nb, bs, fs, local_theme, dp ) )
        # Close progress dialog...
        dp.close()
        # Install local zip...
        install_local_zip( theme )

def download_progress_hook( numblocks, blocksize, filesize, url=None, dp=None, ratio=1.0 ):
    downloadedsize  = numblocks * blocksize
    percent         = int( downloadedsize * 100 / filesize )
    dp.update( percent )

def install_local_zip( theme ) :
    try :
        # Init
     #   shutil.rmtree(INSTALL_PATH)
        if download_mode == 0 :
            contents = [os.path.join(INSTALL_PATH, i) for i in os.listdir(INSTALL_PATH)]
            [shutil.rmtree(i) if os.path.isdir(i) else os.unlink(i) for i in contents]
        if download_mode == 4 :
            xbmc.executebuiltin( 'Skin.SetString(WeatherFanartDir,special://skin/extras/Weather-Fanart/)')
            contents = [os.path.join(INSTALL_PATH, "Weather-Fanart", i) for i in os.listdir(os.path.join(INSTALL_PATH, "Weather-Fanart"))]
            [shutil.rmtree(i) if os.path.isdir(i) else os.unlink(i) for i in contents]
        DownloadedZip = os.path.join( ZIP_PATH, "%s.zip" % theme )
        # Extract theme zip...
        zip = zipfile.ZipFile (DownloadedZip, "r")
        zip.extractall(INSTALL_PATH, filter(lambda f: not f.endswith('/'), zip.namelist()))
        zip.close()   
        if download_mode == 7 :
            xbmcgui.Dialog().ok( __addonid__, "Skin will reload now.")        
            xbmc.executebuiltin( 'XBMC.ReloadSkin()')
        xbmcgui.Dialog().ok( __addonid__, __language__(32003))        
    except :
        # Message...
        xbmcgui.Dialog().ok( __addonid__, __language__(32004))
                            
main()