#!/usr/bin/python
# KodiDisplayInfo v7.0
# Autor: Bjoern Reichert <opendisplaycase[at]gmx.net>
# License: GNU General Public License (GNU GPLv3)

import copy
import datetime
import json
import os
import sys
import pygame
from classes.DrawToDisplay.AudioThumbnail import DrawToDisplayAudioThumbnail
from classes.DrawToDisplay.Default import DrawToDisplayDefault
from classes.DrawToDisplay.VideoThumbnail import DrawToDisplayVideoThumbnail
from classes.DrawToDisplay.VideoTime import DrawToDisplayVideoTime
from classes.Helper import Helper
from classes.HelperConfig import HelperConfig
from classes.HelperImage import HelperImage
from classes.KodiWebserver import KodiWebserver

basedirpath = os.path.dirname(os.path.realpath(__file__)) + os.sep

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 114, 0)
GREEN = (0, 255, 0)
GREY = (153, 153, 153)

_config_default = {
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

helper = Helper(_config_default)

# init config && check config
helperconfig = HelperConfig(helper, _config_default, basedirpath)
_config_default = helperconfig.parse_config()

# Display FB for older
if _config_default['display.fbdev'] != "" and _config_default['display.writetodisplay'] == "SDL_FBDEV":
    os.environ["SDL_FBDEV"] = _config_default['display.fbdev']


def main_exit():
    pygame.quit()
    sys.exit()


def main():
    version = ".".join(map(str, sys.version_info[:3]))
    helper.printout("Python " + version)

    helper.printout("[info]    ", _config_default['mesg.cyan'])
    helper.printout("Start: KodiDisplayInfo")

    pygame.init()
    screen = pygame.display.set_mode(getattr(draw_default, 'screen' + _config_default['display.resolution'])(), 0, 32)
    pygame.display.set_caption('KodiDisplayInfo - Python ' + version)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # create a bunch of events
    reloaded_event = pygame.USEREVENT + 1
    
    # set timer for the event
    pygame.time.set_timer(reloaded_event, 750)
    
    image.set_pygamescreen(pygame, screen)
    draw_default.set_pygamescreen(pygame, screen)
    draw_videotime.set_pygamescreen(pygame, screen, draw_default)
    draw_videothumbnail.set_pygamescreen(pygame, screen, draw_default)
    draw_audiothumbnail.set_pygamescreen(pygame, screen, draw_default)

    running_libery_id = -1
    running = True
    # run the game loop
    try:
        while running:
            clock.tick(2)  # x times in one seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            time_now = datetime.datetime.now()

            screen.fill(_config_default['color.black'])  # start draw - reset
            
            playerid, playertype = KodiWebserver.kodi_getactiveplayers()
            if int(playerid) >= 0:
                if playertype == "video":
                    media_id, media_title, media_thumbnail, media_file = KodiWebserver.kodi_getitemvideo(playerid)
                    speed, media_time, media_totaltime = KodiWebserver.kodi_getproperties(playerid)
                    if _config_default['config.screenmodus_video'] == "time":
                        draw_videotime.drawproperties(media_title, time_now, speed, media_time, media_totaltime)
                    elif _config_default['config.screenmodus_video'] == "thumbnail":
                        if media_id != running_libery_id:
                            running_libery_id = media_id
                            draw_videothumbnail.setthumbnail(media_thumbnail, media_file)

                        draw_videothumbnail.drawproperties(time_now, speed, media_time, media_totaltime)
                elif playertype == "audio":
                    media_id, media_title, media_thumbnail, media_album, media_artist, media_file = KodiWebserver.kodi_getitemaudio(playerid)
                    speed, media_time, media_totaltime = KodiWebserver.kodi_getproperties(playerid)
                    if _config_default['config.screenmodus_audio'] == "thumbnail":
                        if media_id != running_libery_id:
                            running_libery_id = media_id
                            draw_audiothumbnail.setthumbnail(media_thumbnail, media_file)
                        
                        draw_audiothumbnail.drawproperties(media_title, speed, media_time, media_totaltime, media_album, media_artist)
            else:
                # API has nothing
                running_libery_id = -1

                media_total = {}
                jsonobject = _config_default['config.localmediatotal']
                for name in copy.copy(jsonobject):
                    media = jsonobject[name]
                    media_total.update({name:str(KodiWebserver.kodi_gettotalcount(media))})

                draw_default.drawlogostartscreen(time_now, json.loads(json.dumps(media_total)))
    
            pygame.display.flip()
            if _config_default['display.writetodisplay'] == "DIRECT":
                if _config_default['display.fbdev'] != "":
                    f = open(_config_default['display.fbdev'], "wb")
                    f.write(screen.convert(16, 0).get_buffer())
                    f.close()
        
        helper.printout("[end]     ", _config_default['mesg.magenta'])
        helper.printout("bye ...")
        main_exit()
    except SystemExit:
        main_exit()
    except KeyboardInterrupt:
        main_exit()


if __name__ == "__main__":
    image = HelperImage(_config_default)
    draw_default = DrawToDisplayDefault(helper, _config_default)
    draw_videotime = DrawToDisplayVideoTime(helper, _config_default)
    draw_videothumbnail = DrawToDisplayVideoThumbnail(helper, image, _config_default)
    draw_audiothumbnail = DrawToDisplayAudioThumbnail(helper, image, _config_default)
    
    KodiWebserver = KodiWebserver(helper, _config_default, draw_default)
    main()
