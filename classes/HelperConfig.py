import os
import ConfigParser

class HelperConfig:
    
    def __init__(self, helper, _ConfigDefault, basedirpath):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault
        
        helper.printout("[info]    ", _ConfigDefault['mesg.green'])
        print "Parse Config"
        self.configParser = ConfigParser.RawConfigParser()   
        configFilePath = r''+basedirpath+'config.txt'
        self.configParser.read(configFilePath)
        
        #Display FB
        if self.configParser.get('DISPLAY', 'FBDEV')!="":
            os.environ["SDL_FBDEV"] = self.configParser.get('DISPLAY', 'FBDEV')
    
    def parseConfig(self):
        if self.configParser.has_option('CONFIG', 'SCREENMODUS_VIDEO'):
            temp = self.configParser.get('CONFIG', 'SCREENMODUS_VIDEO')
            if temp=="time" or temp=="thumbnail":
                self._ConfigDefault['config.screenmodus_video'] = temp
            else:
                self.helper.printout("[warning]    ", self._ConfigDefault['mesg.yellow'])
                print "Config [CONFIG] SCREENMODUS_VIDEO not set correctly - default is activ!"
                
        if self.configParser.has_option('CONFIG', 'FORMATTIME_VIDEO'):
            temp = self.configParser.get('CONFIG', 'FORMATTIME_VIDEO')
            if temp=="minutes" or temp=="short" or temp=="long":
                self._ConfigDefault['config.timeformat'] = temp
            else:
                self.helper.printout("[warning]    ", self._ConfigDefault['mesg.yellow'])
                print "Config [CONFIG] FORMATTIME_VIDEO not set correctly - default is activ!"
                
        if self.configParser.has_option('CONFIG', 'SCREENMODUS_AUDIO'):
            temp = self.configParser.get('CONFIG', 'SCREENMODUS_AUDIO')
            if temp=="thumbnail":
                self._ConfigDefault['config.screenmodus_audio'] = temp
            else:
                self.helper.printout("[warning]    ", self._ConfigDefault['mesg.yellow'])
                print "Config [CONFIG] SCREENMODUS_VIDEO not set correctly - default is activ!"
                
        if self.configParser.has_option('CONFIG', 'FORMATTIME_AUDIO'):
            temp = self.configParser.get('CONFIG', 'FORMATTIME_AUDIO')
            if temp=="short" or temp=="long":
                self._ConfigDefault['config.formattime_audio'] = temp
            else:
                self.helper.printout("[warning]    ", self._ConfigDefault['mesg.yellow'])
                print "Config [CONFIG] FORMATTIME_AUDIO not set correctly - default is activ!"
                
        if self.configParser.has_option('DISPLAY', 'RESOLUTION'):
            temp = self.configParser.get('DISPLAY', 'RESOLUTION')
            if temp=="320x240" or temp=="480x272" or temp=="480x320":
                self._ConfigDefault['display.resolution'] = temp
            else:
                self.helper.printout("[warning]    ", self._ConfigDefault['mesg.yellow'])
                print "Config [DISPLAY] RESOLUTION not set correctly - default is activ!"
        
        if self.configParser.has_option('KODI_WEBSERVER', 'HOST'):
            self._ConfigDefault['KODI.webserver.host'] = self.configParser.get('KODI_WEBSERVER', 'HOST')
        if self.configParser.has_option('KODI_WEBSERVER', 'PORT'):
            self._ConfigDefault['KODI.webserver.port'] = self.configParser.get('KODI_WEBSERVER', 'PORT')
        if self.configParser.has_option('KODI_WEBSERVER', 'USER'):
            self._ConfigDefault['KODI.webserver.user'] = self.configParser.get('KODI_WEBSERVER', 'USER')
        if self.configParser.has_option('KODI_WEBSERVER', 'PASS'):
            self._ConfigDefault['KODI.webserver.pass'] = self.configParser.get('KODI_WEBSERVER', 'PASS')        
                
        if self.configParser.has_option('COLOR', 'BLACK'):
            self._ConfigDefault['color.black'] = self.helper.HTMLColorToRGB(self.configParser.get('COLOR', 'BLACK'))
        if self.configParser.has_option('COLOR', 'WHITE'):
            self._ConfigDefault['color.white'] = self.helper.HTMLColorToRGB(self.configParser.get('COLOR', 'WHITE'))
        if self.configParser.has_option('COLOR', 'RED'):
            self._ConfigDefault['color.red'] = self.helper.HTMLColorToRGB(self.configParser.get('COLOR', 'RED'))
        if self.configParser.has_option('COLOR', 'GREEN'):
            self._ConfigDefault['color.green'] = self.helper.HTMLColorToRGB(self.configParser.get('COLOR', 'GREEN'))
        if self.configParser.has_option('COLOR', 'ORANGE'):
            self._ConfigDefault['color.orange'] = self.helper.HTMLColorToRGB(self.configParser.get('COLOR', 'ORANGE'))
            
        return self._ConfigDefault
            