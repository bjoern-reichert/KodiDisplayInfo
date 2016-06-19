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
        print "Screen Setup  " + str(self._ConfigDefault['display.resolution'])
        
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
    
    def drawLogoStartScreen(self, time_now):
        if self.default_info_text != '':
            self.infoTextKODI(self.default_info_text, self.default_info_color)
        else:
            self.infoTextKODI("KodiDisplayInfo", self._ConfigDefault['color.white'])
        
        x = (self.screen.get_width()/2) - (self._drawSetting['startscreen.logo'].get_rect().width/2)
        y = (self.screen.get_height()/2) - (self._drawSetting['startscreen.logo'].get_rect().height/2)
        self.screen.blit(self._drawSetting['startscreen.logo'],(x,y-10))

        self.displaytext(time_now.strftime("%H:%M:%S"), self._drawSetting['startscreen.clock.fontsize'], (self.screen.get_width()/2), (self.screen.get_height()/2)+self._drawSetting['startscreen.clock.height_margin'], 'none', (self._ConfigDefault['color.white']))
