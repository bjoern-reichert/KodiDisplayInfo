#!/usr/bin/python
# KodiDisplayInfo v3.0
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
# v3.3    Change the "time" and "totaltime" structure, screen draw optimization, new option -> TIMEFORMAT -> shows 6 minutes or 00:06:21 kodi
#         -> ideas from Andrea Prunic <aprunic[at]gmail.com>
# v3.4    Use the video structure for audio, update class KODI_WEBSERVER
# v3.5    Delete v3.1

import os
import sys
import datetime
import pygame
import ConfigParser
from pygame.locals import *
from classes.Helper import Helper
from classes.DrawToDisplay_Default import DrawToDisplay_Default
from classes.DrawToDisplay_VideoTime import DrawToDisplay_VideoTime
from classes.KODI_WEBSERVER import KODI_WEBSERVER

basedirpath = os.path.dirname(os.path.realpath(__file__)) + os.sep

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,114,0)
GREEN = (0,255,0)

_ConfigDefault = {
    "basedirpath":              basedirpath,
    
    "mesg.grey":                30,
    "mesg.red":                 31,
    "mesg.green":               32,    
    "mesg.yellow":              33,
    "mesg.blue":                34,
    "mesg.magenta":             35,
    "mesg.cyan":                36,   
    "mesg.white":               37,

    "KODI.webserver.host":            "localhost",
    "KODI.webserver.port":            "8080",
    "KODI.webserver.user":            "",
    "KODI.webserver.pass":            "",
    
    "display.resolution":       "320x240",   
    
    "config.screenmodus":       "time",
    "config.titleformat":       "oneline",
    "config.timeformat":        "minutes", 
                  
    "color.black":              BLACK,
    "color.white":              WHITE,
    "color.red":                RED,
    "color.orange":             ORANGE,
    "color.green":              GREEN
    }

helper = Helper(_ConfigDefault)

# init config
helper.printout("[info]    ", _ConfigDefault['mesg.green'])
print "Parse Config"
configParser = ConfigParser.RawConfigParser()   
configFilePath = r''+basedirpath+'config.txt'
configParser.read(configFilePath)

# check config
if configParser.has_option('CONFIG', 'SCREENMODUS'):
    temp = configParser.get('CONFIG', 'SCREENMODUS')
    if temp=="time" or temp=="thumbnail":
        _ConfigDefault['config.screenmodus'] = temp
    else:
        helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
        print "Config [CONFIG] SCREENMODUS not set correctly - default is activ!"
        
if configParser.has_option('CONFIG', 'TITLEFORMAT'):
    temp = configParser.get('CONFIG', 'TITLEFORMAT')
    if temp=="oneline" or temp=="twoline":
        _ConfigDefault['config.titleformat'] = temp
    else:
        helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
        print "Config [CONFIG] TITLEFORMAT not set correctly - default is activ!"
        
if configParser.has_option('CONFIG', 'TIMEFORMAT'):
    temp = configParser.get('CONFIG', 'TIMEFORMAT')
    if temp=="minutes" or temp=="kodi":
        _ConfigDefault['config.timeformat'] = temp
    else:
        helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
        print "Config [CONFIG] TIMEFORMAT not set correctly - default is activ!" 
        
if configParser.has_option('DISPLAY', 'RESOLUTION'):
    temp = configParser.get('DISPLAY', 'RESOLUTION')
    if temp=="320x240" or temp=="480x272" or temp=="480x320":
        _ConfigDefault['display.resolution'] = temp
    else:
        helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
        print "Config [DISPLAY] RESOLUTION not set correctly - default is activ!"

if configParser.has_option('KODI_WEBSERVER', 'HOST'):
    _ConfigDefault['KODI.webserver.host'] = configParser.get('KODI_WEBSERVER', 'HOST')
if configParser.has_option('KODI_WEBSERVER', 'PORT'):
    _ConfigDefault['KODI.webserver.port'] = configParser.get('KODI_WEBSERVER', 'PORT')
if configParser.has_option('KODI_WEBSERVER', 'USER'):
    _ConfigDefault['KODI.webserver.user'] = configParser.get('KODI_WEBSERVER', 'USER')
if configParser.has_option('KODI_WEBSERVER', 'PASS'):
    _ConfigDefault['KODI.webserver.pass'] = configParser.get('KODI_WEBSERVER', 'PASS')        
        
if configParser.has_option('COLOR', 'BLACK'):
    _ConfigDefault['color.black'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'BLACK'))
if configParser.has_option('COLOR', 'WHITE'):
    _ConfigDefault['color.white'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'WHITE'))
if configParser.has_option('COLOR', 'RED'):
    _ConfigDefault['color.red'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'RED'))
if configParser.has_option('COLOR', 'GREEN'):
    _ConfigDefault['color.green'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'GREEN'))
if configParser.has_option('COLOR', 'ORANGE'):
    _ConfigDefault['color.orange'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'ORANGE'))

#Display FB
if configParser.has_option('DISPLAY', 'FBDEV'):
    if configParser.get('DISPLAY', 'FBDEV')!="":
        os.environ["SDL_FBDEV"] = configParser.get('DISPLAY', 'FBDEV')

def main_exit():
    pygame.quit()
    sys.exit()

def main():
    time_now = 0
    media_title = ""

    helper.printout("[info]    ", _ConfigDefault['mesg.cyan'])
    print "Start: KodiDisplayInfo"
    
    pygame.init()
    screen = pygame.display.set_mode(getattr(draw_default, 'Screen'+_ConfigDefault['display.resolution'])(), 0, 32)
    pygame.display.set_caption('KodiDisplayInfo')
    pygame.mouse.set_visible(0)
    clock = pygame.time.Clock()
    
    RELOAD_SPEED = 750
    
    # create a bunch of events
    reloaded_event = pygame.USEREVENT + 1
    
    # set timer for the event
    pygame.time.set_timer(reloaded_event, RELOAD_SPEED)
    
    draw_default.setPygameScreen(pygame, screen)
    draw_videotime.setPygameScreen(pygame, screen, draw_default)
    
    running = True
    # run the game loop
    try:        
        while running:
            clock.tick(4) # 4 x in one seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                #elif event.type == pygame.MOUSEBUTTONDOWN:
                #    print "mouse at (%d, %d)" % event.pos
                #elif event.type == KEYDOWN and event.key == K_ESCAPE:
                #    running = False
                
            time_now = datetime.datetime.now()
            #start draw
            screen.fill(_ConfigDefault['color.black']) #reset
            
            playerid, playertype = KODI_WEBSERVER.KODI_GetActivePlayers()
            if playertype=="video" and int(playerid) >= 0:    
                media_title = KODI_WEBSERVER.KODI_GetItem(playerid, playertype)
                speed, media_time, media_totaltime = KODI_WEBSERVER.KODI_GetProperties(playerid)
                if _ConfigDefault['config.screenmodus']=="time":
                    draw_videotime.drawProperties(media_title, time_now, speed, media_time, media_totaltime)
            elif playertype == "audio" and int(playerid) >= 0:
                # Clone from Video
                media_title = KODI_WEBSERVER.KODI_GetItem(playerid, playertype)
                speed, media_time, media_totaltime = KODI_WEBSERVER.KODI_GetProperties(playerid)
                if _ConfigDefault['config.screenmodus']=="time":
                    draw_videotime.drawProperties(media_title, time_now, speed, media_time, media_totaltime)
            else:
                # API has nothing
                media_title = ""
                draw_default.drawLogoStartScreen(time_now)
    
            pygame.display.flip()
        
        helper.printout("[end]     ", _ConfigDefault['mesg.magenta'])
        print "bye ..."
        main_exit()
    except SystemExit:
        main_exit()
    except KeyboardInterrupt:
        main_exit()

if __name__ == "__main__":
    draw_default = DrawToDisplay_Default(helper, _ConfigDefault)
    
    if _ConfigDefault['config.screenmodus']=="time":
        draw_videotime = DrawToDisplay_VideoTime(helper, _ConfigDefault)
    
    KODI_WEBSERVER = KODI_WEBSERVER(helper, _ConfigDefault, draw_default)
    main()