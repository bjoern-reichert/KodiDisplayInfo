class DrawToDisplayAudioThumbnail:
    
    # default for 320x240
    __drawsetting = {
        'videoinfo.image_width_height': 0,
        'videoinfo.margin_top_media_album': 33,
        'videoinfo.margin_top_media_artist': 60,
        'videoinfo.margin_top_media_artist.maxcount': 2,
        'videoinfo.margin_top_media_title': 55,
        'videoinfo.margin_top_media_title.maxcount': 2,
        'videoinfo.progressbar.margin_top': 150,
        'videoinfo.progressbar.height': 25,
        'videoinfo.button.play': "",
        'videoinfo.button.break': "",
        'videoinfo.title.fontsize': 43,
        'videoinfo.title.height_margin': 4,
        'videoinfo.time_now.fontsize': 60,
        'videoinfo.time_now.height_margin': 68,
        'videoinfo.time_end.fontsize': 60,
        'videoinfo.time_end.height_margin': 68,
        'videoinfo.time.fontsize': 64,
        'videoinfo.time.margin_left': 0,
        'videoinfo.time.margin_top': 67
    }

    # in seconds
    __time = 0
    __totaltime = 0

    __thumbnail = ""

    __img_button_play = None
    __img_button_break = None
    
    def __init__(self, helper, image, config_default):
        self.__pygame = None
        self.__screen = None
        self.__draw_default = None
        self.__helper = helper
        self.__image = image
        self.__config_default = config_default
        
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
        self.__drawsetting['videoinfo.image_width_height'] = 160
        
        self.__drawsetting['videoinfo.margin_top_media_album'] = 33
        self.__drawsetting['videoinfo.margin_top_media_artist'] = 65
        self.__drawsetting['videoinfo.margin_top_media_artist.maxcount'] = 2
        self.__drawsetting['videoinfo.margin_top_media_title'] = 65
        self.__drawsetting['videoinfo.margin_top_media_title.maxcount'] = 2
        
        self.__drawsetting['videoinfo.progressbar.margin_top'] = 162
        self.__drawsetting['videoinfo.progressbar.height'] = 34
        
        self.__drawsetting['videoinfo.button.play'] = self.__config_default['basedirpath']+'img/button_play_480x320.png'
        self.__drawsetting['videoinfo.button.break'] = self.__config_default['basedirpath']+'img/button_break_480x320.png'
    
        self.__drawsetting['videoinfo.title.fontsize'] = 60
        self.__drawsetting['videoinfo.title.height_margin'] = 5
    
        self.__drawsetting['videoinfo.time_now.fontsize'] = 80
        self.__drawsetting['videoinfo.time_now.height_margin'] = 86
        self.__drawsetting['videoinfo.time_end.fontsize'] = 80
        self.__drawsetting['videoinfo.time_end.height_margin'] = 86
        
        self.__drawsetting['videoinfo.time.fontsize'] = 81
        self.__drawsetting['videoinfo.time.margin_left'] = 14
        self.__drawsetting['videoinfo.time.margin_top'] = 83
    
    def setupdrawsetting480x320(self):       
        self.__drawsetting['videoinfo.image_width_height'] = 200
        
        self.__drawsetting['videoinfo.margin_top_media_album'] = 33
        self.__drawsetting['videoinfo.margin_top_media_artist'] = 69
        self.__drawsetting['videoinfo.margin_top_media_artist.maxcount'] = 2
        self.__drawsetting['videoinfo.margin_top_media_title'] = 69
        self.__drawsetting['videoinfo.margin_top_media_title.maxcount'] = 3
        
        self.__drawsetting['videoinfo.progressbar.margin_top'] = 205
        self.__drawsetting['videoinfo.progressbar.height'] = 34
        
        self.__drawsetting['videoinfo.button.play'] = self.__config_default['basedirpath']+'img/button_play_480x320.png'
        self.__drawsetting['videoinfo.button.break'] = self.__config_default['basedirpath']+'img/button_break_480x320.png'
    
        self.__drawsetting['videoinfo.title.fontsize'] = 60
        self.__drawsetting['videoinfo.title.height_margin'] = 5
    
        self.__drawsetting['videoinfo.time_now.fontsize'] = 80
        self.__drawsetting['videoinfo.time_now.height_margin'] = 86
        self.__drawsetting['videoinfo.time_end.fontsize'] = 80
        self.__drawsetting['videoinfo.time_end.height_margin'] = 86
        
        self.__drawsetting['videoinfo.time.fontsize'] = 81
        self.__drawsetting['videoinfo.time.margin_left'] = 14
        self.__drawsetting['videoinfo.time.margin_top'] = 83
        
    def setthumbnail(self, url, file):
        max_width = self.__drawsetting['videoinfo.image_width_height']-20
        max_heigth = self.__drawsetting['videoinfo.image_width_height']-20

        if self.__config_default['display.resolution']!="320x240":
            self.__thumbnail = self.__image.scaleimage(url, file, max_width, max_heigth)
        
    def drawprogressbar(self, margin_top = 0):
        rect_bar = self.__pygame.Rect((10,self.__drawsetting['videoinfo.progressbar.margin_top']+margin_top), (self.__screen.get_width()-20,self.__drawsetting['videoinfo.progressbar.height']))
        
        if self.__totaltime > 0:
            percent_done = int(( 1. * rect_bar.width / self.__totaltime) * self.__time)
        else:
            percent_done = 0
          
        rect_done = self.__pygame.Rect(rect_bar)
        rect_done.width = percent_done
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.green'], rect_bar)
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.orange'], rect_done)
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.white'], rect_bar, 1)
        
    def drawproperties(self, media_title, speed, media_time, media_totaltime, media_album, media_artist):
        self.__time = self.__helper.format_to_seconds(media_time[0], media_time[1], media_time[2])
        self.__totaltime = self.__helper.format_to_seconds(media_totaltime[0], media_totaltime[1], media_totaltime[2])

        width_text = (self.__screen.get_width()-self.__drawsetting['videoinfo.image_width_height'])-20
        margin_top_media_title = self.__drawsetting['videoinfo.margin_top_media_title']
        image_width_height = self.__drawsetting['videoinfo.image_width_height']
        if self.__config_default['display.resolution']=="320x240":
            image_width_height = 10
            width_text = self.__screen.get_width()-20
        
        self.__draw_default.displaytext(media_album, 24, image_width_height+5, self.__drawsetting['videoinfo.margin_top_media_album'], 'left', (self.__config_default['color.white']))
        
        font=self.__pygame.font.Font(self.__config_default['basedirpath']+"fonts/MC360.ttf", 24)
        lines_artist = self.__helper.wrapline(media_artist, font, width_text)
        
        lines_artist_index = 0
        for (i, line) in enumerate(lines_artist):
            if (i+1) > self.__drawsetting['videoinfo.margin_top_media_artist.maxcount']:
                break
            self.__draw_default.displaytext(line, 24, image_width_height+5, self.__drawsetting['videoinfo.margin_top_media_artist']+(24*i), 'left', (self.__config_default['color.grey']))
            lines_artist_index = lines_artist_index + 1
        
        font=self.__pygame.font.Font(self.__config_default['basedirpath']+"fonts/MC360.ttf", 28)
        lines = self.__helper.wrapline(media_title, font, width_text)
        
        for (i, line) in enumerate(lines):
            if lines_artist_index>1:
                if (i+1) > self.__drawsetting['videoinfo.margin_top_media_title.maxcount']:
                    break
            self.__draw_default.displaytext(line, 28, image_width_height+5, margin_top_media_title+(24*lines_artist_index)+12+(28*i), 'left', (self.__config_default['color.white']))

        margin_progessbar = self.__drawsetting['videoinfo.progressbar.margin_top']+self.__drawsetting['videoinfo.progressbar.height']
 
        if self.__config_default['config.formattime_audio']=="short" or self.__config_default['config.formattime_audio']=="long":
            fontsize = 64
            margintop = 9
            if self.__config_default['config.formattime_audio']=="long":
                fontsize = 53
                margintop = 15
                
            if self.__config_default['display.resolution']=="320x240" and self.__config_default['config.formattime_audio']=="long":
                fontsize = 34
                margintop = 16
            elif self.__config_default['display.resolution']=="320x240" and self.__config_default['config.formattime_audio']=="short":
                fontsize = 46
                margintop = 9
            
            self.__draw_default.displaytext(self.__helper.format_to_string(media_time[0], media_time[1], media_time[2], self.__config_default['config.formattime_audio']), fontsize, 62+self.__drawsetting['videoinfo.time.margin_left'], margin_progessbar+self.__drawsetting['videoinfo.time.margin_top']-margintop, 'left', (self.__config_default['color.white']))
            self.__draw_default.displaytext(self.__helper.format_to_string(media_totaltime[0], media_totaltime[1], media_totaltime[2], self.__config_default['config.formattime_audio']), fontsize, self.__screen.get_width()-10, margin_progessbar+self.__drawsetting['videoinfo.time.margin_top']-margintop, 'right', (self.__config_default['color.white']))  
               
        self.drawprogressbar()

        if self.__img_button_play is not None and self.__img_button_break is not None:
            if speed == 1:
                self.__screen.blit(self.__img_button_play, (8, margin_progessbar+8))
            else:
                self.__screen.blit(self.__img_button_break, (8, margin_progessbar+8))
            
        if self.__thumbnail != "":
            self.__screen.blit(self.__thumbnail,(10,10))