from datetime import timedelta


class DrawToDisplayVideoTime:
    
    # default for 320x240
    __drawsetting = {
        'videoinfo.progressbar.margin_top': 85,
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

    __img_button_play = None
    __img_button_break = None
    
    def __init__(self, helper, _config_default):
        self.__pygame = None
        self.__screen = None
        self.__draw_default = None
        self.__helper = helper
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
        self.__drawsetting['videoinfo.progressbar.margin_top'] = 92
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
        self.__drawsetting['videoinfo.progressbar.margin_top'] = 120
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
        
    def drawprogressbar(self, margin_top = 0):
        rect_bar = self.__pygame.Rect((10, self.__drawsetting['videoinfo.progressbar.margin_top']+margin_top), (self.__screen.get_width()-20, self.__drawsetting['videoinfo.progressbar.height']))
        
        if self.__totaltime > 0:
            percent_done = int((1. * rect_bar.width / self.__totaltime) * self.__time)
        else:
            percent_done = 0
          
        rect_done = self.__pygame.Rect(rect_bar)
        rect_done.width = percent_done
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.green'], rect_bar)
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.orange'], rect_done)
        self.__pygame.draw.rect(self.__screen, self.__config_default['color.white'], rect_bar, 1)
        
    def wraplines(self, title, fontsize):
        width_text = self.__screen.get_width()-20
        font = self.__pygame.font.Font(self.__config_default['basedirpath']+"fonts/MC360.ttf", fontsize)
        return self.__helper.wrapline(title, font, width_text)
        
    def drawproperties(self, video_title, time_now, speed, media_time, media_totaltime):
        margin_top = 0
        videoinfo_title_fontsize = self.__drawsetting['videoinfo.title.fontsize']
        
        self.__time = self.__helper.format_to_seconds(media_time[0], media_time[1], media_time[2])
        self.__totaltime = self.__helper.format_to_seconds(media_totaltime[0], media_totaltime[1], media_totaltime[2])

        lines = self.wraplines(video_title, self.__drawsetting['videoinfo.title.fontsize'])
        if len(lines) > 1:
            second_title_height_margin = 0
            if self.__config_default['display.resolution'] == "480x320":
                videoinfo_title_fontsize = 49
                margin_top = -22
                second_title_height_margin = -46
            if self.__config_default['display.resolution'] == "480x272":
                self.__drawsetting['videoinfo.title.height_margin'] = 0
                videoinfo_title_fontsize = 42
                margin_top = -11
                second_title_height_margin = -40
            if self.__config_default['display.resolution'] == "320x240":
                videoinfo_title_fontsize = 38
                margin_top = -16
                second_title_height_margin = -36
                lines = self.wraplines(video_title, videoinfo_title_fontsize)
             
            lines = lines[0:2]
            lines.reverse()
            for (i, line) in enumerate(lines):
                if i > 1:  # max 2
                    break
                self.__draw_default.displaytext(line, videoinfo_title_fontsize, 10, self.__screen.get_height()-self.__drawsetting['videoinfo.title.height_margin']+(second_title_height_margin*i), 'left', self.__config_default['color.white'])
        else:
            self.__draw_default.displaytext(video_title, self.__drawsetting['videoinfo.title.fontsize'], 10, self.__screen.get_height()-self.__drawsetting['videoinfo.title.height_margin'], 'left', self.__config_default['color.white'])
        
        self.__draw_default.displaytext(str(time_now.strftime("%H:%M")), self.__drawsetting['videoinfo.time_now.fontsize'], 10, self.__drawsetting['videoinfo.time_now.height_margin'], 'left', self.__config_default['color.white'])

        addtonow = time_now + timedelta(seconds=(self.__totaltime-self.__time))
        self.__draw_default.displaytext(str(addtonow.strftime("%H:%M")), self.__drawsetting['videoinfo.time_end.fontsize'], self.__screen.get_width()-10, self.__drawsetting['videoinfo.time_end.height_margin'], 'right', self.__config_default['color.white'])
    
        margin_progessbar = self.__drawsetting['videoinfo.progressbar.margin_top']+self.__drawsetting['videoinfo.progressbar.height']+margin_top

        if self.__config_default['config.formattime_video'] == "minutes":
            self.__draw_default.displaytext(str(self.__helper.format_to_minutes(media_time[0], media_time[1])), self.__drawsetting['videoinfo.time.fontsize'], 62+self.__drawsetting['videoinfo.time.margin_left'], margin_progessbar+self.__drawsetting['videoinfo.time.margin_top'], 'left', self.__config_default['color.white'])
            self.__draw_default.displaytext(str(self.__helper.format_to_minutes(media_totaltime[0], media_totaltime[1])), self.__drawsetting['videoinfo.time.fontsize'], self.__screen.get_width()-10, margin_progessbar+self.__drawsetting['videoinfo.time.margin_top'], 'right', self.__config_default['color.white'])  
        elif self.__config_default['config.formattime_video'] == "short" or self.__config_default['config.formattime_video'] == "long":
            fontsize = 64
            margintop = 9
            if self.__config_default['config.formattime_video'] == "long":
                fontsize = 53
                margintop = 15
                
            if self.__config_default['display.resolution'] == "320x240" and self.__config_default['config.formattime_video'] == "long":
                fontsize = 34
                margintop = 16
            elif self.__config_default['display.resolution'] == "320x240" and self.__config_default['config.formattime_video'] == "short":
                fontsize = 46
                margintop = 9
            
            self.__draw_default.displaytext(self.__helper.format_to_string(media_time[0], media_time[1], media_time[2], self.__config_default['config.formattime_video']), fontsize, 62+self.__drawsetting['videoinfo.time.margin_left'], margin_progessbar+self.__drawsetting['videoinfo.time.margin_top']-margintop, 'left', self.__config_default['color.white'])
            self.__draw_default.displaytext(self.__helper.format_to_string(media_totaltime[0], media_totaltime[1], media_totaltime[2], self.__config_default['config.formattime_video']), fontsize, self.__screen.get_width()-10, margin_progessbar+self.__drawsetting['videoinfo.time.margin_top']-margintop, 'right', self.__config_default['color.white'])  
               
        self.drawprogressbar(margin_top)

        if self.__img_button_play is not None and self.__img_button_break is not None:
            if speed == 1:
                self.__screen.blit(self.__img_button_play, (8, margin_progessbar+8))
            else:
                self.__screen.blit(self.__img_button_break, (8, margin_progessbar+8))