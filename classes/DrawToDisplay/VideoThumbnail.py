from datetime import timedelta


class DrawToDisplayVideoThumbnail:
    
    # default for 320x240
    __drawsetting = {
        'videoinfo.progressbar.margin_left': 160,
        'videoinfo.progressbar.width': 25,
        'videoinfo.button.play': "",
        'videoinfo.button.break': "",
        'videoinfo.title.fontsize': 43,
        'videoinfo.title.height_margin': 4,
        'videoinfo.time_now.fontsize': 35,
        'videoinfo.time_now.height_margin': 16,
        'videoinfo.time_end.fontsize': 35,
        'videoinfo.time_end.height_margin': 54,
        'videoinfo.time.fontsize': 64,
        'videoinfo.time.margin_top': 67,
        'videoinfo.time.margin_bottom': 2
    }

    # in seconds
    __time = 0
    __totaltime = 0
    
    __thumbnail = ""

    __img_button_play = None
    __img_button_break = None
    
    def __init__(self, helper, image, _config_default):
        self.__pygame = None
        self.__screen = None
        self.__draw_default = None
        self.__helper = helper
        self.__image = image
        self.__config_default = _config_default
        
    def set_pygamescreen(self, pygame, screen, draw_default):
        self.__pygame = pygame
        self.__screen = screen
        self.__draw_default = draw_default
        
        getattr(self, 'setupdrawsetting'+self.__config_default['display.resolution'])()
        if self.__helper.check_file(self.__drawsetting['videoinfo.button.play']):
            self.__img_button_play = self.__pygame.image.load(self.__drawsetting['videoinfo.button.play'])
        if self.__helper.check_file(self.__drawsetting['videoinfo.button.break']):
            self.__img_button_break = self.__pygame.image.load(self.__drawsetting['videoinfo.button.break'])

    def setupdrawsetting320x240(self):
        self.__drawsetting['videoinfo.button.play'] = self.__config_default['basedirpath']+'img/button_play_320x240.png'
        self.__drawsetting['videoinfo.button.break'] = self.__config_default['basedirpath']+'img/button_break_320x240.png'
    
    def setupdrawsetting480x272(self):       
        self.__drawsetting['videoinfo.progressbar.margin_left'] = 220
        self.__drawsetting['videoinfo.progressbar.width'] = 34
        
        self.__drawsetting['videoinfo.button.play'] = self.__config_default['basedirpath']+'img/button_play_480x320.png'
        self.__drawsetting['videoinfo.button.break'] = self.__config_default['basedirpath']+'img/button_break_480x320.png'
    
        self.__drawsetting['videoinfo.title.fontsize'] = 60
        self.__drawsetting['videoinfo.title.height_margin'] = 5
    
        self.__drawsetting['videoinfo.time_now.fontsize'] = 60
        self.__drawsetting['videoinfo.time_now.height_margin'] = 9
        self.__drawsetting['videoinfo.time_end.fontsize'] = 60
        self.__drawsetting['videoinfo.time_end.height_margin'] = 76
        
        self.__drawsetting['videoinfo.time.fontsize'] = 81
        self.__drawsetting['videoinfo.time.margin_top'] = 83
        self.__drawsetting['videoinfo.time.margin_bottom'] = 6
    
    def setupdrawsetting480x320(self):        
        self.__drawsetting['videoinfo.progressbar.margin_left'] = 220
        self.__drawsetting['videoinfo.progressbar.width'] = 34
        
        self.__drawsetting['videoinfo.button.play'] = self.__config_default['basedirpath']+'img/button_play_480x320.png'
        self.__drawsetting['videoinfo.button.break'] = self.__config_default['basedirpath']+'img/button_break_480x320.png'
    
        self.__drawsetting['videoinfo.title.fontsize'] = 60
        self.__drawsetting['videoinfo.title.height_margin'] = 5
    
        self.__drawsetting['videoinfo.time_now.fontsize'] = 60
        self.__drawsetting['videoinfo.time_now.height_margin'] = 9
        self.__drawsetting['videoinfo.time_end.fontsize'] = 60
        self.__drawsetting['videoinfo.time_end.height_margin'] = 76
        
        self.__drawsetting['videoinfo.time.fontsize'] = 81
        self.__drawsetting['videoinfo.time.margin_top'] = 83
        self.__drawsetting['videoinfo.time.margin_bottom'] = 6
        
    def drawprogressbar(self):
        rect_bar = self.__pygame.Rect((self.__drawsetting['videoinfo.progressbar.margin_left'],10), (self.__drawsetting['videoinfo.progressbar.width'],self.__screen.get_height()-20))
        
        if self.__totaltime > 0:
            percent_done = int((1. * rect_bar.height / self.__totaltime) * self.__time)
        else:
            percent_done = 0
          
        rect_done = self.__pygame.Rect(rect_bar)
        rect_done.height = percent_done
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.green'], rect_bar)
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.orange'], rect_done)
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.white'], rect_bar, 1)
        
    def setthumbnail(self, url, file):
        max_width = self.__drawsetting['videoinfo.progressbar.margin_left']-20
        max_heigth = self.__screen.get_height()-20

        self.__thumbnail = self.__image.scaleimage(url, file, max_width, max_heigth)
                
    def drawproperties(self, time_now, speed, media_time, media_totaltime):
        self.__time = self.__helper.format_to_seconds(media_time[0], media_time[1], media_time[2])
        self.__totaltime = self.__helper.format_to_seconds(media_totaltime[0], media_totaltime[1], media_totaltime[2])

        self.__draw_default.displaytext(str(time_now.strftime("%H:%M")), self.__drawsetting['videoinfo.time_now.fontsize'], self.__screen.get_width()-10, (self.__screen.get_height()/2)-self.__drawsetting['videoinfo.time_now.height_margin'], 'right', (self.__config_default['color.white']))
        
        addtonow = time_now + timedelta(seconds=(self.__totaltime-self.__time))
        self.__draw_default.displaytext(str(addtonow.strftime("%H:%M")), self.__drawsetting['videoinfo.time_end.fontsize'], self.__screen.get_width()-10, (self.__screen.get_height()/2)+self.__drawsetting['videoinfo.time_end.height_margin'], 'right', (self.__config_default['color.white']))
    
        margin_left = 10
        if self.__config_default['display.resolution'] == "320x240":
            margin_left = 8
        margin_progessbar = self.__drawsetting['videoinfo.progressbar.margin_left']+self.__drawsetting['videoinfo.progressbar.width']

        if self.__config_default['config.formattime_video'] == "minutes":
            self.__draw_default.displaytext(str(self.__helper.format_to_minutes(media_time[0], media_time[1])), self.__drawsetting['videoinfo.time.fontsize'], margin_progessbar+margin_left, self.__drawsetting['videoinfo.time.margin_top'], 'left', (self.__config_default['color.white']))
            self.__draw_default.displaytext(str(self.__helper.format_to_minutes(media_totaltime[0], media_totaltime[1])), self.__drawsetting['videoinfo.time.fontsize'], margin_progessbar+margin_left, self.__screen.get_height()+self.__drawsetting['videoinfo.time.margin_bottom'], 'left', (self.__config_default['color.white']))  
        elif self.__config_default['config.formattime_video'] == "short" or self.__config_default['config.formattime_video'] == "long":
            self.__drawsetting['videoinfo.time.fontsize'] = 59
            self.__drawsetting['videoinfo.time.margin_top'] = 64
            self.__drawsetting['videoinfo.time.margin_bottom'] = 0
            if self.__config_default['display.resolution']=="320x240":
                self.__drawsetting['videoinfo.time.fontsize'] = 34
                self.__drawsetting['videoinfo.time.margin_top'] = 41
                self.__drawsetting['videoinfo.time.margin_bottom'] = -3

            self.__draw_default.displaytext(self.__helper.format_to_string(media_time[0], media_time[1], media_time[2], self.__config_default['config.formattime_video']), self.__drawsetting['videoinfo.time.fontsize'], margin_progessbar+margin_left, self.__drawsetting['videoinfo.time.margin_top'], 'left', (self.__config_default['color.white']))
            self.__draw_default.displaytext(self.__helper.format_to_string(media_totaltime[0], media_totaltime[1], media_totaltime[2], self.__config_default['config.formattime_video']), self.__drawsetting['videoinfo.time.fontsize'], margin_progessbar+margin_left, self.__screen.get_height()+self.__drawsetting['videoinfo.time.margin_bottom'], 'left', (self.__config_default['color.white']))
               
        self.drawprogressbar()

        if self.__img_button_play is not None and self.__img_button_break is not None:
            if speed == 1:
                self.__screen.blit(self.__img_button_play, (margin_progessbar+10, (self.__screen.get_height()/2)-(self.__img_button_play.get_rect().size[1]/2)))
            else:
                self.__screen.blit(self.__img_button_break, (margin_progessbar+10, (self.__screen.get_height()/2)-(self.__img_button_break.get_rect().size[1]/2)))

        if self.__thumbnail != "":
            self.__screen.blit(self.__thumbnail, (10, 10))