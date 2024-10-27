import os
import json
import copy
try:
    import ConfigParser as configparser # Python2
except ImportError:
    import configparser # Python3


class HelperConfig:
    
    def __init__(self, helper, _config_default, basedirpath):
        self.helper = helper
        self._config_default = _config_default
        
        self.helper.printout("[info]    ", _config_default['mesg.green'])
        self.helper.printout("Parse Config")
        self.configParser = configparser.RawConfigParser()
        self.configParser.read(r'' + basedirpath + 'config.txt')
    
    def parse_config(self):
        if self.configParser.has_option('CONFIG', 'SCREENMODUS_VIDEO'):
            temp = self.configParser.get('CONFIG', 'SCREENMODUS_VIDEO')
            if temp == "time" or temp == "thumbnail":
                self._config_default['config.screenmodus_video'] = temp
            else:
                self.helper.printout("[warning]    ", self._config_default['mesg.yellow'])
                self.helper.printout("Config [CONFIG] SCREENMODUS_VIDEO not set correctly - default is activ!")
                
        if self.configParser.has_option('CONFIG', 'FORMATTIME_VIDEO'):
            temp = self.configParser.get('CONFIG', 'FORMATTIME_VIDEO')
            if temp == "minutes" or temp == "short" or temp == "long":
                self._config_default['config.formattime_video'] = temp
            else:
                self.helper.printout("[warning]    ", self._config_default['mesg.yellow'])
                self.helper.printout("Config [CONFIG] FORMATTIME_VIDEO not set correctly - default is activ!")
                
        if self.configParser.has_option('CONFIG', 'SCREENMODUS_AUDIO'):
            temp = self.configParser.get('CONFIG', 'SCREENMODUS_AUDIO')
            if temp == "thumbnail":
                self._config_default['config.screenmodus_audio'] = temp
            else:
                self.helper.printout("[warning]    ", self._config_default['mesg.yellow'])
                self.helper.printout("Config [CONFIG] SCREENMODUS_VIDEO not set correctly - default is activ!")
                
        if self.configParser.has_option('CONFIG', 'FORMATTIME_AUDIO'):
            temp = self.configParser.get('CONFIG', 'FORMATTIME_AUDIO')
            if temp == "short" or temp == "long":
                self._config_default['config.formattime_audio'] = temp
            else:
                self.helper.printout("[warning]    ", self._config_default['mesg.yellow'])
                self.helper.printout("Config [CONFIG] FORMATTIME_AUDIO not set correctly - default is activ!")
                
        if self.configParser.has_option('CONFIG', 'LOCALMOUNTPATHS'):
            jsonobject = json.loads(self.configParser.get('CONFIG', 'LOCALMOUNTPATHS'))
            for name in copy.copy(jsonobject):
                path = jsonobject[name]
                if not os.path.isdir(path):
                    del jsonobject[name]
                    self.helper.printout("[error]    ", self._config_default['mesg.red'])
                    self.helper.printout("Path: " + path)

            if len(jsonobject) > 0:
                self._config_default['config.localmountpath'] = jsonobject
            else:
                self.helper.printout("[warning]    ", self._config_default['mesg.red'])
                self.helper.printout("Config [CONFIG] LOCALMOUNTPATHS empty!")
                
        if self.configParser.has_option('CONFIG', 'LOCALMEDIATOTAL'):
            jsonobject = json.loads(self.configParser.get('CONFIG', 'LOCALMEDIATOTAL'))
            for name in copy.copy(jsonobject):
                media = jsonobject[name]
                if media not in ["video", "songs", "album"]:
                    del jsonobject[name]
                    self.helper.printout("[error]    ", self._config_default['mesg.red'])
                    self.helper.printout("Media: " + media)

            if len(jsonobject) > 0:
                self._config_default['config.localmediatotal'] = jsonobject
            else:
                self.helper.printout("[warning]    ", self._config_default['mesg.red'])
                self.helper.printout("Config [CONFIG] LOCALMEDIATOTAL empty!")

        if self.configParser.has_option('DISPLAY', 'RESOLUTION'):
            temp = self.configParser.get('DISPLAY', 'RESOLUTION')
            if temp == "320x240" or temp == "480x272" or temp == "480x320":
                self._config_default['display.resolution'] = temp
            else:
                self.helper.printout("[warning]    ", self._config_default['mesg.yellow'])
                self.helper.printout("Config [DISPLAY] RESOLUTION not set correctly - default is activ!")

        if self.configParser.has_option('DISPLAY', 'FBDEV'):
            temp = self.configParser.get('DISPLAY', 'FBDEV')
            if temp != "":
                self._config_default['display.fbdev'] = temp
            else:
                self._config_default['display.fbdev'] = ''

        if self.configParser.has_option('DISPLAY', 'WRITETODISPLAY'):
            temp = self.configParser.get('DISPLAY', 'WRITETODISPLAY')
            if temp == "SDL_FBDEV" or temp == "DIRECT":
                self._config_default['display.writetodisplay'] = temp
            else:
                self._config_default['display.writetodisplay'] = 'SDL_FBDEV'
        
        if self.configParser.has_option('KODI_WEBSERVER', 'HOST'):
            self._config_default['KODI.webserver.host'] = self.configParser.get('KODI_WEBSERVER', 'HOST')
        if self.configParser.has_option('KODI_WEBSERVER', 'PORT'):
            self._config_default['KODI.webserver.port'] = self.configParser.get('KODI_WEBSERVER', 'PORT')
        if self.configParser.has_option('KODI_WEBSERVER', 'USER'):
            self._config_default['KODI.webserver.user'] = self.configParser.get('KODI_WEBSERVER', 'USER')
        if self.configParser.has_option('KODI_WEBSERVER', 'PASS'):
            self._config_default['KODI.webserver.pass'] = self.configParser.get('KODI_WEBSERVER', 'PASS')        
                
        if self.configParser.has_option('COLOR', 'BLACK'):
            self._config_default['color.black'] = self.helper.html_color_to_rgb(self.configParser.get('COLOR', 'BLACK'))
        if self.configParser.has_option('COLOR', 'WHITE'):
            self._config_default['color.white'] = self.helper.html_color_to_rgb(self.configParser.get('COLOR', 'WHITE'))
        if self.configParser.has_option('COLOR', 'RED'):
            self._config_default['color.red'] = self.helper.html_color_to_rgb(self.configParser.get('COLOR', 'RED'))
        if self.configParser.has_option('COLOR', 'GREEN'):
            self._config_default['color.green'] = self.helper.html_color_to_rgb(self.configParser.get('COLOR', 'GREEN'))
        if self.configParser.has_option('COLOR', 'ORANGE'):
            self._config_default['color.orange'] = self.helper.html_color_to_rgb(self.configParser.get('COLOR', 'ORANGE'))
            
        return self._config_default
            