from datetime import timedelta

class DrawToDisplay_Default:

    # default for 320x240
    _drawSetting = {}
    _drawSetting['startscreen.logo'] = ""
    _drawSetting['startscreen.clock.fontsize'] = 60
    _drawSetting['startscreen.clock.height_margin'] = 88
    
    default_info_text = ""
    default_info_color = ""
    
    def __init__(self, helper, _ConfigDefault):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault
        
        self.helper.printout("[info]    ", self._ConfigDefault['mesg.green'])
        self.helper.printout("Screen Setup  " + str(self._ConfigDefault['display.resolution']))
        
    def setPygameScreen(self, pygame, screen):
        self.pygame = pygame
        self.screen = screen
        
        getattr(self, 'SetupDrawSetting'+self._ConfigDefault['display.resolution'])()
    
    def Screen320x240(self):
        return (320, 240)
    
    def Screen480x272(self):
        return (480, 272)
    
    def Screen480x320(self):
        return (480, 320)
    
    def SetupDrawSetting320x240(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_320x240.png')
    
    def SetupDrawSetting480x272(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x272.png')
        self._drawSetting['startscreen.clock.fontsize'] = 64
        self._drawSetting['startscreen.clock.height_margin'] = 102
    
    def SetupDrawSetting480x320(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x320.png')
        self._drawSetting['startscreen.clock.fontsize'] = 75
        self._drawSetting['startscreen.clock.height_margin'] = 118
    
    def setInfoText(self, text, color):
        self.default_info_text = text
        self.default_info_color = color
    
    def infoTextKODI(self, text, color):
        self.displaytext(text, 32, (self.screen.get_width()/2), 20, 'none', color)
    
    def displaytext(self, text, size, x, y, floating, color):
        font = self.pygame.font.Font(self._ConfigDefault['basedirpath']+"fonts/MC360.ttf", size)
        text = font.render(text, 1, color)
        if floating == 'right':
            x = x - text.get_rect().width
            y = y - text.get_rect().height
        elif floating == 'left':
            x = x
            y = y - text.get_rect().height
        else:
            x = x - (text.get_rect().width/2)
            y = y - (text.get_rect().height/2) 
            
        self.screen.blit(text, [x, y])
    
    def drawLogoStartScreen(self, time_now, media_total):
        if self.default_info_text != '':
            self.infoTextKODI(self.default_info_text, self.default_info_color)
        else:
            self.infoTextKODI("KodiDisplayInfo", self._ConfigDefault['color.white'])
        
        x = (self.screen.get_width()/2) - (self._drawSetting['startscreen.logo'].get_rect().width/2)
        y = (self.screen.get_height()/2) - (self._drawSetting['startscreen.logo'].get_rect().height/2)
        self.screen.blit(self._drawSetting['startscreen.logo'],(x,y-10))

        self.displaytext(time_now.strftime("%H:%M:%S"), self._drawSetting['startscreen.clock.fontsize'], (self.screen.get_width()/2), (self.screen.get_height()/2)+self._drawSetting['startscreen.clock.height_margin'], 'none', (self._ConfigDefault['color.white']))

        # total
        if len(media_total)>0:
            index = 1
            font_size = 28
            font_size_small = 24
            if self._ConfigDefault['display.resolution']=="320x240":
                font_size = 26
            margintop_begin = (self.screen.get_height()/2)-((font_size_small*len(media_total))+(font_size*len(media_total))/2)
            self.displaytext('Total:', font_size, 10, margintop_begin+font_size, 'left', self._ConfigDefault['color.grey'])
                
            jsonObject = media_total
            for name in jsonObject:
                total = jsonObject[name]

                self.displaytext(name, font_size_small, 10, margintop_begin+(font_size_small*index)+(index*font_size), 'left', self._ConfigDefault['color.white'])
    
                color = self._ConfigDefault['color.green']
                if 0 <= int(total) <= 10:
                    color = self._ConfigDefault['color.red']
                    
                self.displaytext(total, font_size, 10, margintop_begin+font_size+(font_size_small*index)+(index*font_size), 'left', color)
                index = index + 1

        # disk
        if len(self._ConfigDefault['config.localmountpath'])>0:
            index = 1
            font_size = 28
            font_size_small = 24
            if self._ConfigDefault['display.resolution']=="320x240":
                font_size = 26
            margintop_begin = (self.screen.get_height()/2)-((font_size_small*len(self._ConfigDefault['config.localmountpath']))+(font_size*len(self._ConfigDefault['config.localmountpath']))/2)
            self.displaytext('Disk:', font_size, self.screen.get_width()-10, margintop_begin+font_size, 'right', self._ConfigDefault['color.grey'])

            jsonObject = self._ConfigDefault['config.localmountpath']
            for name in jsonObject:
                path = jsonObject[name]
                    
                self.displaytext(name, font_size_small, self.screen.get_width()-10, margintop_begin+(font_size_small*index)+(index*font_size), 'right', self._ConfigDefault['color.white'])
                    
                disk_total, disk_used, disk_free, disk_free_percent = self.helper.diskUsage(path)        
            
                color = self._ConfigDefault['color.green']
                if 90 <= disk_free_percent <= 100:
                    color = self._ConfigDefault['color.red']
                    
                self.displaytext(str(int(disk_free_percent)) + '%', font_size, self.screen.get_width()-10, margintop_begin+font_size+(font_size_small*index)+(index*font_size), 'right', color)
                index = index + 1      
        