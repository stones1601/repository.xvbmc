# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Documentaries on YouTube by coldkeys
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: coldkeys
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.carpool-karaoke'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PLZ1f3amS4y1ffYEhGZDtawaEyRQQu69Bw"
YOUTUBE_CHANNEL_ID_2 = "UCJ0uqCI0Vqr2Rrt1HseGirg"





# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="Carpool Karaoke by James Corden and special guests",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="http://i4.mirror.co.uk/incoming/article4843959.ece/ALTERNATES/s615b/James-Corden.jpg",
        folder=True )
		
plugintools.add_item( 
        #action="", 
        title="James Corden Late Night Show",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="http://i4.mirror.co.uk/incoming/article4843959.ece/ALTERNATES/s615b/James-Corden.jpg",
        folder=True )

    
		
		

    
run()
