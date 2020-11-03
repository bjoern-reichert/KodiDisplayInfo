#!/usr/bin/python
# KodiDisplayInfo v6.2
# Autor: Bjoern Reichert <opendisplaycase[at]gmx.net>
# License: GNU General Public License (GNU GPLv3)
#
# v1.0    XBMC 12 Frodo Release [April 2014]
# v1.1    ADD config.txt for Webserver
# v2.0    XBMC 13 Gotham
# v2.1    Bugfix: jsonrpc API - KeyError, IndexError
# v2.2    IF Player.GetItem title is empty check if label is set
# v3.0    Kodi 14 Release - Refactor Version
#         Published GitHub 03.10.2015
# v3.2    Optimization movie title -> TITLEFORMAT -> oneline (default), twoline [smaller font size and optimized for two lines]
#
# v3.3    Change the "time" and "totaltime" structure, screen draw optimization, new option -> TIMEFORMAT -> shows 6 minutes or 00:06:21 long
#         -> ideas from Andrea Prunic <aprunic[at]gmail.com>
# v3.4    Use the video structure for audio, update class KODI_WEBSERVER
# v3.5    Delete v3.1
# v4.0    Add VideoThumbnail intergration -> SCREENMODUS = thumbnail
# v4.1    Add AudioThumbnail and HelperImage
# v4.2    Add TIMEFORMAT 06:21 short
# v4.3    Config optimization, UnicodeEncodeError Fix
# v5.0    Python 2 and Python 3 compatible
# v6.0    Startscreen HDD und KODI total infos
# v6.1    Fix: Kodi server change user and password structure
# v6.2    Fix: Fix HelperImage URL from Kodi-API if thumbnail is from image.tmdb.org
#         Published GitHub 03.11.2020

import os
import json
import sys
import datetime
import pygame
from pygame.locals import *
from classes.HelperConfig import HelperConfig
from classes.Helper import Helper
from classes.HelperImage import HelperImage
from classes.DrawToDisplay_Default import DrawToDisplay_Default
from classes.DrawToDisplay_VideoTime import DrawToDisplay_VideoTime
from classes.DrawToDisplay_VideoThumbnail import DrawToDisplay_VideoThumbnail
from classes.DrawToDisplay_AudioThumbnail import DrawToDisplay_AudioThumbnail
from classes.KODI_WEBSERVER import KODI_WEBSERVER

basedirpath = os.path.dirname(os.path.realpath(__file__)) + os.sep

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,114,0)
GREEN = (0,255,0)
GREY = (153,153,153)

_ConfigDefault = {
    "basedirpath":                  basedirpath,

    "mesg.grey":                    30,
    "mesg.red":                     31,
    "mesg.green":                   32,
    "mesg.yellow":                  33,
    "mesg.blue":                    34,
    "mesg.magenta":                 35,
    "mesg.cyan":                    36,
    "mesg.white":                   37,

    "KODI.webserver.host":          "localhost",
    "KODI.webserver.port":          "8080",
    "KODI.webserver.user":          "",
    "KODI.webserver.pass":          "",

    "display.resolution":           "320x240",

    "config.screenmodus_video":     "time",
    "config.formattime_video":      "minutes",
    "config.screenmodus_audio":     "thumbnail",
    "config.formattime_audio":      "short",

    "config.localmountpath":        [],
    "config.localmediatotal":       [],

    "color.black":                  BLACK,
    "color.white":                  WHITE,
    "color.red":                    RED,
    "color.orange":                 ORANGE,
    "color.green":                  GREEN,
    "color.grey":                   GREY
}

helper = Helper(_ConfigDefault)

# init config && check config
helperconfig = HelperConfig(helper, _ConfigDefault, basedirpath)
_ConfigDefault = helperconfig.parseConfig()

def main_exit():
    pygame.quit()
    sys.exit()

def main():
    time_now = 0
    media_title = ""
    version = ".".join(map(str, sys.version_info[:3]))
    helper.printout("Python "+ version)

    helper.printout("[info]    ", _ConfigDefault['mesg.cyan'])
    helper.printout("Start: KodiDisplayInfo")
    
    pygame.init()
    screen = pygame.display.set_mode(getattr(draw_default, 'Screen'+_ConfigDefault['display.resolution'])(), 0, 32)
    pygame.display.set_caption('KodiDisplayInfo - Python '+ version)
    pygame.mouse.set_visible(0)
    clock = pygame.time.Clock()
    
    RELOAD_SPEED = 750
    
    # create a bunch of events
    reloaded_event = pygame.USEREVENT + 1
    
    # set timer for the event
    pygame.time.set_timer(reloaded_event, RELOAD_SPEED)
    
    image.setPygameScreen(pygame, screen)
    draw_default.setPygameScreen(pygame, screen)
    draw_videotime.setPygameScreen(pygame, screen, draw_default)
    draw_videothumbnail.setPygameScreen(pygame, screen, draw_default)
    draw_audiothumbnail.setPygameScreen(pygame, screen, draw_default)
    
    running_libery_id = -1
    running = True
    # run the game loop
    try:
        while running:
            clock.tick(4) # 4 x in one seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            time_now = datetime.datetime.now()
            #start draw
            screen.fill(_ConfigDefault['color.black']) #reset
            
            playerid, playertype = KODI_WEBSERVER.KODI_GetActivePlayers()
            if int(playerid) >= 0:
                if playertype=="video":
                    media_id, media_title, media_thumbnail = KODI_WEBSERVER.KODI_GetItemVideo(playerid)
                    speed, media_time, media_totaltime = KODI_WEBSERVER.KODI_GetProperties(playerid)
                    if _ConfigDefault['config.screenmodus_video']=="time":
                        draw_videotime.drawProperties(media_title, time_now, speed, media_time, media_totaltime)
                    elif _ConfigDefault['config.screenmodus_video']=="thumbnail":
                        if media_id!=running_libery_id:
                            running_libery_id=media_id
                            draw_videothumbnail.setThumbnail(media_thumbnail)
                        
                        draw_videothumbnail.drawProperties(media_title, time_now, speed, media_time, media_totaltime)
                elif playertype == "audio":
                    media_id, media_title, media_thumbnail, media_album, media_artist = KODI_WEBSERVER.KODI_GetItemAudio(playerid)
                    speed, media_time, media_totaltime = KODI_WEBSERVER.KODI_GetProperties(playerid)
                    if _ConfigDefault['config.screenmodus_audio']=="thumbnail":
                        if media_id!=running_libery_id:
                            running_libery_id=media_id
                            draw_audiothumbnail.setThumbnail(media_thumbnail)
                        
                        draw_audiothumbnail.drawProperties(media_title, time_now, speed, media_time, media_totaltime, media_album, media_artist)
            else:
                # API has nothing
                running_libery_id = -1
                media_title = ""

                media_total = {}
                jsonObject = _ConfigDefault['config.localmediatotal']
                for name in jsonObject.copy():
                    media = jsonObject[name]
                    media_total.update({name:str(KODI_WEBSERVER.KODI_GetTotalCount(media))})

                draw_default.drawLogoStartScreen(time_now, json.loads(json.dumps(media_total)))
    
            pygame.display.flip()
        
        helper.printout("[end]     ", _ConfigDefault['mesg.magenta'])
        helper.printout("bye ...")
        main_exit()
    except SystemExit:
        main_exit()
    except KeyboardInterrupt:
        main_exit()

if __name__ == "__main__":
    image = HelperImage()
    draw_default = DrawToDisplay_Default(helper, _ConfigDefault)
    draw_videotime = DrawToDisplay_VideoTime(helper, _ConfigDefault)
    draw_videothumbnail = DrawToDisplay_VideoThumbnail(helper, image, _ConfigDefault)      
    draw_audiothumbnail = DrawToDisplay_AudioThumbnail(helper, image, _ConfigDefault)  
    
    KODI_WEBSERVER = KODI_WEBSERVER(helper, _ConfigDefault, draw_default)
    main()