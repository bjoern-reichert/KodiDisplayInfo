import os
import json
import copy
try:
    import ConfigParser as configparser # Python2
except ImportError:
    import configparser # Python3


class HelperConfig:
    
    def __init__(self, helper, _config_default, basedirpath):
        self.__helper = helper
        self.__config_default = _config_default
        
        self.__helper.printout("[info]    ", _config_default['mesg.green'])
        self.__helper.printout("Parse Config")
        self.__configParser = configparser.RawConfigParser()
        self.__configParser.read(r'' + basedirpath + 'config.txt')
    
    def parse_config(self):
        if self.__configParser.has_option('CONFIG', 'SCREENMODUS_VIDEO'):
            temp = self.__configParser.get('CONFIG', 'SCREENMODUS_VIDEO')
            if temp == "time" or temp == "thumbnail":
                self.__config_default['config.screenmodus_video'] = temp
            else:
                self.__helper.printout("[warning]    ", self.__config_default['mesg.yellow'])
                self.__helper.printout("Config [CONFIG] SCREENMODUS_VIDEO not set correctly - default is activ!")
                
        if self.__configParser.has_option('CONFIG', 'FORMATTIME_VIDEO'):
            temp = self.__configParser.get('CONFIG', 'FORMATTIME_VIDEO')
            if temp == "minutes" or temp == "short" or temp == "long":
                self.__config_default['config.formattime_video'] = temp
            else:
                self.__helper.printout("[warning]    ", self.__config_default['mesg.yellow'])
                self.__helper.printout("Config [CONFIG] FORMATTIME_VIDEO not set correctly - default is activ!")
                
        if self.__configParser.has_option('CONFIG', 'SCREENMODUS_AUDIO'):
            temp = self.__configParser.get('CONFIG', 'SCREENMODUS_AUDIO')
            if temp == "thumbnail":
                self.__config_default['config.screenmodus_audio'] = temp
            else:
                self.__helper.printout("[warning]    ", self.__config_default['mesg.yellow'])
                self.__helper.printout("Config [CONFIG] SCREENMODUS_VIDEO not set correctly - default is activ!")
                
        if self.__configParser.has_option('CONFIG', 'FORMATTIME_AUDIO'):
            temp = self.__configParser.get('CONFIG', 'FORMATTIME_AUDIO')
            if temp == "short" or temp == "long":
                self.__config_default['config.formattime_audio'] = temp
            else:
                self.__helper.printout("[warning]    ", self.__config_default['mesg.yellow'])
                self.__helper.printout("Config [CONFIG] FORMATTIME_AUDIO not set correctly - default is activ!")
                
        if self.__configParser.has_option('CONFIG', 'LOCALMOUNTPATHS'):
            jsonobject = json.loads(self.__configParser.get('CONFIG', 'LOCALMOUNTPATHS'))
            for name in copy.copy(jsonobject):
                path = jsonobject[name]
                if not os.path.isdir(path):
                    del jsonobject[name]
                    self.__helper.printout("[error]    ", self.__config_default['mesg.red'])
                    self.__helper.printout("Path: " + path)

            if len(jsonobject) > 0:
                self.__config_default['config.localmountpath'] = jsonobject
            else:
                self.__helper.printout("[warning]    ", self.__config_default['mesg.red'])
                self.__helper.printout("Config [CONFIG] LOCALMOUNTPATHS empty!")
                
        if self.__configParser.has_option('CONFIG', 'LOCALMEDIATOTAL'):
            jsonobject = json.loads(self.__configParser.get('CONFIG', 'LOCALMEDIATOTAL'))
            for name in copy.copy(jsonobject):
                media = jsonobject[name]
                if media not in ["video", "songs", "album"]:
                    del jsonobject[name]
                    self.__helper.printout("[error]    ", self.__config_default['mesg.red'])
                    self.__helper.printout("Media: " + media)

            if len(jsonobject) > 0:
                self.__config_default['config.localmediatotal'] = jsonobject
            else:
                self.__helper.printout("[warning]    ", self.__config_default['mesg.red'])
                self.__helper.printout("Config [CONFIG] LOCALMEDIATOTAL empty!")

        if self.__configParser.has_option('DISPLAY', 'RESOLUTION'):
            temp = self.__configParser.get('DISPLAY', 'RESOLUTION')
            if temp == "320x240" or temp == "480x272" or temp == "480x320":
                self.__config_default['display.resolution'] = temp
            else:
                self.__helper.printout("[warning]    ", self.__config_default['mesg.yellow'])
                self.__helper.printout("Config [DISPLAY] RESOLUTION not set correctly - default is activ!")

        if self.__configParser.has_option('DISPLAY', 'FBDEV'):
            temp = self.__configParser.get('DISPLAY', 'FBDEV')
            if temp != "":
                self.__config_default['display.fbdev'] = temp
            else:
                self.__config_default['display.fbdev'] = ''

        if self.__configParser.has_option('DISPLAY', 'WRITETODISPLAY'):
            temp = self.__configParser.get('DISPLAY', 'WRITETODISPLAY')
            if temp == "SDL_FBDEV" or temp == "DIRECT":
                self.__config_default['display.writetodisplay'] = temp
            else:
                self.__config_default['display.writetodisplay'] = 'SDL_FBDEV'
        
        if self.__configParser.has_option('KODI_WEBSERVER', 'HOST'):
            self.__config_default['KODI.webserver.host'] = self.__configParser.get('KODI_WEBSERVER', 'HOST')
        if self.__configParser.has_option('KODI_WEBSERVER', 'PORT'):
            self.__config_default['KODI.webserver.port'] = self.__configParser.get('KODI_WEBSERVER', 'PORT')
        if self.__configParser.has_option('KODI_WEBSERVER', 'USER'):
            self.__config_default['KODI.webserver.user'] = self.__configParser.get('KODI_WEBSERVER', 'USER')
        if self.__configParser.has_option('KODI_WEBSERVER', 'PASS'):
            self.__config_default['KODI.webserver.pass'] = self.__configParser.get('KODI_WEBSERVER', 'PASS')        
                
        if self.__configParser.has_option('COLOR', 'BLACK'):
            self.__config_default['color.black'] = self.__helper.html_color_to_rgb(self.__configParser.get('COLOR', 'BLACK'))
        if self.__configParser.has_option('COLOR', 'WHITE'):
            self.__config_default['color.white'] = self.__helper.html_color_to_rgb(self.__configParser.get('COLOR', 'WHITE'))
        if self.__configParser.has_option('COLOR', 'RED'):
            self.__config_default['color.red'] = self.__helper.html_color_to_rgb(self.__configParser.get('COLOR', 'RED'))
        if self.__configParser.has_option('COLOR', 'GREEN'):
            self.__config_default['color.green'] = self.__helper.html_color_to_rgb(self.__configParser.get('COLOR', 'GREEN'))
        if self.__configParser.has_option('COLOR', 'ORANGE'):
            self.__config_default['color.orange'] = self.__helper.html_color_to_rgb(self.__configParser.get('COLOR', 'ORANGE'))
            
        return self.__config_default
            