import copy


class DrawToDisplayDefault:

    # default for 320x240
    __drawsetting = {
        'startscreen.logo': "",
        'startscreen.clock.fontsize': 60,
        'startscreen.clock.height_margin': 90
    }

    __default_info_text = ""
    __default_info_color = ""
    __img_logo = None

    def __init__(self, helper, config_default):
        self.__pygame = None
        self.__screen = None
        self.__helper = helper
        self.__config_default = config_default

        self.__helper.printout("[info]    ", self.__config_default['mesg.green'])
        self.__helper.printout("Screen Setup  " + str(self.__config_default['display.resolution']))
        
    def set_pygamescreen(self, pygame, screen):
        self.__pygame = pygame
        self.__screen = screen
        
        getattr(self, 'setupdrawsetting'+self.__config_default['display.resolution'])()
        if self.__helper.check_file(self.__drawsetting['startscreen.logo']):
            self.__img_logo = self.__pygame.image.load(self.__drawsetting['startscreen.logo'])

    @staticmethod
    def screen320x240():
        return 320, 240

    @staticmethod
    def screen480x272():
        return 480, 272
    
    @staticmethod
    def screen480x320():
        return 480, 320
    
    def setupdrawsetting320x240(self):
        self.__drawsetting['startscreen.logo'] = self.__config_default['basedirpath']+'img/kodi_logo_320x240.png'
    
    def setupdrawsetting480x272(self):
        self.__drawsetting['startscreen.logo'] = self.__config_default['basedirpath']+'img/kodi_logo_480x272.png'
        self.__drawsetting['startscreen.clock.fontsize'] = 64
        self.__drawsetting['startscreen.clock.height_margin'] = 102
    
    def setupdrawsetting480x320(self):
        self.__drawsetting['startscreen.logo'] = self.__config_default['basedirpath']+'img/kodi_logo_480x320.png'
        self.__drawsetting['startscreen.clock.fontsize'] = 75
        self.__drawsetting['startscreen.clock.height_margin'] = 118
    
    def setinfotext(self, text, color):
        self.__default_info_text = text
        self.__default_info_color = color
    
    def __infotextkodi(self, text, color):
        self.displaytext(text, 34, (self.__screen.get_width()/2), 20, 'none', color)
    
    def displaytext(self, text, size, x, y, floating, color):
        font = self.__pygame.font.Font(self.__config_default['basedirpath']+"fonts/MC360.ttf", size)
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
            
        self.__screen.blit(text, [x, y])
    
    def drawlogostartscreen(self, time_now, media_total):
        if self.__default_info_text != '':
            self.__infotextkodi(self.__default_info_text, self.__default_info_color)
        else:
            self.__infotextkodi("KodiDisplayInfo", self.__config_default['color.white'])

        if self.__img_logo is not None:
            x = (self.__screen.get_width()/2) - (self.__img_logo.get_rect().width/2)
            y = (self.__screen.get_height()/2) - (self.__img_logo.get_rect().height/2)
            self.__screen.blit(self.__img_logo, (x, y-10))

        self.displaytext(time_now.strftime("%H:%M:%S"), self.__drawsetting['startscreen.clock.fontsize'], (self.__screen.get_width()/2), (self.__screen.get_height()/2)+self.__drawsetting['startscreen.clock.height_margin'], 'none', (self.__config_default['color.white']))

        font_size = 62
        font_size_small = 30
        if self.__config_default['display.resolution']=="320x240":
            font_size = 38
            font_size_small = 24

        # total
        if len(media_total)>0:
            index = 0
            
            margintop_begin = (self.__screen.get_height()/2)-((font_size_small+(font_size_small*len(media_total))+(font_size*len(media_total)))/2)-6
            self.displaytext('Total:', font_size_small, 10, margintop_begin+font_size_small, 'left', self.__config_default['color.grey'])

            jsonobject = media_total
            for name in copy.copy(jsonobject):
                total = jsonobject[name]

                self.displaytext(name, font_size_small, 10, margintop_begin+font_size_small+font_size_small+(font_size_small*index)+(index*font_size), 'left', self.__config_default['color.white'])
    
                color = self.__config_default['color.green']
                if 0 <= int(total) <= 10:
                    color = self.__config_default['color.red']
                    
                self.displaytext(total, font_size, 10, margintop_begin+font_size_small+font_size_small+font_size+(font_size_small*index)+(index*font_size), 'left', color)
                index = index + 1

        # disk
        if len(self.__config_default['config.localmountpath'])>0:
            index = 0

            margintop_begin = (self.__screen.get_height()/2)-((font_size_small+(font_size_small*len(self.__config_default['config.localmountpath']))+(font_size*len(self.__config_default['config.localmountpath'])))/2)-6
            self.displaytext('Disk:', font_size_small, self.__screen.get_width()-10, margintop_begin+font_size_small, 'right', self.__config_default['color.grey'])

            jsonobject = self.__config_default['config.localmountpath']
            for name in copy.copy(jsonobject):
                path = jsonobject[name]

                self.displaytext(name, font_size_small, self.__screen.get_width()-10, margintop_begin+font_size_small+font_size_small+(font_size_small*index)+(index*font_size), 'right', self.__config_default['color.white'])

                disk_free_percent = self.__helper.disk_usage(path, "percent")        

                color = self.__config_default['color.green']
                if 90 <= disk_free_percent <= 100:
                    color = self.__config_default['color.red']

                self.displaytext(str(int(disk_free_percent)) + '%', font_size, self.__screen.get_width()-10, margintop_begin+font_size_small+font_size_small+font_size+(font_size_small*index)+(index*font_size), 'right', color)
                index = index + 1